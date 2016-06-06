package com.createw.lunch.servlet;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.io.SAXReader;

/**
 * Servlet implementation class ShowXml
 */
public class ShowXml extends HttpServlet {
	private static final long serialVersionUID = 1L;
//	private final String FILE_PATH = ShowXml.class.getResource("/data.xml").getPath().replace("%20", " ");  
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ShowXml() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		SAXReader reader = new SAXReader();
		String outString = "";
		try {
			Document document = reader.read(new File(Util.FILE_PATH));
			outString = document.asXML();
		} catch (DocumentException e) {
			e.printStackTrace();
		}
		response.setContentType("text/xml;charset=utf-8");
		PrintWriter out = response.getWriter();
		out.println(outString);
		
		out.flush();
        out.close();
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
	}

}
