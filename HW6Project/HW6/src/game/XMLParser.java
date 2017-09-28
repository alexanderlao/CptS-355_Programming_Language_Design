package game;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

// code adapted from: https://www.mkyong.com/java/how-to-read-xml-file-in-java-dom-parser/
public class XMLParser 
{
	public static void main(String argv[]) 
	{
	    try 
	    {
			File xmlFile = new File("C:\\Users\\Alex\\Desktop\\HW6\\HW6\\src\\game\\config.xml");
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(xmlFile);
	
			//optional, but recommended
			//read this - http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
			doc.getDocumentElement().normalize();
	
			System.out.println("Root element : " + doc.getDocumentElement().getNodeName());
	
			NodeList nList = doc.getElementsByTagName("Ball");
	
			System.out.println("----------------------------");

			for (int temp = 0; temp < nList.getLength(); temp++) 
			{
				Node nNode = nList.item(temp);
	
				System.out.println("\nCurrent Element : " + nNode.getNodeName());
	
				if (nNode.getNodeType() == Node.ELEMENT_NODE) 
				{
	
					Element eElement = (Element) nNode;
	
					System.out.println("Ball ID : " + eElement.getAttribute("id"));
					System.out.println("type : " + eElement.getElementsByTagName("type").item(0).getTextContent());
					System.out.println("radius : " + eElement.getElementsByTagName("radius").item(0).getTextContent());
					System.out.println("initXpos : " + eElement.getElementsByTagName("initXpos").item(0).getTextContent());
					System.out.println("initYpos : " + eElement.getElementsByTagName("initYpos").item(0).getTextContent());
					System.out.println("speedX : " + eElement.getElementsByTagName("speedX").item(0).getTextContent());
					System.out.println("speedY : " + eElement.getElementsByTagName("speedY").item(0).getTextContent());
					System.out.println("maxBallSpeed : " + eElement.getElementsByTagName("maxBallSpeed").item(0).getTextContent());
					System.out.println("color : " + eElement.getElementsByTagName("color").item(0).getTextContent());
				}
			}
	    } 
	    catch (Exception e) 
	    {
	    	e.printStackTrace();
	    }
	}
}
