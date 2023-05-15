const xml2js = require('xml2js');
const builder = new xml2js.Builder();

// FITXATEGI HONEK APLIKAZIO-EREDUA SORTZEKO OBJEKTU ETA FUNTZIO ERABILGARRIAK BILTZEN DITU


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
        let microserviceList = result.Application.Microservice;
        microserviceList.push(newMicroservice);

        // Fog aplikazio-ereduaren kanalen zerrenda eguneratu eta berria sartu
        let channelList = result.Application.channel;
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

module.exports = { FunctionInfo, createFirstMicroservice, createNewMicroservice, createLastMicroservice, addMicroServiceToModel } // Export class