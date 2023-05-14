# XML fitxategia irakurtzeko liburutegia
import xml.etree.ElementTree as ET

# Fitxategiak aukeratzeko liburutegia
from tkinter import Tk
from tkinter.filedialog import askopenfilename


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
        Tk()
        Tk().withdraw()
        archivo_xml = askopenfilename(filetypes=[("Archivos XML", "*.xml")])
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


def main():
    print("Kaixo! Ongi etorri aplikazio-eredua Kuberneteseko Custom Resource elementuan transformatzeko kodera.")
    appModelObject = getAppModel()
    if appModelObject is not None:
        appName = appModelObject.getroot().attrib.get("name")
        print("APP NAME: " + appName)
        for app in appModelObject.iter("Microservice"):
            print(f"Etiqueta: {app.tag}")
            print(f"Texto: {app.attrib}")
        # for element in appModelObject.iter():
        #     print(f"Etiqueta: {element.tag}")
        #     print(f"Texto: {element.text}")
        #     print(f"Texto: {element.attrib}")


main()
