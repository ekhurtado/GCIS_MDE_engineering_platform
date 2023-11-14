# Node-RED-based platform

This folder contains the entire Node-RED-based platform code. The organization of this folder is as follows:

  - [customNode](https://github.com/ekhurtado/GCIS_MDE_methodology/tree/main/IDE_platform/customNode): This presents the resources needed to create custom nodes for the Node-RED platform. These include:
    - [webView.xslt](https://github.com/ekhurtado/GCIS_MDE_methodology/blob/main/IDE_platform/customNode/webView.xslt): XSLT file to create the custom nodes visual part using M2T transformations.
    - [functionalPart.xslt](https://github.com/ekhurtado/GCIS_MDE_methodology/blob/main/IDE_platform/customNode/functionalPart.xslt): XSLT file to create the custom nodes functional part using M2T transformations.
  - [nodeGenerator.py](https://github.com/ekhurtado/GCIS_MDE_methodology/blob/main/IDE_platform/nodeGenerator.py): Program for the automatic creation of custom nodes. By passing a XML model of the component, it will automatically create all the custom node files and store them in a folder located where the program is running.
  - [appModel_utils.js](https://github.com/ekhurtado/GCIS_MDE_methodology/blob/main/IDE_platform/appModel_utils.js): File that encapsulates the methods used by the nodes at runtime to create the application model automatically.
