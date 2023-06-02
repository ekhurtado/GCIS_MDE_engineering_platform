const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice, addMicroServiceToModel} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ProcessingNumbers";
const codeName = "gcr.io/gcis/processing-numbers:latest";

module.exports = function(RED) {
    function Functionality(config) {
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
                const newMicroservice = createNewMicroservice(componentName, codeName, selectedFunctionInfo, node.selectedPortNumber);
                // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
                newMicroservice.$.customization = `{'${selectedFunctionInfo.customizationName}': ${selectedCustomizationValue}}`;


                // Aurreko osagaiak bidalitako aplikazio-eredua lortzen dugu
                // --------------------
                let appModelXML = addMicroServiceToModel(msg, newMicroservice, false);

                // XML aplikazio-eredua hurrengo nodoari bidali
                node.send(appModelXML);
            }


        });
    }

    RED.nodes.registerType("Functionality",Functionality);
}
