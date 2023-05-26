import datetime
import os
import sys
import time
import pytz
import urllib3
from dateutil import parser

from kubernetes import client, config, watch

import utils

# Osagai mailaren ezaugarrientzako aldagaiak
group = "ehu.gcis.org"
version = "v1alpha1"
namespace = "default"
plural = "components"


# # Osagai mailaren informazioa
# componentVersion = "v1alpha1"
# componentPlural = "components"


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

    # Ondoren, osagaiaren CRD sortuta ez badago kontrobatuko da
    try:
        client_extension.create_custom_resource_definition(utils.CRD_comp())
        time.sleep(2)  # 2 segundo itxaroten dugu ondo sortu dela ziurtatzeko
        print("Osagaientzako CRDa sortu da.")
    except urllib3.exceptions.MaxRetryError as e:
        print("KONEXIO ERROREA!")
        print("Baliteke k3s.yaml fitxategiko IP helbide nagusia zuzena ez izatea")
        controller()
    except Exception as e:
        if "Reason: Conflict" in str(e):
            print("Osagaientzako CRDa jada existitzen da, begirale metodo pasatzen...")
        elif "No such file or directory" in str(e):
            print("Ezin izan da osagaiaren definizioaren fitxategia aurkitu.")
            sys.exit()  # Kasu honetan, programa bukatzen da, fitxategi egokia sar ezazu, eta birrabiarazi

    # CRDa sisteman egonda, osagaien begiralera pasatuko gara
    watcher(custom_client)


def watcher(custom_client):
    watcher = watch.Watch()  # Begiralea aktibatzen dugu
    startedTime = pytz.utc.localize(datetime.datetime.utcnow())  # Kontroladorearen hasiera data lortzen da

    for event in watcher.stream(custom_client.list_namespaced_custom_object, group, version, namespace, plural):
        print('Osagaien gertaera berria.')
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
                # Osagai berria da
                # Osagaiarekin erlazionatutako gertaera sortzen dugu, abisatuz osagai berria sortu dela
                eventObject = utils.customResourceEventObject(action='Created', CR_type="Component",
                                                              CR_object=object,
                                                              message='Osagai berria zuzen sortu da.',
                                                              reason='Created')
                eventAPI = client.CoreV1Api()
                eventAPI.create_namespaced_event("default", eventObject)

                # Lógica para llevar el recurso al estado deseado.
                deploy_component(object, custom_client)
            case "DELETED":
                delete_component(object)
            case _:  # default case
                pass


def deploy_component(compObject, custom_client):
    # Hasteko, osagaiaren egoera atala eguneratzen da
    status_object = {'status': {'situation': 'Deploying'}}
    custom_client.patch_namespaced_custom_object_status(group, version, namespace, plural,
                                                        compObject['metadata']['name'], status_object)

    # Bestalde, egoera horren berri emateko gertaera sortzen da
    eventAPI = client.CoreV1Api()
    eventObject = utils.customResourceEventObject(action='deploying', CR_type="Component",
                                                  CR_object=compObject,
                                                  message='Osagaiaren hedapena hasita.',
                                                  reason='Deploying')
    eventAPI.create_namespaced_event("default", eventObject)

    # TODO konprobatu ea compObject labels informazioa badu, edo objektu osoa lortu behar baden APIarekin
    myAppName = compObject['metadata']['labels']['applicationName']  # dagokion aplikazioaren izena jasoko dugu
    shortName = compObject['metadata']['labels']['shortName']  # osagaiaren jatorrizko izena lortzen da

    # Hedapen fitxategia lortzen da
    deployment_yaml = utils.deploymentObject(compObject, "component-controller", myAppName, shortName)

    # Kuberneteseko APIarekin, osagaia sisteman hedatzen dugu
    appsAPI = client.AppsV1Api()
    appsAPI.create_namespaced_deployment(namespace, deployment_yaml)

    # Busco el status del deployment.
    status_deployment = appsAPI.read_namespaced_deployment_status(deployment_yaml['metadata']['name'], namespace)
    # TODO FALTA DA KONPROBATZEA EA HEDATU DEN (running egoera)

    # Creamos el evento notificando que se ha desplegado el componente
    eventObject = utils.customResourceEventObject(action='deployed', CR_type="Component",
                                                  CR_object=compObject,
                                                  message='Osagaia zuzen hedatu da.',
                                                  reason='Running')
    eventAPI.create_namespaced_event("default", eventObject)

    # TODO FALTA DA OSAGAIAREN STATUS-A ALDATZEA ETA BERE APLIKAZIOARENA BAITA ERE


def delete_component(compObject):  # TODO konprobatu funtzionatzen duela
    # Osagaiaren objektua ezabatu denez, berarekin erlazionatutako Deployment-a ere ezabatuko da
    client_deploys = client.AppsV1Api()
    client_deploys.delete_namespaced_deployment(compObject['metadata']['name'], namespace)


if __name__ == '__main__':
    controller()
