# Fitxategi hau kontroladoreek konpartitzen dituzten metodoak eta objektuak jasotzeko balio du
import datetime
import json
import os
import string
import random

import pytz
import yaml


# --------------------------------
# CRDekin erlazionatutako metodoak
# --------------------------------
def CRD_app():
    path = os.path.abspath(os.path.dirname(__file__))
    # Kodearen fitxategiko karpeta berdinean dagoen "CRD" karpetatik aplikazioen definizioa lortzen da
    rel_path = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "CRD", "application_definition.yaml")
    with open(rel_path, 'r') as stream:
        CRD_applicacion = yaml.safe_load(stream)
    return CRD_applicacion


def CRD_microsvc():
    path = os.path.abspath(os.path.dirname(__file__))
    # Kodearen fitxategiko karpeta berdinean dagoen "CRD" karpetatik mikrozerbitzuen definizioa lortzen da
    rel_path = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "CRD", "microservice_definition.yaml")
    with open(rel_path, 'r') as stream:
        CRD_microservice = yaml.safe_load(stream)
    return CRD_microservice


# ------------------------------------
# Gertaerekin erlazionatutako metodoak
# ------------------------------------
def customResourceEventObject(action, CR_type, CR_object, message, reason):
    create_time = pytz.utc.localize(datetime.datetime.utcnow())

    # Objektuaren informazioa lortzen dugu
    CR_name = CR_object['metadata']['name']
    CR_UID = CR_object['metadata']['uid']
    eventName = CR_object['metadata']['name']

    # Gertaeraren izenaren tamaina ezin da 63 baina handiagoa izan behar
    if len(eventName) > (56 - len(action)):
        eventName = eventName[0:56 - len(action)]

    # Gertaeren izenak ez errepikatzeko, ausazko zati bat gehitzen diogu
    eventName = eventName + '-' + action + '-' + \
                ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

    # Objektuaren izenaren tamaina ezin da 63 baina handiagoa izan behar
    if len(CR_name) > 63:
        CR_name = CR_name[0:62] + ''.join(random.choices(string.ascii_lowercase + string.digits, k=1))

    return {
        'api_Version': 'v1',
        'eventTime': create_time,
        'firstTimestamp': create_time,
        'lastTimestamp': create_time,
        'action': action,
        'involvedObject': {
            'apiVersion': 'ehu.gcis.org/v1alpha1',
            'kind': CR_type,
            'name': CR_name,
            'namespace': 'default',
            'fieldPath': 'Events',
            'uid': CR_UID,
        },
        'kind': 'Event',
        'message': message,
        'reason': reason,
        'reportingComponent': CR_name,
        'reportingInstance': CR_name,
        'type': 'Normal',
        'metadata': {
            'name': eventName,
            'creation_timestamp': create_time
        },
        'source': {
            'component': CR_name
        }
    }


# ------------------------------------
# Osagaiekin erlazionatutako metodoak
# ------------------------------------
def microservice_object(microserviceInfo, appName):
    microservice_resource = {
        'apiVersion': 'ehu.gcis.org/v1alpha1',
        'kind': 'Microservice',
        'metadata': {
            'name': microserviceInfo['name'] + '-' + appName,
            'labels': {
                'applicationName': appName,
                'shortName': microserviceInfo['name']
            }
        },
        'spec': {}
    }

    for infoKey, infoValue in microserviceInfo.items():
        microservice_resource['spec'][infoKey] = infoValue

    if 'output' in microserviceInfo:
        microservice_resource['metadata']['labels']['output'] = microserviceInfo['output']
        microservice_resource['metadata']['labels']['output_port'] = microserviceInfo['output_port']

    return microservice_resource


def service_object(microserviceInfo, appName):
    return {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': microserviceInfo['name'] + '-' + appName,
            'labels': {
                'resource.name': microserviceInfo['name'] + '-' + appName
            }
        },
        'spec': {
            'ports': [{
                'name': microserviceInfo['inPort']['number'],
                # 'name': componentInfo['inPort']['name'],
                'port': int(microserviceInfo['inPort']['number']),
                'targetPort': int(microserviceInfo['inPort']['number'])
            }],
            'selector': {
                'resource.name': microserviceInfo['name'] + '-' + appName
            }
        }
    }


def deploymentObject(microservice, controllerName, appName, microserviceName, **kwargs):
    deployObject = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': microservice['metadata']['name'],
            'labels': {
                'resource.controller': controllerName,
                'resource.name': microservice['metadata']['name'],
                'microservice.name': microserviceName,
                'applicationName': appName
            }
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'resource.name': microservice['metadata']['name']
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'resource.name': microservice['metadata']['name']
                    }
                },
                'spec': {
                    'containers': [{
                        'imagePullPolicy': 'Always',
                        'name': microservice['metadata']['name'],
                        # 'name': componentName,
                        'image': microservice['spec']['image'],
                        'env': [{'name': 'SERVICE',
                                 'value': microservice['spec']['service']}]
                    }],
                    'nodeSelector': {
                        'node-type': 'multipass'
                    },
                    'restartPolicy': 'Always',
                }
            }
        }
    }

    # Osagaiaren izena ezin dute 63 karaktere baino gehiago eduki
    if len(microserviceName) > 63:
        deployObject['spec']['template']['spec']['containers'][0]['name'] = microserviceName[0:63]

    if "customization" in microservice['spec']:
        envVarList = []
        customJSON = json.loads(microservice['spec']['customization'])
        for customAttr, customValue in customJSON.items():
            envVarList.append({'name': str.upper(customAttr), 'value': str(customValue)})
        deployObject['spec']['template']['spec']['containers'][0]['env'] = \
            deployObject['spec']['template']['spec']['containers'][0]['env'] + envVarList

    if "inPort" in microservice['spec']:
        deployObject['spec']['template']['spec']['containers'][0]['ports'] = [{
            'containerPort': int(microservice['spec']['inPort']['number'])
        }]
        deployObject['spec']['template']['spec']['containers'][0]['env'] = \
            deployObject['spec']['template']['spec']['containers'][0]['env'] + [{
                'name': 'INPORT_NUMBER', 'value': microservice['spec']['inPort']['number']
            }]
    if "outPort" in microservice['spec']:
        deployObject['spec']['template']['spec']['containers'][0]['env'] = \
            deployObject['spec']['template']['spec']['containers'][0]['env'] + [
                {'name': 'OUTPUT', 'value': microservice['metadata']['labels']['output']},
                {'name': 'OUTPUT_PORT', 'value': microservice['metadata']['labels']['output_port']},
            ]

    return deployObject
