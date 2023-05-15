const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createFirstMicroservice} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "CreatingNumbers";
const codePath = "gcr.io/gcis/creating-numbers:latest";

module.exports = function(RED) {
    function CreatingNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.valuetype = config.valuetype;
        this.firstvalue = config.firstvalue;
        var node = this;

        var RED2 = require.main.require('node-red');
        var miflow = RED2.nodes.getFlow(this.z);    // this.z -> nodoa dagoen fluxuaren IDa
        var appName = miflow.label;

        if (node.function === "") {
            node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
        } else {

            // Funtzionalitate guztien informazioa betetzen dugu
            // --------------------
            const allFunctionsInfo= [
                naturalValueInfo = new FunctionInfo("NaturalValue", null, "HTTP", null, "TNumber", "type,firstvalue"),
                integerValue = new FunctionInfo("IntegerValue", null, "HTTP", null, "TNumber", "type,firstvalue"),
                floatValue = new FunctionInfo("FloatValue", null, "HTTP", null, "TNumber", "type,firstvalue")
            ]

            // Hautatutako funtzionalitatearen informazioa lortzen dugu
            // --------------------
            let selectedFunctionInfo;
            for (const funcObj in allFunctionsInfo) {
                if (node.function === allFunctionsInfo[funcObj].name)
                    selectedFunctionInfo = allFunctionsInfo[funcObj];
            }

            // Customization datuak sartu badira konprobatuko da
            if (node.valuetype === "" || node.firstvalue === -999) {
                node.error("Customization datuak ez dira sartu. Sar ditzazu, mesedez.");
                return;
            }

            // Mikrozerbitzu berriaren informazioa eraikitzen dugu
            // --------------------
            const Microservice = createFirstMicroservice(componentName, codePath, selectedFunctionInfo);
            // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
            Microservice.$.customization = `{` +
                `'${selectedFunctionInfo.customizationName.split(',')[0]}': '${node.valuetype}', ` +
                `'${selectedFunctionInfo.customizationName.split(',')[1]}': ${node.firstvalue}`+
                `}`;

            const channel = {
                $: {
                    from: Microservice.outPort.$.name
                }
            }

            // Lehenengo osagaia izanik, aplikazio-eredua eraikiko dugu
            // --------------------
            let appModelXML = {
                Application: {
                    $: {
                        name: appName, // recogerlo del nombre del flow
                    },
                    Microservice,
                    channel
                }
            }

            // XML fitxategia sortu
            appModelXMLObject = builder.buildObject(appModelXML);

            // XML aplikazio-eredua hurrengo nodoari bidali
            node.send(appModelXMLObject);
        }
    }

    RED.nodes.registerType("Creating numbers",CreatingNumbers);
}
