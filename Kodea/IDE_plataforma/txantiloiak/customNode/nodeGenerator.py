# Kode honek XML osagai-eredua edukita, Node-RED tresnarako prest dagoen nodo pertsonalizatua lortzeko beharrezko fitxategiak sortzen ditu
import os
import shutil
from io import BytesIO

# Fitxategiak aukeratzeko liburutegia
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# XML, XSLT eta XSD fitxategiekin lan egiteko liburutegiak
from saxonche import *
from lxml import etree

'''
---------------------------------------------
Component Model-ekin erlazionatutako metodoak
---------------------------------------------
'''


def getCompModel():
    print("Osagai-eredua sartzeko hautatu ezazu hurrengo aukeretako bat:")
    print("\t\t -> 1: Osagai-eredua fitxategi moduan sartu.")
    print("\t\t -> 2: Osagai-eredua zuzenean sartu.")
    print("\t\t -> 3: Programatik irten.")
    while True:
        selectedOption = int(input("Aukera zenbakia sar ezazu: "))
        if 1 <= selectedOption <= 3:
            break
        else:
            print("Sartutako aukera ez da zuzena, sar ezazu berriro, mesedez.")
    print(selectedOption)
    match selectedOption:
        case 1:
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
            window.destroy()
            return content
        case 2:
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
        case 3:
            exit()
        case _:
            print("Aukera ez eskuragarria.")


'''
---------------------------------------------
Saxonche liburutegiarekin erlazionatutako metodoak
---------------------------------------------
'''


def checkComponentMetaModel(componentXML):
    result = False
    while not result:
        xmlschema_doc = etree.parse("../../../meta_ereduak/Component.xsd")
        xmlschema = etree.XMLSchema(xmlschema_doc)

        some_file_or_file_like_object = BytesIO(componentXML.encode('utf-8'))
        xml_doc = etree.parse(some_file_or_file_like_object)
        result = xmlschema.validate(xml_doc)
        if not result:
            print("Sartutako XML fitxategia ez da zuzena, sar ezazu berriro mesedez.")
            componentXML = getCompModel()
    return componentXML


def getCompName(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/component/@name')
        return str.lower(result.string_value)


def getCategory(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/component/@category')
        return result.string_value


def getXSLT_transformation(originXML, stylesheetXSLT):
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        document = proc.parse_xml(xml_text=originXML)
        # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/webView.xslt")
        # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/customNode/functionalPart.xslt")
        executable = xsltproc.compile_stylesheet(stylesheet_file=stylesheetXSLT)
        output = executable.transform_to_string(xdm_node=document)
        return output


'''
---------------------------------------------
Bestelako metodoak
---------------------------------------------
'''


def getIconFilePath():
    print("Osagairako ikono propia aukeratu nahi duzu (defektuz kategoriako ikonoa esleituko zaio)?")
    print("\t\t -> 1: Bai.")
    print("\t\t -> 2: Ez.")
    while True:
        selectedOption = int(input("Aukera zenbakia sar ezazu: "))
        if 1 <= selectedOption <= 2:
            break
        else:
            print("Sartutako aukera ez da zuzena, sar ezazu berriro, mesedez.")
    print(selectedOption)
    match selectedOption:
        case 1:
            window = Tk()
            window.lift()
            window.attributes("-topmost", True)  # Leihoa pantailan erakusteko
            window.after_idle(window.attributes, '-topmost', False)
            Tk().withdraw()
            icon_file_path = askopenfilename(filetypes=[("PNG fitxategiak", "*.png")],
                                             title="Aukeratu ikonorako fitxategia")
            window.destroy()
            return icon_file_path
        case _:
            return None
    # with open(icon_file_path,
    #           "r") as archivo:
    #     # Lee el contenido del archivo y almacénalo en una cadena
    #     content = archivo.read()
    # return icon_file_path


def copyRelatedIcon(compModelXML, compName):
    category = getCategory(compModelXML)
    iconFilePath = getIconFilePath()

    if not os.path.exists("./" + compName + '/icons'):
        os.makedirs("./" + compName + '/icons')
    if iconFilePath is not None:
        shutil.copy2(iconFilePath, './' + compName + '/icons/')
        updateIconOnHTML(compName, category, iconFilePath)
    else:
        shutil.copy2('./icons/' + category + '.png', './' + compName + '/icons/' + category + '.png')


def updateIconOnHTML(compName, category, iconFilePath):
    file = open("./" + compName + "/" + compName + ".html", "r")
    htmlContent = file.read()
    iconDirectory, iconFileName = os.path.split(iconFilePath)
    htmlContent = htmlContent.replace("icon: '" + category + ".png'", "icon: '" + iconFileName + "'")
    file.close()

    file = open("./" + compName + "/" + compName + ".html", "w")
    file.write(htmlContent)
    file.close()


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
    print("Prozesua hasi aurretik, sartutako osagai-eredua zuzena baden konprobatuko da.")
    compModelXML = checkComponentMetaModel(compModelXML)

    print("Osagai-eredua zuzena denez, NodeRED nodo bat lortzeko beharrezko fitxategiak lortuko dira. Fitxategi "
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
