# from lxml import etree
#
# # Cargar el archivo XML de origen
# arbol_xml = etree.parse("C:\\Users\\ekait\\OneDrive - UPV EHU\\Documentos\\INCAR\\TFM\\Recursos\\ejemplo_componente.xml")
# # arbol_xml = etree.parse("C:\\Users\\\839073\\Downloads\\ejemplo_componente.xml")
#
# # Cargar la plantilla XSLT desde un archivo
# plantilla_xslt = etree.parse("../txantiloiak/webView.xslt")
# plantilla_xslt = etree.parse("../txantiloiak/functionalPart.xslt")
# # lxml.x
# # Crear un transformador XSLT
# transformador = etree.XSLT(plantilla_xslt)
#
# # Aplicar la transformación al árbol XML
# resultado = transformador(arbol_xml)
#
# # Obtener el resultado de la transformación como un string
# resultado_string = str(resultado)
#
# # Imprimir el resultado
# print(resultado_string)
import json

from saxonche import *

with PySaxonProcessor(license=False) as proc:

    # with open("C:\\Users\\ekait\\OneDrive - UPV EHU\\Documentos\\INCAR\\TFM\\Recursos\\ejemplo_componente.xml", "r") as archivo:
    with open("C:\\Users\\ekait\\OneDrive - UPV EHU\\Documentos\\INCAR\\TFM\\Recursos\\ejemplo_app.xml", "r") as archivo:
        # Lee el contenido del archivo y almacénalo en una cadena
        contenido = archivo.read()

    xsltproc = proc.new_xslt30_processor()
    document = proc.parse_xml(xml_text=contenido)
    # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/webView.xslt")
    # executable = xsltproc.compile_stylesheet(stylesheet_file="../txantiloiak/customNode/functionalPart.xslt")
    executable = xsltproc.compile_stylesheet(stylesheet_file="../../Software_plataforma/appModel2CR/transformer.xslt")
    output = executable.transform_to_string(xdm_node=document)
    print(output)
