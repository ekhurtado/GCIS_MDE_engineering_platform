const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createLastMicroservice} = require('../appModel_utils');

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
    function ShowNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.selectedPortNumber = config.portnumber;
        var node = this;
        
        node.on('input', function(msg) {

            if (node.function === "") {
                node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
            } else {

                // Funtzionalitate guztien informazioa betetzen dugu
                // --------------------
                const allFunctionsInfo= [
                    consoleDisplay = new FunctionInfo("ConsoleDisplay", "HTTP", null, "TNumber", null, null),
                    saveTXT = new FunctionInfo("SaveTXT", "HTTP", null, "TNumber", null, "filename"),
                    saveCSV = new FunctionInfo("SaveCSV", "HTTP", null, "TNumber", null, "filename"),
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
                const newMicroservice = createLastMicroservice(componentName, codePath, selectedFunctionInfo, node.selectedPortNumber);
                // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
                //newMicroservice.$.customization = `{${selectedFunctionInfo.customizationName}: ${selectedCustomizationValue}}`;


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
                    channelList.push(lastChannel);

                    // XML fitxategia sortu
                    appModelXML = builder.buildObject(result);
                });

                // XML aplikazio-eredua hurrengo nodoari bidali
                node.warn(appModelXML);
                // node.done();
            }


        });
    }

    RED.nodes.registerType("Show numbers",ShowNumbers);
}
