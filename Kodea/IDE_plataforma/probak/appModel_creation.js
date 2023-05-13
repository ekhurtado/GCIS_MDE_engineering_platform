// Beharrezko liburutegiak inportatu
const xml2js = require('xml2js');
const builder = new xml2js.Builder();

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice} = require('../txantiloiak/appModel_utils');
// import FunctionInfo from './appModel_utils';

// Heltzen de mezua
var msg = "<Application name=\"NumbersProcessing\">\n" +
    "\t\t<Microservice name=\"CreatingNumber\" service=\"NaturalValue\"\n" +
    "\t\t\t\t\t\tcustomization=\"{type: 'random'}\">\n" +
    "\t\t\t<outPort name=\"CreatingNumberOPort\" \n" +
    "\t\t\t\tprotocol=\"HTTP\" dataType=\"TNumber\"/>\n" +
    "\t\t</Microservice>\t\n" +
    "\n" +
    "\t\t\n" +
    "\t\t<channel from=\"CreatingNumbersOPort\"/>" +
    "</Application>\t\n"


// hautatutako pertsonalizazioa TODO CAMBIARLO POR LO RECOGIDO EN NODERED
var selectedFunctionName = "IncreaseValue";
var selectedPortNumber = 7000;
var selectedCustomizationValue = 4; // osagai honen kasuan "step"

// Osagaiaren aldagaiak
const componentName = "ProcessingNumbers";
const codePath = "gcr.io/gcis/processing-numbers:latest";


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
    if (selectedFunctionName === allFunctionsInfo[funcObj].name)
        selectedFunctionInfo = allFunctionsInfo[funcObj];
}

// Mikrozerbitzu berriaren informazioa eraikitzen dugu
// --------------------
const newMicroservice = createNewMicroservice(componentName, codePath, selectedFunctionInfo, selectedPortNumber);
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

console.log("XML inicio:");
console.log(msg);
console.log("XML final:");
console.log(appModelXML);

// XML aplikazio-eredua hurrengo nodoari bidali
// node.send(appModelXML);
