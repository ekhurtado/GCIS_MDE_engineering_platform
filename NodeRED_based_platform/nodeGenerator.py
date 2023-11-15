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
    print("Choose one of the following options to include the component model:")
    print("\t\t -> 1: Enter the component model as a file.")
    print("\t\t -> 2: Enter the component model directly as a plain text.")
    print("\t\t -> 3: Exit the program.")
    while True:
        selectedOption = int(input("Enter the number of the option: "))
        if 1 <= selectedOption <= 3:
            break
        else:
            print("The option introduced is not correct, please reintroduce it.")
    print(selectedOption)
    match selectedOption:
        case 1:
            window = Tk()
            window.eval('tk::PlaceWindow . center')  # Leihoa pantaila erdian irekitzeko
            window.lift()
            window.attributes("-topmost", True)  # Leihoa pantailan erakusteko
            window.after_idle(window.attributes, '-topmost', False)
            Tk().withdraw()
            archivo_xml = askopenfilename(filetypes=[("XML files", "*.xml")], title="Select component model")
            with open(archivo_xml,
                      "r") as archivo:
                # Lee el contenido del archivo y almacénalo en una cadena
                content = archivo.read()
            window.destroy()
            return content
        case 2:
            print("Copy the component model and paste it here (end by pressing Enter on an empty line):")
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
            print("Option not available.")


'''
---------------------------------------------
Saxonche liburutegiarekin erlazionatutako metodoak
---------------------------------------------
'''


def checkComponentMetaModel(componentXML):
    result = False
    while not result:
        xmlschema_doc = etree.parse("../Meta_models/Component.xsd")
        xmlschema = etree.XMLSchema(xmlschema_doc)

        some_file_or_file_like_object = BytesIO(componentXML.encode('utf-8'))
        xml_doc = etree.parse(some_file_or_file_like_object)
        result = xmlschema.validate(xml_doc)
        if not result:
            print("The XML file entered is not correct, please re-enter it.")
            componentXML = getCompModel()
    return componentXML


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


def getXSLT_transformation(originXML, stylesheetXSLT):
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        document = proc.parse_xml(xml_text=originXML)
        executable = xsltproc.compile_stylesheet(stylesheet_file=stylesheetXSLT)
        output = executable.transform_to_string(xdm_node=document)
        return output


'''
---------------------------------------------
Bestelako metodoak
---------------------------------------------
'''


def getIconFilePath():
    print("Would you like to choose your own icon for the component? In case you don't, it will be assigned the icon "
          "of its category (if it exists) or a default one.")
    print("\t\t -> 1: Yes.")
    print("\t\t -> 2: No.")
    while True:
        selectedOption = int(input("Enter the number of the option: "))
        if 1 <= selectedOption <= 2:
            break
        else:
            print("The option introduced is not correct, please reintroduce it.")
    print(selectedOption)
    match selectedOption:
        case 1:
            window = Tk()
            window.eval('tk::PlaceWindow . center')  # Leihoa pantaila erdian irekitzeko
            window.lift()
            window.attributes("-topmost", True)  # Leihoa pantailan erakusteko
            window.after_idle(window.attributes, '-topmost', False)
            Tk().withdraw()
            icon_file_path = askopenfilename(filetypes=[("PNG files", "*.png")],
                                             title="Select the file for the icon")
            window.destroy()
            return icon_file_path
        case _:
            return None


def copyRelatedIcon(compModelXML, compName):
    category = getCategory(compModelXML)
    iconFilePath = getIconFilePath()

    if not os.path.exists("./" + compName + '/icons'):
        os.makedirs("./" + compName + '/icons')
    if iconFilePath is not None:
        shutil.copy2(iconFilePath, './' + compName + '/icons/')
        updateIconOnHTML(compName, category, iconFilePath)
    else:
        if os.path.isfile('./icons/' + category + '.png'):
            shutil.copy2('./icons/' + category + '.png', './' + compName + '/icons/' + category + '.png')
        else:
            shutil.copy2('./customNode/icons/fog_component.png', './' + compName + '/icons/fog_component.png')
            updateIconOnHTML(compName, category, './icons/fog_component.png')


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
    with open("customNode/package.json", "r") as file:
        # Lee el contenido del archivo y almacénalo en una cadena
        configFileContent = file.read()
    return configFileContent.replace("<COMP_NAME>", compName)


def createFile(content, fileName):
    f = open(fileName, 'w')
    f.write(content)
    f.close()


def main():
    compModelXML = getCompModel()
    print("Before the process begins, it will be verified whether the model of components introduced is correct..")
    compModelXML = checkComponentMetaModel(compModelXML)

    print("As the component model is correct, the necessary files will be obtained to obtain a NodeRED node. A folder "
          "will be created to store those files..")
    compName = getCompName(compModelXML)
    if not os.path.exists("./" + compName):
        os.makedirs("./" + compName)

    print("First of all, the web view will be generated.")
    webViewContent = getXSLT_transformation(compModelXML, './customNode/webView.xslt')
    createFile(webViewContent, compName + '/' + compName + '.html')

    print("Then, the functional part will be generated.")
    functionalityContent = getXSLT_transformation(compModelXML, './customNode/functionalPart.xslt')
    createFile(functionalityContent, compName + '/' + compName + '.js')

    print("Finally, configuration file will be generated.")
    configFileContent = getConfigurationFile(compName)
    createFile(configFileContent, compName + '/package.json')

    # Azkenik, ikonoa karpetara kopiatuko dugu
    copyRelatedIcon(compModelXML, compName)


main()
