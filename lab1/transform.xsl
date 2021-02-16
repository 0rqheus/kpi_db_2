<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output method="xml" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" doctype-public="-//W3C//DTD XHTML 1.1//EN" indent="yes"/>

    <xsl:template match="/">
        <html xml:lang="en">
            <head>
                <title>Lab 1</title>
            </head>
            <body>
                <h1>Exclusive "Rozetka" items</h1>
                <xsl:apply-templates select="/rozetka"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="/rozetka">
        <table border="1" style="border-collapse: collapse;">
            <thead>
                <tr>
                    <td>Image</td>
                    <td>Price</td>
                    <td>Description</td>
                </tr>
            </thead>
            <tbody>
                <xsl:apply-templates select="/rozetka/product"/>
            </tbody>
        </table>
    </xsl:template>


    <xsl:template match="/rozetka/product">
        <tr>
            <td><xsl:apply-templates select="image"/></td>
            <td><xsl:apply-templates select="price"/></td>
            <td><xsl:apply-templates select="description"/></td>
        </tr>
    </xsl:template>

    <xsl:template match="image">
        <img>
            <xsl:attribute name="style">
                max-width: 200px;
                max-height: 200px;
                margin: auto;
                display: block;
            </xsl:attribute>
            <xsl:attribute name="src">
                <xsl:value-of select="text()"/>
            </xsl:attribute>
        </img>
    </xsl:template>
    
    <xsl:template match="price">
        <xsl:attribute name="style">
            font-weight: bold;
            text-align: center;
        </xsl:attribute>
        <xsl:value-of select="text()"/>
    </xsl:template>

    <xsl:template match="description">
        <xsl:value-of select="text()"/>
    </xsl:template>

</xsl:stylesheet>