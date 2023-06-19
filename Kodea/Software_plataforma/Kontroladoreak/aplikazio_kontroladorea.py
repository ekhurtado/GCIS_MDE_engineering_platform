import datetime
import os
import sys
import time
import pytz
import urllib3
from dateutil import parser
from kubernetes import client, config, watch

import utils

# Aplikazio mailaren ezaugarrientzako aldagaiak
group = "ehu.gcis.org"
version = "v1alpha1"
namespace = "default"
plural = "applications"

# Mikrozerbitzu mailaren informazioa
microserviceVersion = "v1alpha1"
microservicePlural = "microservices"


def controller():
    # Lehenik eta behin, klusterraren konfigurazio fitxategia
    config.load_kube_config(os.path.join("../klusterKonfigurazioa/k3s.yaml"))

    # Kontroladorea Docker edukiontzi baten barruan, eta klusterrean hedatu badago, kode hau erabili
    # if 'KUBERNETES_PORT' in os.environ:
    #     config.load_incluster_config()
    # else:
    #     config.load_kube_config()

    custom_client = client.CustomObjectsApi()  # Custom objektuetarako APIa lortzen dugu
    client_extension = client.ApiextensionsV1Api()  # CRDekin lan egiteko APIa lortzen dugu

    # Ondoren, aplikazioaren CRD sortuta ez badago kontrobatuko da
    try:
        client_extension.create_custom_resource_definition(utils.CRD_app())
        time.sleep(2)  # 2 segundo itxaroten da ondo sortu dela ziurtatzeko
        print("Aplikazioentzako CRDa sortu da.")
    except urllib3.exceptions.MaxRetryError as e:
        print("KONEXIO ERROREA!")
        print("Baliteke k3s.yaml fitxategiko IP helbide nagusia zuzena ez izatea")
        controller()
    except Exception as e:
        if "Reason: Conflict" in str(e):
            print("Aplikazioentzako CRDa jada existitzen da, begirale metodora pasatzen...")
        elif "No such file or directory" in str(e):
            print("Ezin izan da aplikazioaren definizioaren fitxategia aurkitu.")
            sys.exit()  # Kasu honetan, programa bukatzen da, fitxategi egokia sar ezazu, eta birrabiarazi

    # CRDa sisteman egonda, aplikazioen begiralera pasatuko da
    watcher(custom_client)


def watcher(custom_client):
    watcher = watch.Watch()  # Begiralea aktibatzen da
    startedTime = pytz.utc.localize(datetime.datetime.utcnow())  # Kontroladorearen hasiera data lortzen da

    for event in watcher.stream(custom_client.list_namespaced_custom_object, group, version, namespace, plural):
        print('Aplikazioen gertaera berria.')
        object = event['object']
        eventType = event['type']

        creationTime = parser.isoparse(object['metadata']['creationTimestamp'])
        if creationTime < startedTime:
            print("Gertaera zaharkitua da")
            continue

        # Gertaeraren objektua edukita, bere motaren arabera beharrezko jarduerak exekutatuko dira
        print("Gertaera berria: ", "ordua: ",
              datetime.datetime.now(), ", mota: ", eventType, ", objektuaren izena: ", object['metadata']['name'])

        match eventType:
            case "ADDED":  # Aplikazio berria
                # Aplikazioarekin erlazionatutako gertaera sortzen da, abisatuz aplikazio berria sortu dela
                eventObject = utils.customResourceEventObject(action='Created', CR_type="Application",
                                                              CR_object=object,
                                                              message='Aplikazio berria zuzen sortu da.',
                                                              reason='Created')
                eventAPI = client.CoreV1Api()
                eventAPI.create_namespaced_event("default", eventObject)

                # Aplikazioa abiarazten da
                deploy_application(object, custom_client)
            case "DELETED":  # Aplikazioa ezabatuta
                delete_application(object, custom_client)
            case "MODIFIED":  # Aplikazioa aldatuta
                check_modifications(object, custom_client)
            case _:  # default case
                pass


def deploy_application(appObject, custom_client):
    # Hasi aurretik, aplikazioaren egoera eguneratzeko gertaera sortzen da
    eventObject = utils.customResourceEventObject(action='Deploy', CR_type="Application",
                                                  CR_object=appObject,
                                                  message='Aplikazioaren hedapen hasita.',
                                                  reason='Deploying')
    eventAPI = client.CoreV1Api()
    eventAPI.create_namespaced_event("default", eventObject)

    # Ondoren, aplikazioaren objektuaren egoera atala sortzen da, adieraziz oraindik ez dela mikrozerbitzurik sortu.
    num_microservices = len(appObject['spec']['microservices'])
    status_object = {'status': {'microservices': [0] * num_microservices, 'ready': "0/" + str(num_microservices)}}
    for i in range(int(num_microservices)):
        status_object['status']['microservices'][i] = {'name': appObject['spec']['microservices'][i]['name'],
                                                       'status': "Creating"}
    custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                        appObject['metadata']['name'], status_object)

    # Orain, mikrozerbitzu bakoitza sortuko da
    for microsvc in appObject['spec']['microservices']:
        # Lehenik eta behin, beste mikrozerbitzuek aztertzen ari den mikrozerbitzuarekin komunikatu behar badira, Kubernetesen
        # zerbitzu deituriko bat sortu beharra dago, mikrozerbitzua eskuragarri egiteko
        if 'inPort' in microsvc:
            create_service(microsvc, appObject)

        # Orain, mikrozerbitzua bera sortu daiteke
        create_microservice(custom_client, microsvc, appObject)


