import datetime
import os
import sys
import time
import pytz
import urllib3
from dateutil import parser
from kubernetes import client, config, watch

import utils

# Mikrozerbitzu mailaren ezaugarrientzako aldagaiak
group = "ehu.gcis.org"
version = "v1alpha1"
namespace = "default"
plural = "microservices"

applicationPlural = "applications"


def controller():
    # Klusterretik kanpo exekutatzen bada, klusterraren konfigurazio fitxategia zehaztu beharko da
    # config.load_kube_config("k3s.yaml")

    # Kontroladorea klusterrean eta Docker edukiontzi baten barruan hedatu badago, kode hau erabili
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    custom_client = client.CustomObjectsApi()  # Custom objektuetarako APIa lortzen da
    client_extension = client.ApiextensionsV1Api()  # CRDekin lan egiteko APIa lortzen da

    # Ondoren, mikrozerbitzuaren CRD sortuta ez badago kontrobatuko da
    try:
        client_extension.create_custom_resource_definition(utils.CRD_microsvc())
        time.sleep(2)  # 2 segundo itxaroten da ondo sortu dela ziurtatzeko
        print("Mikrozerbitzuientzako CRDa sortu da.")
    except urllib3.exceptions.MaxRetryError as e:
        print("KONEXIO ERROREA!")
        print("Baliteke k3s.yaml fitxategiko IP helbide nagusia zuzena ez izatea")
        controller()
    except Exception as e:
        if "Reason: Conflict" in str(e):
            print("Mikrozerbitzuentzako CRDa jada existitzen da, begirale metodora pasatzen...")
        elif "No such file or directory" in str(e):
            print("Ezin izan da mikrozerbitzuaren definizioaren fitxategia aurkitu.")
            sys.exit()  # Kasu honetan, programa bukatzen da, fitxategi egokia sar ezazu, eta birrabiarazi

    # CRDa sisteman egonda, mikrozerbitzuen begiralera pasatuko da
    watcher(custom_client)


def watcher(custom_client):
    watcher = watch.Watch()  # Begiralea aktibatzen da
    startedTime = pytz.utc.localize(datetime.datetime.utcnow())  # Kontroladorearen hasiera data lortzen da

    for event in watcher.stream(custom_client.list_namespaced_custom_object, group, version, namespace, plural):
        print('Mikrozerbitzuen gertaera berria.')
        object = event['object']
        eventType = event['type']

        creationTime = parser.isoparse(object['metadata']['creationTimestamp'])
        if creationTime < startedTime:
            print("Gertaera zaharkitua da")
            continue

        # Gertaeraren objektua edukita, bere motaren arabera beharrezko jarduerak exekutatuko dira
        print("Gertaera berria: ", "Gertaera ordua: ",
              datetime.datetime.now(), "Gertaera mota: ", eventType, "Objektuaren izena: ", object['metadata']['name'])

        match eventType:
            case "ADDED":  # Mikrozerbitzu berria
                # Mikrozerbitzuarekin erlazionatutako gertaera sortzen da, abisatuz mikrozerbitzu berria sortu dela
                eventObject = utils.customResourceEventObject(action='Created', CR_type="Microservice",
                                                              CR_object=object,
                                                              message='The new microservice is correctly created.',
                                                              reason='Created')
                eventAPI = client.CoreV1Api()
                eventAPI.create_namespaced_event("default", eventObject)

                # Mikrozerbitzua abiarazten da
                deploy_microservice(object, custom_client)
            case "DELETED":  # Mikrozerbitzua ezabatuta
                delete_microservice(object)
            case _:  # default case
                pass


def deploy_microservice(microsvcObject, custom_client):
    # Hasteko, mikrozerbitzuaren egoera atala eguneratzen da
    status_object = {'status': {'situation': 'Deploying'}}
    custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                        microsvcObject['metadata']['name'], status_object)

    # Bestalde, egoera horren berri emateko gertaera sortzen da
    eventAPI = client.CoreV1Api()
    eventObject = utils.customResourceEventObject(action='deploying', CR_type="Microservice",
                                                  CR_object=microsvcObject,
                                                  message='Microservice deployment started.',
                                                  reason='Deploying')
    eventAPI.create_namespaced_event("default", eventObject)

    myAppName = microsvcObject['metadata']['labels']['applicationName']  # dagokion aplikazioaren izena jasoko dugu
    shortName = microsvcObject['metadata']['labels']['shortName']  # mikrozerbitzuaren jatorrizko izena lortzen da

    # Hedapen fitxategia lortzen da
    deployment_yaml = utils.deploymentObject(microsvcObject, "microservice-controller", myAppName, shortName)

    # Kuberneteseko APIarekin, mikrozerbitzua sisteman hedatzen da
    appsAPI = client.AppsV1Api()
    appsAPI.create_namespaced_deployment(namespace, deployment_yaml)

    # Deployment objektuaren egoera aztertuko da
    deploymentObject = appsAPI.read_namespaced_deployment_status(deployment_yaml['metadata']['name'], namespace)
    # Ondo hedatu den arte itxaroten da
    availableReplicas = deploymentObject.status.available_replicas
    while availableReplicas is None:
        status_deployment = appsAPI.read_namespaced_deployment_status(deployment_yaml['metadata']['name'], namespace)
        availableReplicas = status_deployment.status.available_replicas

    # Mikrozerbitzua zuzen hedatu dela komunikatzen da
    eventObject = utils.customResourceEventObject(action='deployed', CR_type="Microservice",
                                                  CR_object=microsvcObject,
                                                  message='The microservice has correctly deployed.',
                                                  reason='Running')
    eventAPI.create_namespaced_event("default", eventObject)

    # Mikrozerbitzuaren egoera eguneratzen da, abiarazita dagoela komunikatuz
    status_object = {'status': {'replicas': 1, 'situation': 'Running'}}
    custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                        microsvcObject['metadata']['name'], status_object)

    # Azkenik, erlazionatutako aplikazioaren egoera aldatzen da. Horretarako, aplikazioaren objektua lortzen da,
    # mikrozerbitzuaren informazioa bilatzen da eta informazio berria sartzen da (abiarazita dagoela)
    relatedApp = custom_client.get_namespaced_custom_object_status(group, version, namespace,
                                                                   applicationPlural, myAppName)
    field_manager = 'microservice-' + shortName + '-' + relatedApp['metadata']['name']
    for i in range(len(relatedApp['status']['microservices'])):
        if relatedApp['status']['microservices'][i]['name'] == microsvcObject['spec']['name']:
            relatedApp['status']['microservices'][i]['status'] = "Running"
            custom_client.patch_namespaced_custom_object_status(group, version, namespace,
                                                                applicationPlural, myAppName,
                                                                {'status': relatedApp['status']},
                                                                field_manager=field_manager)
            break


def delete_microservice(microsvcObject):
    # Mikrozerbitzuaren objektua ezabatu denez, berarekin erlazionatutako Deployment-a ere ezabatuko da
    client_deploys = client.AppsV1Api()
    client_deploys.delete_namespaced_deployment(microsvcObject['metadata']['name'], namespace)

    # Gainera, zerbitzuren bat erlazionaturik badu, ere ezabatu beharko da
    if "inPort" in microsvcObject['spec']:
        coreAPI = client.CoreV1Api()
        coreAPI.delete_namespaced_service(microsvcObject['metadata']['name'], namespace)


if __name__ == '__main__':
    controller()
