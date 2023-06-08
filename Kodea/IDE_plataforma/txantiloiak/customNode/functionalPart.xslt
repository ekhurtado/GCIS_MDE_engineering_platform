<!--<?xml version="1.0" encoding="UTF-8"?>-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:str="http://exslt.org/strings"
				xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
				<xsl:output omit-xml-declaration="yes" indent="yes"/>

  <xsl:template match="component">

const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo<xsl:if test="count(//outputs) = 0">, createFirstMicroservice</xsl:if><xsl:if test="count(//inputs) > 0 and count(//outputs) > 0">, createNewMicroservice</xsl:if><xsl:if test="count(//inputs) > 0">, addMicroServiceToModel</xsl:if><xsl:if test="count(//outputs) = 0">, checkApplicationMetaModel</xsl:if>} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "<xsl:value-of select="@name"/>";
const imgBase = "<xsl:value-of select="@imgBase"/>";

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);

	  	// Web-ikuspegian zehaztutako balioak lortuko ditugu
	  	// --------------------
        this.function = config.function;
		<xsl:for-each select="distinct-values(functionality/@customization)"><xsl:for-each select="tokenize(., ',')">this.selected<xsl:value-of select="."/> = config.<xsl:value-of select="."/>;
		</xsl:for-each></xsl:for-each>
	  	<xsl:if test="count(//inputs) > 0">this.selectedPortNumber = config.portnumber;</xsl:if>
		var node = this;

	  	<xsl:if test="count(//inputs) = 0">
		var RED2 = require.main.require('node-red');
        var nireflow = RED2.nodes.getFlow(this.z);    // this.z -> nodoa dagoen fluxuaren IDa
        var appName = nireflow.label;
	  	</xsl:if>

	  	 // Funtzionalitate guztien informazioa betetzen dugu
		 // --------------------
		 const allFunctionsInfo = [

	  		<xsl:for-each select="functionality">
				<xsl:value-of select="@id"/>Info = new FunctionInfo("<xsl:value-of select="@id"/>", "<xsl:value-of select="inputs/@protocol"/>", "<xsl:value-of select="outputs/@protocol"/>", "<xsl:value-of select="inputs/@dataType"/>", "<xsl:value-of select="outputs/@dataType"/>", "<xsl:value-of select="@customization"/>");
			</xsl:for-each>
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
		<xsl:if test="count(//outputs) = 0">const newMicroservice = createLastMicroservice(componentName, codeName, selectedFunctionInfo, node.selectedPortNumber);</xsl:if>
		<xsl:if test="count(//inputs) > 0 and count(//outputs) > 0">const newMicroservice = createNewMicroservice(componentName, codeName, selectedFunctionInfo, node.selectedPortNumber);</xsl:if>
		<xsl:if test="count(//inputs) > 0 and count(//outputs) > 0">const newMicroservice = createFirstMicroservice(componentName, codeName, selectedFunctionInfo);</xsl:if>
		<xsl:if test="count(//functionality/@customization) > 0">
		if (selectedCustomizationValue !== "")
			newMicroservice.$.customization = `{'${selectedFunctionInfo.customizationName}': '${selectedCustomizationValue}'}`;
		// Customization balio gehiago badaude, hemen gehi ditzakezu, aurreko bi lerroak aldatuz
		</xsl:if>

	  	<xsl:if test="count(//inputs) != 0">
		// Aurreko osagaiak bidalitako aplikazio-eredua lortzen dugu
		// --------------------
		let appModelXML = addMicroServiceToModel(msg, newMicroservice, <xsl:if test="count(//outputs) = 0">false</xsl:if>
		<xsl:if test="count(//inputs) > 0 and count(//outputs) > 0">true</xsl:if>);

		</xsl:if>

	  	<xsl:if test="count(//inputs) = 0">
		let Microservice = newMicroservice;
	  	const channel = {
			$: {
				from: Microservice.outPort.$.name
			}
		}
		let appModel = {
			Application: {
				$: {
					name: appName, // recogerlo del nombre del flow
				},
				Microservice,
				channel
			}
		}
		// XML fitxategia sortu
		let appModelXML = builder.buildObject(appModel);
	  	</xsl:if>
	  	<xsl:if test="count(//outputs) = 0">
		// Azkenengo osagaia denez, aplikazio-eredua zuzena dela konprobatuko du
		let result = checkApplicationMetaModel(appModelXML);
		if (!result || result.length === 0) {
			// XML aplikazio-eredua zuzena da, erabiltzaileari emaitza erakustiko diogu
			node.warn(appModelXML);
		} else
			node.error(`Sortutako aplikazio-eredua ez dator bat meta-ereduarekin. Arrazoia: ${result}`);
	  	</xsl:if>
	  	<xsl:if test="count(//outputs) != 0">
		// XML aplikazio-eredua hurrengo nodoari bidali
		node.send(appModelXML);
	  	</xsl:if>
	}

    RED.nodes.registerType("Processing numbers",ProcessingNumbers);
}
  </xsl:template>
</xsl:stylesheet>
