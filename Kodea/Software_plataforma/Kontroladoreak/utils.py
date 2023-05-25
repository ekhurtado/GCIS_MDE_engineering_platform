# Fitxategi hau kontroladoreek konpartitzen dituzten metodoak eta objektuak jasotzeko balio du
import datetime
import json
import os
import string
from random import random

import pytz
import yaml


# --------------------------------
# CRDekin erlazionatutako metodoak
# --------------------------------
def CRD_app():
    path = os.path.abspath(os.path.dirname(__file__))
    rel_path = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "CRD", "application_definition.yaml")
    with open(rel_path, 'r') as stream:
        CRD_applicacion = yaml.safe_load(stream)
    return CRD_applicacion


def CRD_comp():
    path = os.path.abspath(os.path.dirname(__file__))
    rel_path = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "CRD", "component_definition.yaml")
    with open(rel_path, 'r') as stream:
        CRD_component = yaml.safe_load(stream)
    return CRD_component


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
def component_object(componentInfo, appName):
    component_resource = {
        'apiVersion': 'ehu.gcis.org/v1alpha1',
        'kind': 'Component',
        'metadata': {
            'name': componentInfo['name'] + '-' + appName,
            'labels': {
                'applicationName': appName,
                'shortName': componentInfo['name']
            }
        },
        'spec': {}
    }

    for infoKey, infoValue in componentInfo.items():
        component_resource['spec'][infoKey] = infoValue

    return component_resource


def deploymentObject(component, controllerName, appName, replicas, componentName, **kwargs):
    deployObject = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': component['metadata']['name'],
            'labels': {
                'resource.controller': controllerName,
                'component.name': componentName,
                'applicationName': appName
            }
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'component.name': componentName
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'component.name': componentName
                    }
                },
                'spec': {
                    'containers': [{
                        'imagePullPolicy': 'Always',
                        'name': componentName,
                        'image': component['spec']['image'],
                        'env': [{'name': 'SELECTED_SERVICE',
                                 'value': component['spec']['service']}]
                    }],
                    'nodeSelector': {
                        'node-type': 'multipass'
                    },
                }
            }
        }
    }

    # Osagaiaren izena ezin dute 63 karaktere baino gehiago eduki
    if len(componentName) > 63:
        deployObject['spec']['template']['spec']['containers'][0]['name'] = componentName[0:63]

    if "customization" in component['spec']:
        envVarList = []
        customJSON = json.loads(component['spec']['customization'])
        for customAttr, customValue in customJSON.items():
            envVarList.append({'name': customAttr, 'value': customValue})
        deployObject['spec']['template']['spec']['containers'][0]['env'] = \
            deployObject['spec']['template']['spec']['containers'][0]['env'] + envVarList

    if "inPort" in component['spec']:
        deployObject['spec']['template']['spec']['containers'][0]['env'] = \
            deployObject['spec']['template']['spec']['containers'][0]['env'] + {
                'name': 'INPORT_NUMBER', 'value': component['spec']['inPort']['number']
            }

    return deployObject
