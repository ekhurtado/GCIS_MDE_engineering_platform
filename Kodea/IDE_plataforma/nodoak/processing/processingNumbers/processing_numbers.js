const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ProcessingNumbers";
const codePath = "gcr.io/gcis/processing-numbers:latest";

// TODO BORRAR
var appmodelAnterior = "<Application name=\"NumbersProcessing\">\n" +
    "\t\t<Microservice name=\"CreatingNumber\" service=\"NaturalValue\"\n" +
    "\t\t\t\t\t\tcustomization=\"{type: 'random'}\">\n" +
    "\t\t\t<outPort name=\"CreatingNumberOPort\" \n" +
    "\t\t\t\tprotocol=\"HTTP\" dataType=\"TNumber\"/>\n" +
    "\t\t</Microservice>\t\n" +
    "\n" +
    "\t\t\n" +
    "\t\t<channel from=\"CreatingNumbersOPort\"/>" +
    "</Application>\t\n"

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.selectedPortNumber = config.portnumber;
        var node = this;
        
        node.on('input', function(msg) {

            node.error(msg);

            /*

            if (node.function === "") {
                node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
            } else {

                // Funtzionalitate guztien informazioa betetzen dugu
                // --------------------
                const allFunctionsInfo= [
                    increaseValueInfo = new FunctionInfo("IncreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
                    decreaseValueInfo = new FunctionInfo("DecreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
                    multiplyValueInfo = new FunctionInfo("MultiplyValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
                ]

                // Hautatutako funtzionalitatearen informazioa lortzen dugu
                // --------------------
                let selectedFunctionInfo;
                for (const funcObj in allFunctionsInfo) {
                    if (node.function === allFunctionsInfo[funcObj].name)
                        selectedFunctionInfo = allFunctionsInfo[funcObj];
                }

                // Mikrozerbitzu berriaren informazioa eraikitzen dugu
                // --------------------
                const newMicroservice = createNewMicroservice(componentName, codePath, selectedFunctionInfo, node.selectedPortNumber);
                // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
                //newMicroservice.$.customization = `{${selectedFunctionInfo.customizationName}: ${selectedCustomizationValue}}`;


                // Aurreko osagaiak bidalitako aplikazio-eredua lortzen dugu
                // --------------------
                let appModelXML;    // XML aplikazio-eredu eguneratua gordetzeko objektua
                xml2js.parseString(appmodelAnterior, function (err, result) {
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

                msg.appmodel = appModelXML;

                // XML aplikazio-eredua hurrengo nodoari bidali
                node.send(msg);
            }
            */

        });
    }

    RED.nodes.registerType("Processing numbers",ProcessingNumbers);
}
