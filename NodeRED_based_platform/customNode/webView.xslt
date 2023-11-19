<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:str="http://exslt.org/strings"
				xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
				<xsl:output omit-xml-declaration="yes" indent="yes"/>

  <xsl:template match="Component">
	<xsl:if test="count(functionality/@customization) > 0">
		<script type="text/javascript">
	function show<xsl:value-of select="@name"/>Customization() {
		const selectElement = document.getElementById("node-input-function");
		const customizationContainer = document.getElementById("contenedor-customization");

		// Kode honen bitartez customization datuak lortzeko elementuak erakutsi edo izkatatu ditzakezu
		// Nahi izanez gero, kode hau modifika dezakezu, garatutako osagaiaren arabera
		switch (selectElement.value) {
			case "":
				customizationContainer.style.display = "none";
				break;
			default:
				customizationContainer.style.display = "block";
				break;
		}
	}
</script>
</xsl:if>
<xsl:text>&#xA;</xsl:text>
<script type="text/javascript">
	RED.nodes.registerType('<xsl:value-of select="@name"/>',{
		category: '<xsl:value-of select="@category"/>',
		<xsl:if test="@category = 'source'">color: '#14a7e0',</xsl:if>
		<xsl:if test="@category = 'processing'">color: '#f0e007',</xsl:if>
		<xsl:if test="@category = 'sink'">color: '#08bd08',</xsl:if>
		defaults: {
			function:{value: ""},
			<xsl:if test="count(//inputs) > 0">portnumber: {value: -1},<xsl:text>&#xA;&#x9;&#x9;&#x9;</xsl:text></xsl:if>
			<xsl:for-each select="distinct-values(functionality/@customization)">
				<xsl:for-each select="tokenize(., ',')">
					<xsl:value-of select="."/>: {value: ""},
				</xsl:for-each>
			</xsl:for-each>
		},
		<xsl:if test="count(functionality/inputs) = 0">inputs:0,&#xA;&#x9;&#x9;</xsl:if>
		<xsl:if test="count(functionality/inputs) > 0">inputs:1,&#xA;&#x9;&#x9;</xsl:if>
		<xsl:if test="count(functionality/outputs) = 0">outputs:0,&#xA;&#x9;&#x9;&#x9;</xsl:if>
		<xsl:if test="count(functionality/outputs) > 0">outputs:1,&#xA;&#x9;&#x9;&#x9;</xsl:if>
		icon: '<xsl:value-of select="@category"/>.png',
		label: function() {
			return this.label || "<xsl:value-of select="@name"/>";
		},
		oneditprepare: function() {
			var node = this;
			$("#node-input-function").on("change", function() {
				node.label = $(this).val();
			});
		},
		oneditsave: function () {
			this.label = $("#node-input-function").val();
		}
	});
</script>
<xsl:text>&#xA;</xsl:text>	<!-- lerro-saltoa-->

<script type="text/html">
	<xsl:attribute name="data-template-name"><xsl:value-of select="@name"/></xsl:attribute>
	<xsl:text>&#xA;&#x9;</xsl:text>
	<div class="form-row">
		<xsl:text>&#xA;&#x9;&#x9;</xsl:text>
		<label for="node-input-function"><i class="fa fa-tag"></i> Funtzionalitateak </label><span><xsl:text>&#160;&#160;</xsl:text></span>
		<xsl:text>&#xA;&#x9;&#x9;</xsl:text>
		<select name="function" id="node-input-function">
		<xsl:if test="count(functionality/@customization) > 0">
			<xsl:attribute name="onchange">show<xsl:value-of select="@name"/>Customization()</xsl:attribute>
		</xsl:if>
		<xsl:text>&#xA;&#x9;&#x9;&#x9;</xsl:text>
		<xsl:for-each select="functionality">
		<option>
			 <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
			<xsl:value-of select="@name"/>
		</option>
		<xsl:text>&#xA;&#x9;&#x9;&#x9;</xsl:text>
		</xsl:for-each>
	</select><xsl:text>&#xA;&#x9;&#x9;&#x9;</xsl:text>
	<xsl:if test="count(functionality/inputs) > 0">
		<label for="node-input-portnumber"><i class="fa fa-tag"></i> Aukeratu ataka zenbakia </label>
        <input name="portnumber" id="node-input-portnumber"
               type="number" min="0" max= "65536" step="1" placeholder="Sarrera-ataka zenbakia"/>
	</xsl:if>
	<xsl:if test="count(functionality/@customization) > 0">
		<div id="contenedor-customization" style="display: none;"><xsl:text>&#xA;&#x9;&#x9;&#x9;&#x9;</xsl:text>
			<xsl:for-each select="distinct-values(functionality/@customization)">
				<xsl:for-each select="tokenize(., ',')">
					<label>
						<xsl:attribute name="for">node-input-<xsl:value-of select="."/></xsl:attribute>
						<i class="fa fa-tag"></i>
						<xsl:value-of select="."/>
					</label><xsl:text>&#xA;&#x9;&#x9;&#x9;&#x9;</xsl:text>
					<xsl:comment>Sar ezazu hemen customization balioa lortzeko elementu egokia, bere mota kontuan edukiz (select, input...)</xsl:comment>
					<xsl:comment>Defektuz, textuak lortzeko baliabideak gehituko da</xsl:comment>
<!--					<input name=<xsl:value-of select="."/> id="node-input-"<xsl:value-of select="."/>" type="text">-->
					<input>
						<xsl:attribute name="name"><xsl:value-of select="."/></xsl:attribute>
						<xsl:attribute name="id">node-input-<xsl:value-of select="."/></xsl:attribute>
						<xsl:attribute name="type">text</xsl:attribute>
					</input>
					<xsl:text>&#xA;&#x9;&#x9;&#x9;&#x9;</xsl:text>
				</xsl:for-each>
			</xsl:for-each>
		</div><xsl:text>&#xA;&#x9;</xsl:text>
	</xsl:if>
	</div><xsl:text>&#xA;</xsl:text>
</script>
<xsl:text>&#xA;</xsl:text>
<script type="text/html">
	<xsl:attribute name="data-help-name">
		<xsl:value-of select="@name"/>
	</xsl:attribute><xsl:text>&#xA;&#x9;</xsl:text>
	<p>Description of the component.</p><xsl:text>&#xA;&#x9;</xsl:text>
	<ul><xsl:text>&#xA;&#x9;&#x9;</xsl:text>
	<xsl:for-each select="functionality">
		<li><b><xsl:value-of select="@name"/></b>: <xsl:value-of select="@description"/>
		<xsl:for-each select="inputs">
			Input Protocol: <xsl:value-of select="@protocol"/>.
		</xsl:for-each>
		<xsl:for-each select="outputs">
			Output protocol: <xsl:value-of select="@protocol"/>.
		</xsl:for-each>
		</li><xsl:text>&#xA;&#x9;&#x9;</xsl:text>
	</xsl:for-each>
	</ul><xsl:text>&#xA;</xsl:text>
</script>
  </xsl:template>
</xsl:stylesheet>
