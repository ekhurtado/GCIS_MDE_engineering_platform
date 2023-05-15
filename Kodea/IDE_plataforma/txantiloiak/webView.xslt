<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
  <xsl:template match="Component">
	<xsl:if test="count(@customization) > 0">
		<script type="text/javascript">
			function show<xsl:value-of select="@name"/>Customization() {
				const selectElement = document.getElementById("node-input-function");
				const customizationContainer = document.getElementById("contenedor-customization");

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
  	<script type="text/javascript">
		RED.nodes.registerType('<xsl:value-of select="@name"/>',{
			category: '<xsl:value-of select="@category"/>',
			<xsl:if test="@category = 'source'">color: '#14a7e0',</xsl:if>
			<xsl:if test="@category = 'processing'">color: '#f0e007',</xsl:if>
			<xsl:if test="@category = 'sink'">color: '#08bd08',</xsl:if>
			defaults: {
				function:{value: ""},
				<xsl:for-each select="functionality">
					<xsl:value-of select="@customization"/>: {value: ""},
				</xsl:for-each>
			},

			<xsl:if test="count(functionality/inputs) = 0">inputs:0,&#xA;&#x9;&#x9;&#x9;</xsl:if>
			<xsl:if test="count(functionality/inputs) > 0">inputs:1,&#xA;&#x9;&#x9;&#x9;</xsl:if>
			<xsl:if test="count(functionality/outputs) = 0">outputs:0,&#xA;&#x9;&#x9;&#x9;</xsl:if>
			<xsl:if test="count(functionality/outputs) > 0">outputs:1,&#xA;&#x9;&#x9;&#x9;</xsl:if>
		});
	</script>

	<script type="text/html">
		<xsl:attribute name="data-template-name"><xsl:value-of select="@name"/></xsl:attribute>

		<div class="form-row">
			<label for="node-input-function"><i class="fa fa-tag"></i>Functions</label>
			<select name="function" id="node-input-function">
			<xsl:for-each select="functionality">
			<option>
				 <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
				<xsl:value-of select="@name"/>
			</option>
			</xsl:for-each>
			</select>
		</div>
	</script>

	<script type="text/html">
		<xsl:attribute name="data-template-name">
			<xsl:value-of select="@name"/>
		</xsl:attribute>
		<p>Description of the component.</p>
		<ul>
		<xsl:for-each select="functionality">
			<li><b><xsl:value-of select="@name"/></b>: <xsl:value-of select="@description"/>.
			<xsl:for-each select="inputs">
			Input Protocol: <xsl:value-of select="@protocol"/>.
			</xsl:for-each>
			<xsl:for-each select="outputs">
			Output protocol: <xsl:value-of select="@protocol"/>.
			</xsl:for-each>
			</li>
		</xsl:for-each>
		</ul>
	</script>
  </xsl:template>
</xsl:stylesheet>
