from lxml import etree

# Cargar el archivo XML de origen
# arbol_xml = etree.parse("C:\\Users\\ekait\\OneDrive - UPV EHU\\Documentos\\INCAR\\TFM\\Recursos\\ejemplo_componente.xml")
arbol_xml = etree.parse("C:\\Users\\\839073\\Downloads\\ejemplo_componente.xml")

# Cargar la plantilla XSLT desde un archivo
plantilla_xslt = etree.parse("../txantiloiak/webView.xslt")
plantilla_xslt = etree.parse("../txantiloiak/functionalPart.xslt")

# Crear un transformador XSLT
transformador = etree.XSLT(plantilla_xslt)

# Aplicar la transformación al árbol XML
resultado = transformador(arbol_xml)

# Obtener el resultado de la transformación como un string
resultado_string = str(resultado)

# Imprimir el resultado
print(resultado_string)
