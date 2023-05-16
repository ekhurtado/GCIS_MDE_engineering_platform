<!--<?xml version="1.0" encoding="UTF-8"?>-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:str="http://exslt.org/strings"
				xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
				<xsl:output omit-xml-declaration="yes" indent="yes"/>


  <xsl:template match="Component">
const fs = require('fs');

// Aplikazio-eredua osatzeko elementu erabilgarrien liburutegia inportatu
const {FunctionInfo<xsl:if test="count(//outputs) = 0">, createFirstMicroservice</xsl:if><xsl:if test="count(//inputs) > 0 and count(//outputs) > 0">, createNewMicroservice</xsl:if><xsl:if test="count(//inputs) > 0">, addMicroServiceToModel</xsl:if>} = require('../appModel_utils');

// Osagaiaren aldagaiak
const componentName = "<xsl:value-of select="@name"/>";
const codeName = "<xsl:value-of select="@codeName"/>";

module.exports = function(RED) {
    function ProcessingNumbers(config) {
        RED.nodes.createNode(this,config);

        this.function = config.function;
		<xsl:for-each select="functionality"><xsl:for-each select="str:split(@customization, ',')">this.<xsl:value-of select="."/> = config.<xsl:value-of select="."/>;
		</xsl:for-each></xsl:for-each>
		var node = this;

	  	 // Funtzionalitate guztien informazioa betetzen dugu
		 // --------------------
		 const allFunctionsInfo= [
	  		<xsl:for-each select="functionality">INFORMAZIOA BETETZEA  FALTA DA</xsl:for-each>
	     ]

	}

    RED.nodes.registerType("Processing numbers",ProcessingNumbers);
}
  </xsl:template>
</xsl:stylesheet>
