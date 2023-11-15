# Kode honek XML osagai-eredua edukita, Node-RED tresnarako prest dagoen nodo pertsonalizatua lortzeko beharrezko fitxategiak sortzen ditu
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


def getAppModel():
    print("To enter the application model select one of the following options:")
    print("\t\t -> 1: Enter the application model as a file.")
    print("\t\t -> 2: Enter the application model directly as a plain text.")
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
            archivo_xml = askopenfilename(filetypes=[("XML files", "*.xml")], title="Select application model")
            with open(archivo_xml,
                      "r") as archivo:
                # Lee el contenido del archivo y almacénalo en una cadena
                content = archivo.read()
            window.destroy()
            return content
        case 2:
            print("Copy the application model and paste it here (end by pressing Enter on an empty line):")
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


def checkApplicationMetaModel(appXML):
    result = False
    while not result:
        xmlschema_doc = etree.parse("../../Meta_models/Application.xsd")
        xmlschema = etree.XMLSchema(xmlschema_doc)

        some_file_or_file_like_object = BytesIO(appXML.encode('utf-8'))
        xml_doc = etree.parse(some_file_or_file_like_object)
        result = xmlschema.validate(xml_doc)
        if not result:
            print("The XML file entered is not correct, please re-enter it.")
            appXML = getAppModel()
    return appXML


def getAppName(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/Application/@name')
        return str.lower(result.string_value)



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


def createFile(content, fileName):
    f = open(fileName, 'w')
    f.write(content)
    f.close()


def main():
    appModelXML = getAppModel()
    print("Before the process begins, it will be verified whether the model of application introduced is correct..")
    appModelXML = checkApplicationMetaModel(appModelXML)
    appName = getAppName(appModelXML)

    print("Once the integrity of the model is checked, the Custom Resource transformation will be achieved..")
    customResourceContent = getXSLT_transformation(appModelXML, 'appModelTransformer.xslt')
    createFile(customResourceContent, './' + appName + '_delivery.yaml')


main()
