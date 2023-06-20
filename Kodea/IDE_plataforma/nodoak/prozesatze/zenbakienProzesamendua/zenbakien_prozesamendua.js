const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice, addMicroServiceToModel} = require('../appModel_utils.js');

// Osagaiaren aldagaiak
const componentName = "ZenbakienProzesamendua";
const imgBase = "ekhurtado/gcis:zenbakien-prozesamendua";

module.exports = function(RED) {
    function ZenbakienProzesamendua(config) {
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
                    increaseValueInfo = new FunctionInfo("BalioaHanditu", "HTTP", "HTTP", "TZenbaki", "TZenbaki", "custom_urratsa"),
                    decreaseValueInfo = new FunctionInfo("BalioaTxikitu", "HTTP", "HTTP", "TZenbaki", "TZenbaki", "custom_urratsa"),
                    multiplyValueInfo = new FunctionInfo("BalioaBiderkatu", "HTTP", "HTTP", "TZenbaki", "TZenbaki", "custom_biderkatzailea"),
                ]

                // Hautatutako funtzionalitatearen informazioa lortzen dugu
                // --------------------
                let selectedFunctionInfo;
                let selectedCustomizationValue;
                for (const funcObj in allFunctionsInfo) {
                    if (node.function === allFunctionsInfo[funcObj].name) {
                        selectedFunctionInfo = allFunctionsInfo[funcObj];
                        if (node.function === "BalioaHanditu" || node.function === "BalioaTxikitu") {
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
                const newMicroservice = createNewMicroservice(componentName, imgBase, selectedFunctionInfo, node.selectedPortNumber);
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

    RED.nodes.registerType("zenbakienProzesamendua",ZenbakienProzesamendua);
}
