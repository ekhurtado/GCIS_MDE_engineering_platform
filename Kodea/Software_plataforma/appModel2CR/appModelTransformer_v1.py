import json
import os

# XML fitxategia irakurtzeko liburutegia
import xml.etree.ElementTree as ET

# Fitxategiak aukeratzeko liburutegia
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# YAML fitxategiekin lan egiteko liburutegia
import yaml


def getAppModel():
    print("Aplikazio-eredua sartzeko hautatu ezazu hurrengo aukeretako bat:")
    print("\t\t -> 1: Aplikazio-eredua fitxategi moduan sartu.")
    print("\t\t -> 2: Aplikazio-eredua zuzenean sartu.")
    while True:
        selectedOption = int(input("Aukera zenbakia sar ezazu: "))
        if 1 <= selectedOption <= 2:
            break
        else:
            print("Sartutako aukera ez da zuzena, sar ezazu berriro, mesedez.")
    print(selectedOption)
    if selectedOption == 1:
        window = Tk()
        window.lift()
        window.attributes("-topmost", True)  # Leihoa pantailan erakusteko
        window.after_idle(window.attributes, '-topmost', False)
        Tk().withdraw()
        archivo_xml = askopenfilename(filetypes=[("Archivos XML", "*.xml")], title="Aukeratu fitxategia")
        return ET.parse(archivo_xml)
    else:
        print("Aplikazio-eredua kopia eta hemen itsas ezazu (amaitu Enter sakatuz lerro huts batean):")
        stringAppModel = ''
        while True:

            line = input('''''')
            if line == '':
                break
            else:
                stringAppModel += line + '\n'
        print(stringAppModel)
        try:
            stringAppModelObj = ET.fromstring(stringAppModel)
        except ET.ParseError as e:
            print("Sartutako XMLa ez da zuzena.")
            print(e)
            return None
        return stringAppModelObj


def transformXMLToYAML(appModelXML, appName):

    print("APP NAME: " + appName)
    appModelYAML = {
        'apiVersion': 'ehu.gcis.org/v1alpha1',
        'kind': 'Application',
        'metadata': {
            'name': appName
        },
        'spec': {
            'components': [],
            'channels': []
        }
    }

    for microsvc in appModelXML.iter("Microservice"):
        # Osagaiaren informazio lortuko dugu
        componentInfo = {}
        for key, value in microsvc.attrib.items():
            if value.__contains__("'"):
                value = value.replace("'", '"')
            componentInfo[key] = value

        # Sarrera edo/eta irteera portuen informazioa osagaian sartuko dugu
        for port in microsvc:
            componentInfo[port.tag] = {}
            for key, value in port.attrib.items():
                componentInfo[port.tag][key] = value

        # Osagaiaren informazioa aplikazioan sartzen dugu
        appModelYAML['spec']['components'].append(componentInfo)

    for channel in appModelXML.iter("channel"):
        # Kanalaren informazio lortuko dugu
        channelInfo = {}
        for key, value in channel.attrib.items():
            channelInfo[key] = value
        # Kanalaren informazioa aplikazioan sartzen dugu
        appModelYAML['spec']['channels'].append(channelInfo)

    return appModelYAML


def main():
    print("Kaixo! Ongi etorri aplikazio-eredua Kuberneteseko Custom Resource elementuan transformatzeko kodera.")
    appModelXML = getAppModel()
    if appModelXML is not None:
        appName = appModelXML.getroot().attrib.get("name")
        appName = appName.replace(" ", "_")  # Kubernetes fitxategietarako egiaztapena
        # XML aplikazio-eredutik Custom Resource den YAML aplikazio-eredua lortuko dugu
        appModelYaml = transformXMLToYAML(appModelXML, appName)
        # Aplikazio-eredua YAML formatuan edukita, fitxategian gordeko dugu
        f = open(appName + '_CR.yaml', 'w')
        yaml.dump(appModelYaml, f)
        print("Aplikazio-eredua sortuta. Fitxategia programa honen karpeta berdinean aurki dezakezu:")
        print("\t" + os.path.realpath(f.name))
        f.close()


string = '{"type": "random"}'
# decoded_string = bytes(string, "utf-8").decode("unicode_escape")
# string = string.replace("''", '"')
print(string)
aa = json.loads(string)
main()
