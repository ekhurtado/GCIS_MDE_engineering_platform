

const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo, createNewMicroservice, addMicroServiceToModel} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "ProcessingNumbers";
const codeName = "processing_numbers_base_image";

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);

	  	// Web-ikuspegian zehaztutako balioak lortuko ditugu
	  	// --------------------
        this.function = config.function;
		this.selectedstep = config.step;
		this.selectedhola = config.hola;
		this.selectedstep = config.step;
		this.selectedPortNumber = config.portnumber;
		var node = this;

	  	

	  	 // Funtzionalitate guztien informazioa betetzen dugu
		 // --------------------
		 const allFunctionsInfo = [

	  		IncreaseValueInfo = new FunctionInfo("IncreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step,hola"),
			DecreaseValueInfo = new FunctionInfo("DecreaseValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
			MultiplyValueInfo = new FunctionInfo("MultiplyValue", "HTTP", "HTTP", "TNumber", "TNumber", "step"),
			
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
		const newMicroservice = createNewMicroservice(componentName, codeName, selectedFunctionInfo, node.selectedPortNumber);//const newMicroservice = createFirstMicroservice(componentName, codeName, selectedFunctionInfo);
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
  