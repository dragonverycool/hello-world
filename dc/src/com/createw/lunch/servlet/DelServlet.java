package com.createw.lunch.servlet;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public class DelServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.sendRedirect(request.getContextPath()+"/del.jsp");
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		request.setCharacterEncoding("UTF-8");
		String dish = request.getParameter("cai");
		String user = request.getParameter("ren");
		
		if(dish!=null && !"".equals(dish.trim()))
			XmlHandle.delDish(dish.trim());
		if(user!=null && !"".equals(user.trim()))
			XmlHandle.delUser(user.trim());
		
		response.sendRedirect(request.getContextPath()+"/index.jsp");
	}
}
