

const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice, addMicroServiceToModel} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ZenbakienProzesamendua";
const imgBase = "ekhurtado/gcis:zenbakien-prozesamendua";

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);

	  	// Web-ikuspegian zehaztutako balioak lortuko ditugu
	  	// --------------------
        this.function = config.function;
		this.selectedurratsa = config.urratsa;
		this.selectedbiderkatzailea = config.biderkatzailea;
		this.selectedPortNumber = config.portnumber;
		var node = this;

	  	

	  	 // Funtzionalitate guztien informazioa betetzen dugu
		 // --------------------
		 const allFunctionsInfo = [

	  		BalioaHandituInfo = new FunctionInfo("BalioaHanditu", "HTTP", "HTTP", "TNumber", "TNumber", "urratsa"),
			BalioaTxikituInfo = new FunctionInfo("BalioaTxikitu", "HTTP", "HTTP", "TNumber", "TNumber", "urratsa"),
			BalioaBiderkatuInfo = new FunctionInfo("BalioaBiderkatu", "HTTP", "HTTP", "TNumber", "TNumber", "biderkatzailea"),
			
	     ]

	  	// Hautatutako funtzionalitatearen informazioa lortzen dugu
	  	// --------------------
	  	// Nahi izanez gero, customization balioetako bat zuzena ez izanez gero, hemen konproba dezakezu
	  	let selectedFunctionInfo;
		for (const funcObj in allFunctionsInfo) {
			if (node.function === allFunctionsInfo[funcObj].name) {
				selectedFunctionInfo = allFunctionsInfo[funcObj];
			}
		}

	  	// Mikrozerbitzu berriaren informazioa eraikitzen dugu
		// --------------------
		const newMicroservice = createNewMicroservice(componentName, codeName, selectedFunctionInfo, node.selectedPortNumber);
		if (selectedCustomizationValue !== "")
			newMicroservice.$.customization = `{'${selectedFunctionInfo.customizationName}': '${selectedCustomizationValue}'}`;
		// Customization balio gehiago badaude, hemen gehi ditzakezu, aurreko bi lerroak aldatuz
		
		// Aurreko osagaiak bidalitako aplikazio-eredua lortzen dugu
		// --------------------
		let appModelXML = addMicroServiceToModel(msg, newMicroservice, true);

		
		// XML aplikazio-eredua hurrengo nodoari bidali
		node.send(appModelXML);
	  	
	}

    RED.nodes.registerType("Processing numbers",ProcessingNumbers);
}
  