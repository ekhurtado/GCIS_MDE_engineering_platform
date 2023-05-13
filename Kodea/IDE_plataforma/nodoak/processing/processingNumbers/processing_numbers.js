const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ProcessingNumbers";
const codePath = "gcr.io/gcis/processing-numbers:latest";

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.selectedPortNumber = config.portnumber;
        this.selectedStepSize = config.stepsize;
        this.selectedMultiplier = config.multiplier;
        var node = this;
        
        node.on('input', function(msg) {

            if (node.function === "") {
                node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
            } else {

                // Funtzionalitate guztien informazioa betetzen dugu
                // --------------------
                const allFunctionsInfo= [
                    increaseValueInfo = new FunctionInfo("IncreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
                    decreaseValueInfo = new FunctionInfo("DecreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
                    multiplyValueInfo = new FunctionInfo("MultiplyValue", "HTTP", "HTTP", "TNumber", "TNumber", "multiplier"),
                ]

                // Hautatutako funtzionalitatearen informazioa lortzen dugu
                // --------------------
                let selectedFunctionInfo;
                let selectedCustomizationValue;
                for (const funcObj in allFunctionsInfo) {
                    if (node.function === allFunctionsInfo[funcObj].name) {
                        selectedFunctionInfo = allFunctionsInfo[funcObj];
                        if (node.function === "IncreaseValue" || node.function === "DecreaseValue") {
                            if (node.selectedStepSize === -1) {
                                node.error("Ez da urrats-tamainarik aukeratu. Sar ezazu baliodun zenbaki bat, mesedez.");
                                return;
                            } else
                                selectedCustomizationValue = node.selectedStepSize;
                        } else {
                            if (node.selectedMultiplier === -1) {
                                node.error("Ez da biderkatzailerik aukeratu. Sar ezazu baliodun zenbaki bat, mesedez.");
                                return;
                            } else
                                selectedCustomizationValue = node.selectedMultiplier;

                        }
                    }
                }

                // Mikrozerbitzu berriaren informazioa eraikitzen dugu
                // --------------------
                const newMicroservice = createNewMicroservice(componentName, codePath, selectedFunctionInfo, node.selectedPortNumber);
                // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
                newMicroservice.$.customization = `{${selectedFunctionInfo.customizationName}: ${selectedCustomizationValue}}`;


                // Aurreko osagaiak bidalitako aplikazio-eredua lortzen dugu
                // --------------------
                let appModelXML;    // XML aplikazio-eredu eguneratua gordetzeko objektua
                xml2js.parseString(msg, function (err, result) {
                    // Fog aplikazio-ereduaren mikrozerbitzuen zerrendan, berria sartu
                    let microserviceList = result.Application.Microservice;
                    microserviceList.push(newMicroservice);

                    // Fog aplikazio-ereduaren kanalen zerrenda eguneratu eta berria sartu
                    let channelList = result.Application.channel;
                    let lastChannel = channelList.pop();
                    lastChannel.$.to = newMicroservice.inPort.$.name;
                    channelList.push(lastChannel, { // azkenengo eta kanal berria sartzen ditugu
                        $: {
                            from: newMicroservice.outPort.$.name
                        }
                    });

                    // XML fitxategia sortu
                    appModelXML = builder.buildObject(result);
                });

                // XML aplikazio-eredua hurrengo nodoari bidali
                node.send(appModelXML);
            }


        });
    }

    RED.nodes.registerType("Processing numbers",ProcessingNumbers);
}
