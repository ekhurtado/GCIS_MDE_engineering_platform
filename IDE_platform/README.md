# IDE_plataforma

This folder contains the entire IDE platform code. Since the selected IDE is Node-RED, the organization of this folder is as follows:

  - [customNode](https://github.com/ekhurtado/EkaitzHurtado-MAL/tree/main/Kodea/IDE_plataforma/txantiloiak/customNode): This presents the resources needed to create custom nodes for the Node-RED platform. These include:
    - [webView.xslt](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/webView.xslt): XSLT file to create the custom nodes visual part using M2T transformations.
    - [functionalPart.xslt](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/functionalPart.xslt): XSLT file to create the custom nodes functional part using M2T transformations.
  - [nodeGenerator.py](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/nodeGenerator.py): Program for the automatic creation of custom nodes. By passing a XML model of the component, it will automatically create all the custom node files and store them in a folder located where the program is running.
  - [appModel_utils.js](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/nodeGenerator.py): File that encapsulates the methods used by the nodes at runtime to create the application model automatically.
