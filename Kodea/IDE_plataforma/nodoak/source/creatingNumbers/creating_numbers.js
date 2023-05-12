const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');


// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createFirstMicroservice} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "CreatingNumbers";
const codePath = "gcr.io/gcis/creating-numbers:latest";

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
    function CreatingNumbers(config) {
        RED.nodes.createNode(this,config);
        
        this.function = config.function;
        var node = this;

        // var xmlDef = {
        //     application: {
        //         $: {
        //             'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        //             'xsi:noNamespaceSchemaLocation': '/xmlSchemas/Application.xsd',
        //             name: 'data_adquisition'
        //         }
        //     }
        // }
        //
        // const builder = new xml2js.Builder();
        // const xml = builder.buildObject(xmlDef);
        //
        // node.send(xml);

        if (node.function === "") {
            node.error(`Ez da funtzionalitaterik aukeratu nodo batean. Jakiteko zein den, klikatu errore mezu honetan.`);
        } else {

            // Funtzionalitate guztien informazioa betetzen dugu
            // --------------------
            const allFunctionsInfo= [
                naturalValueInfo = new FunctionInfo("NaturalValue", null, "HTTP", "TNumber", "type"),
                increasingValueInfo = new FunctionInfo("IncreasingValue", null, "HTTP", null, "TNumber", "step"),
                decreasingValueInfo = new FunctionInfo("DecreasingValue", null, "HTTP", null, "TNumber", "step")
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
            const Microservice = createFirstMicroservice(componentName, codePath, selectedFunctionInfo);
            // Osagai honen pertsonalizazioa gehitzen diogu (osagai honen bereizgarria dena)
            //newMicroservice.$.customization = `{${selectedFunctionInfo.customizationName}: ${selectedCustomizationValue}}`;

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
                        name: "NumbersProcessing", // recogerlo del nombre del flow
                    },
                    Microservice,
                    channel
                }
            }

            // XML fitxategia sortu
            appModelXMLObject = builder.buildObject(appModelXML);

            // let msg = {
            //     payload: "hola"
            // };
            // msg.appmodel = appModelXML;
            // msg.appmodel2 = appModelXMLObject;

            // XML aplikazio-eredua hurrengo nodoari bidali
            node.send(appModelXMLObject);
        }


    }

    RED.nodes.registerType("Creating numbers",CreatingNumbers);
}
