package com.createw.lunch.servlet;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.Node;
import org.dom4j.io.OutputFormat;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;

public class XmlHandle {
	
//	static final String FILE_PATH = XmlHandle.class.getResource("/data.xml").getPath().replace("%20", " ");
//			System.getProperty("java.class.path"); 
//			getClass().getResource("/data.xml").getPath();
	
	public XmlHandle() {

	}
	
	public synchronized  static boolean ordering(String user, String dish){
		String DATE_STR = Util.getDateString();
		if(dish==null || user==null || "".equals(user.trim()) || "".equals(dish.trim()))
			return false;
		try {
	        SAXReader reader = new SAXReader(); 
			Document document = reader.read(new File(Util.FILE_PATH));			
	        Element root = document.getRootElement();	        
	        Element node = (Element) root.selectSingleNode("//date[@day='" + DATE_STR + "']");	        
	        
        	if(node==null){
        		return false;
	        }else{
	        	Element foodNode = (Element) node.selectSingleNode("./food[@name='" + dish + "']");	        	    	
	        	Element personNode = (Element) node.selectSingleNode("./food/person[@name='" +user+ "']");
	        	if(personNode!=null){
	        		System.out.println(user+ "已经订餐");
	        		personNode.getParent().remove(personNode);
	        	}
	        	
	        	foodNode.addElement("person").addAttribute("name", user).addAttribute("time", new SimpleDateFormat("HH:mm:ss.SSS").format(new Date()));
	        }
	        
        	
        	OutputFormat xmlFormat = OutputFormat.createPrettyPrint();
        	xmlFormat.setEncoding("utf-8");
        	XMLWriter writer = new XMLWriter(new FileOutputStream(new File(Util.FILE_PATH)), xmlFormat);
        	
//	        XMLWriter writer = new XMLWriter(new FileWriter(new File(FILE_PATH)));  
            writer.write(document);  
            writer.close();
            
//            System.out.println(document.asXML());
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}
	
	public synchronized  static boolean addDish(String dish){
		if(dish==null || "".equals(dish.trim()))
			return false;
		try {
//			dish = dish.replace(" ", "");
			String DATE_STR = new SimpleDateFormat("yyyyMMdd").format(new Date());
	        SAXReader reader = new SAXReader(); 
			Document document = reader.read(new File(Util.FILE_PATH));			
	        Element root = document.getRootElement();
	        List<Element> elements = root.elements();
	        
	        Element node = (Element) root.selectSingleNode("//date[@day='" + DATE_STR + "']");
	        if(node==null){
	        	node = DocumentHelper.createElement("date");  
	        	node.addAttribute("day", DATE_STR);  
                elements.add(0, node);                
//	        	node = root.addElement("date");
//	        	node.addAttribute("day", DATE_STR);
	        }
	        if(node.selectSingleNode("./food[@name='" + dish + "']")!=null){
	        	System.out.println("菜单已经存在");
	        	return false;
	        }
        	Element foodNode = node.addElement("food");
        	foodNode.addAttribute("name", dish);        	
        	
        	OutputFormat xmlFormat = OutputFormat.createPrettyPrint();
        	xmlFormat.setEncoding("utf-8");
        	XMLWriter writer = new XMLWriter(new FileOutputStream(new File(Util.FILE_PATH)), xmlFormat);
        	
//        	XMLWriter writer = new XMLWriter(new FileWriter(new File(FILE_PATH)));  
            writer.write(document);  
            writer.close();
		}catch(Exception e){
			e.printStackTrace();
			return false;
		}
		return true;
	}
	
	
	public synchronized  static void delDish(String dish){
		if(dish==null || "".equals(dish))
			return;
		try {
			String DATE_STR = new SimpleDateFormat("yyyyMMdd").format(new Date());
	        SAXReader reader = new SAXReader(); 
			Document document = reader.read(new File(Util.FILE_PATH));			
	        Element root = document.getRootElement();
	        
	        Element node = (Element) root.selectSingleNode("//date[@day='" + DATE_STR + "']");
	        if(node==null){
	        	return;
	        }
	        Node  dishNode = node.selectSingleNode("./food[@name='" + dish + "']");
	        if(dishNode == null){
	        	return;
	        }
	        
	        node.remove(dishNode);
	        
        	OutputFormat xmlFormat = OutputFormat.createPrettyPrint();
        	xmlFormat.setEncoding("utf-8");
        	XMLWriter writer = new XMLWriter(new FileOutputStream(new File(Util.FILE_PATH)), xmlFormat);  
            writer.write(document);  
            writer.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	public synchronized  static void delUser(String user){
		if(user==null || "".equals(user))
			return;
		try {
			String DATE_STR = new SimpleDateFormat("yyyyMMdd").format(new Date());
	        SAXReader reader = new SAXReader(); 
			Document document = reader.read(new File(Util.FILE_PATH));			
	        Element root = document.getRootElement();
	        
	        Element node = (Element) root.selectSingleNode("//date[@day='" + DATE_STR + "']");
	        if(node==null){
	        	return;
	        }
	        Element userNode = (Element) node.selectSingleNode("./food/person[@name='" +user+ "']");
        	if(userNode!=null){
        		userNode.getParent().remove(userNode);
        	}
        	
        	OutputFormat xmlFormat = OutputFormat.createPrettyPrint();
        	xmlFormat.setEncoding("utf-8");
        	XMLWriter writer = new XMLWriter(new FileOutputStream(new File(Util.FILE_PATH)), xmlFormat);  
            writer.write(document);
            writer.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		XmlHandle.ordering("cc","gg");
	}

}
