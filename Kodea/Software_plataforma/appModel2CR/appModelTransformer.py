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
    print("Aplikazio-eredua sartzeko hautatu ezazu hurrengo aukeretako bat:")
    print("\t\t -> 1: Aplikazio-eredua fitxategi moduan sartu.")
    print("\t\t -> 2: Aplikazio-eredua zuzenean sartu.")
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


def checkApplicationMetaModel(appXML):
    result = False
    while not result:
        xmlschema_doc = etree.parse("../../meta_ereduak/Application.xsd")
        xmlschema = etree.XMLSchema(xmlschema_doc)

        some_file_or_file_like_object = BytesIO(appXML.encode('utf-8'))
        xml_doc = etree.parse(some_file_or_file_like_object)
        result = xmlschema.validate(xml_doc)
        if not result:
            print("Sartutako XML fitxategia ez da zuzena, sar ezazu berriro mesedez.")
            appXML = getAppModel()
    return appXML


def getAppName(originXML):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=originXML)
        xp.set_context(xdm_item=node)
        result = xp.evaluate_single('/application/@name')
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
    print("Prozesua hasi aurretik, sartutako aplikazio-eredua zuzena baden konprobatuko da.")
    appModelXML = checkApplicationMetaModel(appModelXML)
    appName = getAppName(appModelXML)

    print("Ereduaren zuzentasuna konprobatuta, Custom Resource transformazioa lortuko da.")
    customResourceContent = getXSLT_transformation(appModelXML, 'cr_transformer.xslt')
    createFile(customResourceContent, './' + appName + '.yaml')


main()
