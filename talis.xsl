<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:purl="http://purl.org/rss/1.0/"
  xmlns:relevance="http://a9.com/-/opensearch/extensions/relevance/1.0/"
  xmlns:os="http://a9.com/-/spec/opensearch/1.1/"
  xmlns:ns.0="http://data.ordnancesurvey.co.uk/ontology/admingeo/"
  xmlns:ns.1="http://xmlns.com/foaf/0.1/"
  xmlns:ns.2="http://data.ordnancesurvey.co.uk/ontology/spatialrelations/"
  xmlns:ns.3="http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/"
  xmlns:ns.4="http://www.w3.org/2000/01/rdf-schema#">

    <xsl:output method="html"/>
    <xsl:template match="/">
        <html>
        <xsl:apply-templates select="/rdf:RDF/purl:channel"/>
        </html>
    </xsl:template>
    <xsl:template match="/rdf:RDF/purl:channel">
        <h1>Ordnance Survey</h1>
        <p>Your search for “<xsl:value-of select="purl:title"/>” returned <xsl:value-of select="os:totalResults"/> results:</p>
        <ul>
            <xsl:apply-templates select="/rdf:RDF/purl:item"/>
        </ul>
    </xsl:template>
    <xsl:template match="/rdf:RDF/purl:item">
        <li>
            <a href="{purl:link}" title="{substring(dc:date, 0, 11)}">
                <xsl:value-of select="ns.1:name"/>
            </a>
            <xsl:text> (</xsl:text>
            <xsl:variable name="type" select="ns.3:featureType/rdf:Description/@rdf:about"/>
            <xsl:choose>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/Antiquity'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Antiquity</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/ForestOrWood'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Forrest or wood</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/Farm'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Farm</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/HillOrMountain'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Hill or mountain</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/City'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>City</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/Town'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Town</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/Other'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Other</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/OtherSettlement'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Settlement</xsl:text>
                    </span>
                </xsl:when>
                <xsl:when test="$type = 'http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/WaterFeature'">
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Water feature</xsl:text>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <span>
                        <xsl:attribute name="title" select="$type"/>
                        <xsl:text>Unknown</xsl:text>
                    </span>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text>)</xsl:text>
        </li>
    </xsl:template>
</xsl:stylesheet>
