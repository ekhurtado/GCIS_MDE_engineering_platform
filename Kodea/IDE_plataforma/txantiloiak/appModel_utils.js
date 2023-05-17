// FITXATEGI HONEK APLIKAZIO-EREDUA SORTZEKO OBJEKTU ETA FUNTZIO ERABILGARRIAK BILTZEN DITU
// ---------------------

// Fitxategiak irakurtzeko liburutegia
const fs = require('fs');

// XML fitxategiekin lan egiteko liburutegiak
const xml2js = require('xml2js');
const builder = new xml2js.Builder();

// XSD fitxategiekin lan egiteko liburutegia
const validatorXSD = require('xsd-schema-validator');


// Funtzionalitateen informazio gordetzeko klasea
class FunctionInfo {
    constructor(name, inProtocol, outProtocol, inDataType, outDataType, customizationName) {
        this.name = name;
        this.portName = name;
        this.inProtocol = inProtocol;
        this.outProtocol = outProtocol;
        this.inDataType = inDataType;
        this.outDataType = outDataType;
        this.customizationName = customizationName;
    }
}

// Lehenengo mikrozerbitzua sortzeko (bakarrik irteerak dituena)
function createFirstMicroservice(componentName, codePath, selectedFunctionInfo) {
    return {
        $ : {   // $ jarri behar da mikrozerbitzuen zerrendan sartutakoan "Microservice" objektu gisa hartzeko
            name: componentName,
            service: selectedFunctionInfo.name,
            image: codePath
        },
        outPort: {
            $: {
                name: selectedFunctionInfo.portName + 'OPort',
                protocol: selectedFunctionInfo.outProtocol,
                dataType: selectedFunctionInfo.outDataType
            }
        }
    }
}

// Sarrerak eta irteerak dituen mikrozerbitzuak sortzeko (erdikoak)
function createNewMicroservice(componentName, codePath, selectedFunctionInfo, selectedPortNumber) {
    return {
        $ : {   // $ jarri behar da mikrozerbitzuen zerrendan sartutakoan "Microservice" objektu gisa hartzeko
            name: componentName,
            service: selectedFunctionInfo.name,
            image: codePath
        },
        inPort: {
            $: {
                name: selectedFunctionInfo.portName + 'IPort',
                protocol: selectedFunctionInfo.inProtocol,
                dataType: selectedFunctionInfo.inDataType,
                number: selectedPortNumber
            }
        },
        outPort: {
            $: {
                name: selectedFunctionInfo.portName + 'OPort',
                protocol: selectedFunctionInfo.outProtocol,
                dataType: selectedFunctionInfo.outDataType
            }
        }
    }
}

// Azkenengo mikrozerbitzua sortzeko (bakarrik sarrerak dituena)
function createLastMicroservice(componentName, codePath, selectedFunctionInfo, selectedPortNumber) {
    return {
        $ : {   // $ jarri behar da mikrozerbitzuen zerrendan sartutakoan "Microservice" objektu gisa hartzeko
            name: componentName,
            service: selectedFunctionInfo.name,
            image: codePath
        },
        inPort: {
            $: {
                name: selectedFunctionInfo.portName + 'IPort',
                protocol: selectedFunctionInfo.inProtocol,
                dataType: selectedFunctionInfo.inDataType,
                number: selectedPortNumber
            }
        }
    }
}

function addMicroServiceToModel(stringModel, newMicroservice, lastComponent) {
    let appModelXML;    // XML aplikazio-eredu eguneratua gordetzeko objektua
    xml2js.parseString(stringModel, function (err, result) {
        // Fog aplikazio-ereduaren mikrozerbitzuen zerrendan, berria sartu
        let microserviceList = result.application.microservice;
        microserviceList.push(newMicroservice);

        // Fog aplikazio-ereduaren kanalen zerrenda eguneratu eta berria sartu
        let channelList = result.application.channel;
        let lastChannel = channelList.pop();
        lastChannel.$.to = newMicroservice.inPort.$.name;
        channelList.push(lastChannel);
        if (lastComponent === false) {  // bakarrik gehituko da azkenengo osagaia ez bada
            channelList.push({ // azkenengo eta kanal berria sartzen ditugu
                $: {
                    from: newMicroservice.outPort.$.name
                }
            });
        }

        // XML fitxategia sortu
        appModelXML = builder.buildObject(result);
    });
    return appModelXML;
}

function checkApplicationMetaModel(appModelXML) {


    // Read de XSD Schema
    const xsdPath = '/data/node_modules/Application.xsd'
    let xsdContent = fs.readFile(xsdPath, 'utf8', (err, xsdContent) => {
        if (err) {
            console.error('Error reading XSD file:', err);
            return;
        } else
            return xsdContent;
    });

    // return xsdContent;
    // const path = require('path');
    // return path.resolve(__filename);
    //
    // // Validate XML against XSD
    let resultado;
    validatorXSD.validateXML(appModelXML, './Application.xsd', function (err, result) {
        console.error(result);
        //     if (result.valid) {
        //         console.log('XML is valid against XSD.');
        //     } else {
        //         console.log('XML is not valid against XSD.');
        //         console.log('Validation errors:', result.errors);
        //     }
            resultado = result;
        });
    return resultado;
}

module.exports = { FunctionInfo, createFirstMicroservice, createNewMicroservice,
    createLastMicroservice, addMicroServiceToModel, checkApplicationMetaModel } // Export class