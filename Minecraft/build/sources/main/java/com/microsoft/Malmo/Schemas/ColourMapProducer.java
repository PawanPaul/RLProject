//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2024.09.17 at 07:25:58 AM IST 
//


package com.microsoft.Malmo.Schemas;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.HexBinaryAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="Width" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="Height" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;choice maxOccurs="unbounded" minOccurs="0">
 *           &lt;element name="ColourSpec" type="{http://ProjectMalmo.microsoft.com}MobWithColour"/>
 *         &lt;/choice>
 *       &lt;/sequence>
 *       &lt;attribute name="skyColour" type="{http://ProjectMalmo.microsoft.com}HexColour" default="fbceb1" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "width",
    "height",
    "colourSpec"
})
@XmlRootElement(name = "ColourMapProducer")
public class ColourMapProducer {

    @XmlElement(name = "Width")
    protected int width;
    @XmlElement(name = "Height")
    protected int height;
    @XmlElement(name = "ColourSpec")
    protected List<MobWithColour> colourSpec;
    @XmlAttribute(name = "skyColour")
    @XmlJavaTypeAdapter(HexBinaryAdapter.class)
    protected byte[] skyColour;

    /**
     * Gets the value of the width property.
     * 
     */
    public int getWidth() {
        return width;
    }

    /**
     * Sets the value of the width property.
     * 
     */
    public void setWidth(int value) {
        this.width = value;
    }

    /**
     * Gets the value of the height property.
     * 
     */
    public int getHeight() {
        return height;
    }

    /**
     * Sets the value of the height property.
     * 
     */
    public void setHeight(int value) {
        this.height = value;
    }

    /**
     * Gets the value of the colourSpec property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the colourSpec property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getColourSpec().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link MobWithColour }
     * 
     * 
     */
    public List<MobWithColour> getColourSpec() {
        if (colourSpec == null) {
            colourSpec = new ArrayList<MobWithColour>();
        }
        return this.colourSpec;
    }

    /**
     * Gets the value of the skyColour property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public byte[] getSkyColour() {
        if (skyColour == null) {
            return new HexBinaryAdapter().unmarshal("fbceb1");
        } else {
            return skyColour;
        }
    }

    /**
     * Sets the value of the skyColour property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSkyColour(byte[] value) {
        this.skyColour = value;
    }

}
