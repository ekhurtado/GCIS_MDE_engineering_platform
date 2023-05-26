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

# Osagai mailaren informazioa
componentVersion = "v1alpha1"
componentPlural = "components"


def controller():
    # Lehenik eta behin, klusterraren konfigurazio fitxategia
    config.load_kube_config(os.path.join("../clusterConfiguration/k3s.yaml"))

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
        time.sleep(2)  # 2 segundo itxaroten dugu ondo sortu dela ziurtatzeko
        print("Aplikazioentzako CRDa sortu da.")
    except urllib3.exceptions.MaxRetryError as e:
        print("KONEXIO ERROREA!")
        print("Baliteke k3s.yaml fitxategiko IP helbide nagusia zuzena ez izatea")
        controller()
    except Exception as e:
        if "Reason: Conflict" in str(e):
            print("Aplikazioentzako CRDa jada existitzen da, begirale metodo pasatzen...")
        elif "No such file or directory" in str(e):
            print("Ezin izan da aplikazioaren definizioaren fitxategia aurkitu.")
            sys.exit()  # Kasu honetan, programa bukatzen da, fitxategi egokia sar ezazu, eta birrabiarazi

    # CRDa sisteman egonda, aplikazioen begiralera pasatuko gara
    watcher(custom_client)


def watcher(custom_client):
    watcher = watch.Watch()  # Begiralea aktibatzen dugu
    startedTime = pytz.utc.localize(datetime.datetime.utcnow())  # Kontroladorearen hasiera data lortzen da

    for event in watcher.stream(custom_client.list_namespaced_custom_object, group, version, namespace, plural):
        print('Aplikazioen gertaera berria.')
        object = event['object']
        eventType = event['type']

        creationTime = parser.isoparseobjeto(['metadata']['creationTimestamp'])
        if creationTime < startedTime:
            print("Gerteara zaharkitua da")
            continue

        # Gertaeraren objektua edukita, bere motaren arabera beharrezko jarduerak exekutatuko dira
        print("Gertaera berria: ", "Gertaera ordua: ",
              datetime.datetime.now(), "Gertaera mota: ", eventType, "Objektuaren izena: ", object['metadata']['name'])

        match eventType:
            case "ADDED":
                # Aplikazio berria da
                # Aplikazioarekin erlazionatutako gertaera sortzen dugu, abisatuz aplikazio berria sortu dela
                eventObject = utils.customResourceEventObject(action='Created', CR_type="Application",
                                                              CR_object=object,
                                                              message='Aplikazio berria zuzen sortu da.',
                                                              reason='Created')
                eventAPI = client.CoreV1Api()
                eventAPI.create_namespaced_event("default", eventObject)

                # Lógica para llevar el recurso al estado deseado.
                deploy_application(object, custom_client)
            case "DELETED":
                delete_application(object, custom_client)
            case "MODIFIED":
                check_modifications(object, custom_client)
            case _:  # default case
                pass


def deploy_application(appObject, custom_client):
    # Hasi aurretik, aplikazioaren egoera eguneratzeko gertaera sortzen dugu
    eventObject = utils.customResourceEventObject(action='Deploy', CR_type="Application",
                                                  CR_object=appObject,
                                                  message='Aplikazioaren hedapen hasita.',
                                                  reason='Deploying')
    eventAPI = client.CoreV1Api()
    eventAPI.create_namespaced_event("default", eventObject)

    # Ondoren, aplikazioaren objektuaren egoera atala sortzen dugu, adieraziz oraindik es dela osagairik sortu.
    num_components = len(appObject['spec']['components'])
    status_object = {'status': {'components': [0] * num_components, 'ready': "0/" + str(num_components)}}
    for i in range(int(num_components)):
        status_object['status']['components'][i] = {'name': appObject['spec']['components'][i]['name'],
                                                    'status': "Creating"}
    custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                        appObject['metadata']['name'], status_object)

    # Orain, osagai bakoitza sortuko dugu
    for comp in appObject['spec']['components']:

        # Lehenik eta behin, beste osagaiek aztertzen ari garen osagaiarekin komunikatu behar badira, Kubernetesen
        # zerbitzu deituriko bat sortu beharra dago, osagaia eskuragarri egiteko
        if 'inPort' in comp:
            create_service(custom_client, comp, appObject)

        # Orain, osagaia bera sortu daiteke
        create_component(custom_client, comp, appObject)


def delete_application(appObject, custom_client):  # TODO konprobatu funtzionatzen duela
    # Aplikazioaren osagai guztiak ezabatuko dira
    for comp in appObject['spec']['components']:
        custom_client.delete_namespaced_custom_object(group, componentVersion, namespace, componentPlural,
                                                      comp['name'] + '-' + appObject['metadata']['name'])


