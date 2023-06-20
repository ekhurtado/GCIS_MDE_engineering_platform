const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createFirstMicroservice} = require('../appModel_utils.js');

// Osagaiaren aldagaiak
const componentName = "ZenbakienSorkuntza";
const imgBase = "ekhurtado/gcis:zenbakien-sorkuntza";

module.exports = function(RED) {
    function ZenbakienSorkuntza(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        this.valuetype = config.valuetype;
        this.firstvalue = config.firstvalue;
        var node = this;

        var RED2 = require.main.require('node-red');
        var miflow = RED2.nodes.getFlow(this.z);    // this.z -> nodoa dagoen fluxuaren IDa
        var appName = miflow.label;
        if (appName.includes(" "))
            appName = appName.replace(" ", "_");

        if (node.function === "") {
            node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
        } else {

            // Funtzionalitate guztien informazioa betetzen dugu
            // --------------------
            const allFunctionsInfo= [
                naturalValueInfo = new FunctionInfo("BalioNaturalak", null, "HTTP", null, "TZenbaki", "custom_mota,custom_hasierakobalioa"),
                integerValue = new FunctionInfo("BalioOsoak", null, "HTTP", null, "TZenbaki", "custom_mota,custom_hasierakobalioa"),
                floatValue = new FunctionInfo("BalioDezimalak", null, "HTTP", null, "TZenbaki", "custom_mota,custom_hasierakobalioa")
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
            const microservice = createFirstMicroservice(componentName, imgBase, selectedFunctionInfo);
            // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
            microservice.$.customization = `{` +
                `'${selectedFunctionInfo.customizationName.split(',')[0]}': '${node.valuetype}', ` +
                `'${selectedFunctionInfo.customizationName.split(',')[1]}': ${node.firstvalue}`+
                `}`;

            const channel = {
                $: {
                    from: microservice.outPort.$.name
                }
            }

            // Lehenengo osagaia izanik, aplikazio-eredua eraikiko dugu
            // --------------------
            let appModelXML = {
                application: {
                    $: {
                        name: appName, // recogerlo del nombre del flow
                    },
                    microservice,
                    channel
                }
            }

            // XML fitxategia sortu
            appModelXMLObject = builder.buildObject(appModelXML);

            // XML aplikazio-eredua hurrengo nodoari bidali
            node.send(appModelXMLObject);
        }
    }

    RED.nodes.registerType("zenbakienSorkuntza",ZenbakienSorkuntza);
}