def delete_application(appObject, custom_client):
    # Aplikazioaren mikrozerbitzu guztiak ezabatuko dira
    for microsvc in appObject['spec']['microservices']:
        custom_client.delete_namespaced_custom_object(group, microserviceVersion, namespace, microservicePlural,
                                                      microsvc['name'] + '-' + appObject['metadata']['name'])


def check_modifications(appObject, custom_client):
    eventAPI = client.CoreV1Api()  # Gertaerekin lan egiteko APIa lortzen da

    # Lehenik, aztertuko da nor izan den aplikazio objektua aldatu duena
    lastManager = appObject['metadata']['managedFields'][len(appObject['metadata']['managedFields']) - 1]['manager']
    if "microservice" in lastManager:
        # Bakarrik aplikazioaren barruko mikrozerbitzuak alda dezakete aplikazioaren objektua, zehazki egoera atala
        # Aldaketaren arduradunatik mikrozerbitzuaren izena lortzen da
        microserviceName = lastManager.replace('microservice-', '')
        microserviceName = microserviceName.replace('-' + appObject['metadata']['name'], '')

        # Egoera atala aldatu denez, abiarazitako mikrozerbitzuak aztertuko dira
        runningCount = 0
        for i in range(len(appObject['status']['microservices'])):
            if appObject['status']['microservices'][i]['status'] == "Running":
                runningCount += 1

                if appObject['status']['microservices'][i]['name'] == microserviceName:
                    # Mezua bidali duen mikrozerbitzua abiarazita badago, gertaera horren berri emango da
                    eventObject = utils.customResourceEventObject(action='Created', CR_type="Application",
                                                      CR_object=appObject,
                                                      message=microserviceName + ' mikrozerbitzua zuzen abiarazita.',
                                                      reason='Deployed')
                    eventAPI.create_namespaced_event("default", eventObject)

        # Abiarazitako mikrozerbitzu guztiak aztertuta, baten bat abiarazita badago, egoera atala eguneratuko da
        if runningCount != 0:
            appObject['status']['ready'] = str(runningCount) + "/" + appObject['status']['ready'].split("/")[1]

            if runningCount == len(appObject['status']['microservices']):
                # Mikrozerbitzu guztiak abiarazita badaude, gertaera horren berri emango dugu
                eventObject = utils.customResourceEventObject(action='Deployed', CR_type="Application",
                                                              CR_object=appObject,
                                                              message='Mikrozerbitzu guztiak zuzen abiarazita.',
                                                              reason='Running')
                eventAPI.create_namespaced_event("default", eventObject)

        # Bete diren aldaketekin, aplikazioaren egoera atala eguneratzen da
        custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                            appObject['metadata']['name'],
                                                            {'status': appObject['status']},
                                                            field_manager=appObject['metadata']['name'])


def create_microservice(custom_client, microsvcObject, appObject):
    # Mikrozerbitzuari beharrezko informazioa gehitu zaio (adibidez, hurrengo mikrozerbitzuarekin komunikatzeko datuak)
    microsvcObject = addFlowInfo(microsvcObject, appObject)
    # Mikrozerbitzuaren objetua eraikitzen da
    microservice_body = utils.microservice_object(microserviceInfo=microsvcObject, appName=appObject['metadata']['name'])
    # Mikrozerbitzu berria sortzen da
    custom_client.create_namespaced_custom_object(group, microserviceVersion, namespace, microservicePlural, microservice_body)

    # Behin mikrozerbitzuaren sorkuntza eskaera betez, bere objektuaren egoera atala eguneratuko da, sortzen ari dela
    # adieraziz
    status_object = {'status': {'situation': 'Creating'}}
    custom_client.patch_namespaced_custom_object_status(group, microserviceVersion, namespace, microservicePlural,
                                                        microservice_body['metadata']['name'], status_object)


def create_service(microsvcObject, appObject):
    # Zerbitzuaren objektua sortzen dugu
    serviceObject = utils.service_object(microserviceInfo=microsvcObject, appName=appObject['metadata']['name'])
    # Kuberneteseko APIarekin, zerbitzua sisteman hedatzen dugu
    coreAPI = client.CoreV1Api()
    coreAPI.create_namespaced_service(namespace, serviceObject)


def addFlowInfo(microsvcObject, appObject):
    # Metodo honi esker, hurrengo mikrozerbitzuari buruzko informazio oraingo mikrozerbitzuari gehituko zaio
    if "outPort" in microsvcObject:  # bakarrik irteera badu osotu beharko da mikrozerbitzuaren informazioa
        currentMicrosvcOutPort = microsvcObject['outPort']['name']
        nextMicrosvcInPort = getChannelPort(appObject, currentMicrosvcOutPort, 'from')
        nextMicrosvcObject = getMicrosvcObjectByPortName(appObject, nextMicrosvcInPort, 'inPort')

        # Datu guztiak edukita, mikrozerbitzuari informazio berria gehi daiteke
        microsvcObject['output'] = nextMicrosvcObject['name'] + '-' + \
                                   appObject['metadata']['name']  # Kubernetesen mikrozerbitzuen izena beraiena
        # gehi aplikazioarena da, bakarra izateko
        microsvcObject['output_port'] = nextMicrosvcObject['inPort']['number']

    return microsvcObject


def getMicrosvcObjectByPortName(appObject, portName, portType):
    for microsvc in appObject['spec']['microservices']:
        if portType in microsvc:
            if microsvc[portType]['name'] == portName:
                return microsvc
    return None


def getChannelPort(appObject, portName, portType):
    for channel in appObject['spec']['channels']:
        if portType == "from" and channel['from'] == portName:
            return channel['to']
        if portType == "to" and channel['to'] == portName:
            return channel['from']
    return None


if __name__ == '__main__':
    controller()
