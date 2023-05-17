# Kode honek XML osagai-eredua edukita, Node-RED tresnarako prest dagoen nodo pertsonalizatua lortzeko beharrezko fitxategiak sortzen ditu
import os, shutil

from saxonche import *

# Fitxategiak aukeratzeko liburutegia
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def getCompModel():
    print("Osagai-eredua sartzeko hautatu ezazu hurrengo aukeretako bat:")
    print("\t\t -> 1: Osagai-eredua fitxategi moduan sartu.")
    print("\t\t -> 2: Osagai-eredua zuzenean sartu.")
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
        with open(archivo_xml,
                  "r") as archivo:
            # Lee el contenido del archivo y almacénalo en una cadena
            content = archivo.read()
        return content
    else:
        print("Osagai-eredua kopia eta hemen itsas ezazu (amaitu Enter sakatuz lerro huts batean):")
        stringAppModel = ''
        while True:

            line = input('''''')
            if line == '':
                break
            else:
                stringAppModel += line + '\n'
        print(stringAppModel)
        return stringAppModel


def getCompName(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/Component/@name')
        return str.lower(result.string_value)


def getCategory(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/Component/@category')
        return result.string_value


def copyRelatedIcon(compModelXML, compName):
    category = getCategory(compModelXML)
    if not os.path.exists("./" + compName + '/icons'):
        os.makedirs("./" + compName + '/icons')
    shutil.copy2('./icons/' + category + '.png', './' + compName + '/icons/' + category + '.png')

def getXSLT_transformation(originXML, stylesheetXSLT):
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        document = proc.parse_xml(xml_text=originXML)
        # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/webView.xslt")
        # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/customNode/functionalPart.xslt")
        executable = xsltproc.compile_stylesheet(stylesheet_file=stylesheetXSLT)
        output = executable.transform_to_string(xdm_node=document)
        return output


def getConfigurationFile(compName):
    with open("./package.json", "r") as file:
        # Lee el contenido del archivo y almacénalo en una cadena
        configFileContent = file.read()
    return configFileContent.replace("<COMP_NAME>", compName)


def createFile(content, fileName):
    f = open(fileName, 'w')
    f.write(content)
    f.close()


def main():
    compModelXML = getCompModel()

    print("Osagai-eredua sartu duzunez, NodeRED nodo bat lortzeko beharrezko fitxategiak lortuko dira. Fitxategi "
          "horiek gordetzeko karpeta bat sortuko da.")
    compName = getCompName(compModelXML)
    if not os.path.exists("./" + compName):
        os.makedirs("./" + compName)

    print("Lehenik eta behin, web-ikuspegia lortuko da.")
    webViewContent = getXSLT_transformation(compModelXML, './webView.xslt')
    createFile(webViewContent, compName + '/' + compName + '.html')

    print("Ondoren, funztionalitaterako fitxategia lortuko da.")
    functionalityContent = getXSLT_transformation(compModelXML, './functionalPart.xslt')
    createFile(functionalityContent, compName + '/' + compName + '.js')

    print("Azkenik, konfigurazio fitxategia lortuko da.")
    configFileContent = getConfigurationFile(compName)
    createFile(configFileContent, compName + '/package.json')

    # Azkenik, ikonoa karpetara kopiatuko dugu
    copyRelatedIcon(compModelXML, compName)


main()
