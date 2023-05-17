<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:str="http://exslt.org/strings"
				xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
				<xsl:output omit-xml-declaration="yes" indent="yes"/>

  <xsl:template match="application">
<xsl:param name="singleQuote">'</xsl:param>
<xsl:param name="doubleQuote">"</xsl:param>apiVersion: ehu.gcis.org/v1alpha1
kind: Application
metadata:
  name: <xsl:value-of select="@name"/>
spec:
  components: <xsl:for-each select="microservice">
    - name: <xsl:value-of select="@name"/>
      service: <xsl:value-of select="@service"/>
      image: <xsl:value-of select="@image"/>
    <xsl:if test="count(@customization) > 0">
      customization: '<xsl:value-of select="replace(@customization, $singleQuote, $doubleQuote)"/>'</xsl:if>
    <xsl:if test="count(inPort) > 0">
      inPort:
        name: <xsl:value-of select="inPort/@name"/>
        dataType: <xsl:value-of select="inPort/@dataType"/>
        protocol: <xsl:value-of select="inPort/@protocol"/>
        number: '<xsl:value-of select="inPort/@number"/>'</xsl:if>
    <xsl:if test="count(outPort) > 0">
      outPort:
        name: <xsl:value-of select="outPort/@name"/>
        dataType: <xsl:value-of select="outPort/@dataType"/>
        protocol: <xsl:value-of select="outPort/@protocol"/>
	</xsl:if>
  </xsl:for-each>
  channels: <xsl:for-each select="channel">
    - from: <xsl:value-of select="@from"/>
      to: <xsl:value-of select="@to"/>
  </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
