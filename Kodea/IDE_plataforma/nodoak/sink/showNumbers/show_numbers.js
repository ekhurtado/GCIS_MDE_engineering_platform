const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createLastMicroservice} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ShowNumbers";
const codePath = "gcr.io/gcis/show-numbers:latest";

module.exports = function(RED) {
    function ShowNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.selectedPortNumber = config.portnumber;
        this.selectedFileName = config.filename;
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
                let selectedCustomizationValue = "";
                for (const funcObj in allFunctionsInfo) {
                    if (node.function === allFunctionsInfo[funcObj].name) {
                        selectedFunctionInfo = allFunctionsInfo[funcObj];
                        if (node.function === "SaveTXT" || node.function === "SaveCSV") {
                            if (node.selectedFileName === "") {
                                node.error("Ez duzu fitxategi izenik zehaztu. Mesedez, zehaztu ezazu.");
                                return;
                            } else
                                selectedCustomizationValue = node.selectedFileName;
                        }
                    }
                }

                // Mikrozerbitzu berriaren informazioa eraikitzen dugu
                // --------------------
                const newMicroservice = createLastMicroservice(componentName, codePath, selectedFunctionInfo, node.selectedPortNumber);
                // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
                if (selectedCustomizationValue !== "")
                    newMicroservice.$.customization = `{${selectedFunctionInfo.customizationName}: '${selectedCustomizationValue}'}`;


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
            }


        });
    }

    RED.nodes.registerType("Show numbers",ShowNumbers);
}
