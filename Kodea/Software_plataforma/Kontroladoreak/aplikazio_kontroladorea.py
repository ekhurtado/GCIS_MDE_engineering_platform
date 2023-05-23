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
                delete_application(object)
            case _:  # default case
                pass


def deploy_application(object, custom_client):
    # TODO
    pass


def delete_application(object):
    # TODO
    pass


if __name__ == '__main__':
    controller()