def check_modifications(appObject, custom_client):
    eventAPI = client.CoreV1Api()  # Gertaerekin lan egiteko APIa lortzen dugu

    # Lehenik, aztertuko da nor izan den aplikazio objektua aldatu duena
    lastManager = appObject['metadata']['managedFields'][len(appObject['metadata']['managedFields']) - 1]['manager']
    if "component" in lastManager:
        # Bakarrik aplikazioaren barruko osagaiak alda dezakete aplikazioaren objektua, zehazki egoera atala
        # Aldaketaren arduradunatik osagaiaren izena lortzen dugu
        componentName = lastManager.replace('component-', '')
        componentName = componentName.replace('-' + appObject['metadata']['name'], '')

        # Egoera atala aldatu denez, abiarazitako osagaiak aztertuko dira
        runningCount = 0
        for i in range(len(appObject['status']['components'])):
            if appObject['status']['components'][i]['status'] == "Running":
                runningCount += 1

                if appObject['status']['components'][i]['name'] == componentName:
                    # Mezua bidali duen osagaia abiarazita badago, gertaera horren berri emango dugu
                    eventObject = utils.customResourceEventObject(action='Created', CR_type="Application",
                                                                  CR_object=appObject,
                                                                  message=componentName + ' osagaia zuzen abiarazita.',
                                                                  reason='Deployed')
                    eventAPI.create_namespaced_event("default", eventObject)

        # Abiarazitako osagai guztiak aztertuta, baten bat abiarazita badago, egoera atala eguneratuko da
        if runningCount != 0:
            appObject['status']['ready'] = str(runningCount) + "/" + appObject['status']['ready'].split("/")[1]

            if runningCount == len(appObject['status']['components']):
                # Osagai guztiak abiarazita badaude, gertaera horren berri emango dugu
                eventObject = utils.customResourceEventObject(action='Deployed', CR_type="Application",
                                                              CR_object=appObject,
                                                              message='Osagai guztiak zuzen abiarazita.',
                                                              reason='Running')
                eventAPI.create_namespaced_event("default", eventObject)

        # Bete diren aldaketekin, aplikazioaren egoera atala eguneratzen da
        custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                            appObject['metadata']['name'],
                                                            {'status': appObject['status']},
                                                            field_manager=appObject['metadata']['name'])


def create_component(custom_client, compObject, appObject):  # TODO konprobatu funtzionatzen duela

    # Osagaiari beharrezko informazio gehitu diogu (adibidez, hurrengo osagaiarekin komunikatzeko datuak)
    compObject = addFlowInfo(compObject, appObject)
    # Osagaiaren objetua eraikitzen da
    component_body = utils.component_object(componentInfo=compObject, appName=appObject['metadata']['name'])
    # Osagai berria sortzen da
    custom_client.create_namespaced_custom_object(group, componentVersion, namespace, componentPlural, component_body)

    # Behin osagaiaren sorkuntza eskaera betez, bere objektuaren egoera atala eguneratuko da, aurkeztuz sortzen ari dela
    status_object = {'status': {'situation': 'Creating'}}
    custom_client.patch_namespaced_custom_object_status(group, componentVersion, namespace, componentPlural,
                                                        component_body['metadata']['name'], status_object)


def create_service(compObject, appObject):
    # Zerbitzuaren objektua sortzen dugu
    serviceObject = utils.service_object(componentInfo=compObject, appName=appObject['metadata']['name'])
    # Kuberneteseko APIarekin, zerbitzua sisteman hedatzen dugu
    coreAPI = client.CoreV1Api()
    coreAPI.create_namespaced_service(namespace, serviceObject)


def addFlowInfo(compObject, appObject):
    # Metodo honi esker, hurrengo osagaiari buruzko informazio gehituko diogu oraingo osagaiari
    if "outPort" in compObject:  # bakarrik irteera badu osotu beharko dugu osagaiaren informazioa
        currentCompOutPort = compObject['outPort']['name']
        nextCompInPort = getChannelPort(appObject, currentCompOutPort, 'from')
        nextCompObject = getCompObjectByPortName(appObject, nextCompInPort, 'inPort')

        # Datu guztiak edukita, osagaiari informazio berria gehi dezakegu
        compObject['output'] = nextCompObject['name'] + '-' + appObject['name']  # Kubernetesen osagaien izena beraiena
        # gehi aplikazioarena da, bakarra izateko
        compObject['output_port'] = nextCompObject['inPort']['number']

    return compObject


def getCompObjectByPortName(appObject, portName, portType):
    for comp in appObject['components']:
        if comp[portType]['name'] == portName:
            return comp
    return None


def getChannelPort(appObject, portName, portType):
    for channel in appObject['channels']:
        if portType == "from" and channel['from'] == portName:
            return channel['to']
        if portType == "to" and channel['to'] == portName:
            return channel['from']
    return None


if __name__ == '__main__':
    controller()
