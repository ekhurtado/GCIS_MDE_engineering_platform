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

module.exports = { FunctionInfo, createFirstMicroservice, createNewMicroservice, createLastMicroservice } // Export class