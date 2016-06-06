<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<%@page import="org.dom4j.*"%>
<%@page import="org.dom4j.io.*"%>
<%@page import="java.io.*"%>
<%@page import="java.text.SimpleDateFormat"%>
<%@page import="java.util.Date, java.util.List"%>
<%@page import="com.createw.lunch.servlet.Util"%>


<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>订餐</title>
<style type="text/css">
html,body{width:100%; height:100%; margin:0; padding:0; overflow:hidden;}
#backDiv {
	width:100%; 
	height:100%;
	position:absolute; 
	left:0px; 
	top:0px; 
	z-index:100;	
	filter:alpha(opacity=40);
	-moz-opacity:0.4;
	-khtml-opacity: 0.4;
	opacity: 0.4;
}

#bodyDiv {
	width:100%; 
	height:100%;  
	margin:5px; 
	padding:5px; 
	position:absolute; 
	left:0px; 
	top:0px; 
	z-index:200;
}

table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}

</style>
<% 
	response.setContentType("application/vnd.ms-excel"); 
	response.addHeader("Content-Disposition", "attachment;filename=dingcan.xls"); 
%>
</head>
<body>
	<div id="backDiv">
		<img src="<%=request.getContextPath()%>/backgd.jpg" width="100%" height="100%" />
	</div>
	<div id = "bodyDiv">
	<table class="gridtable">
		<tr>
			<th>菜单</th>
			<th>数量</th>
			<th>订餐人</th>
		</tr>
	
	<%
	int count = 0;
	//String fileName = "D:/data.xml";
	String dateStr = new SimpleDateFormat("yyyyMMdd").format(new Date());
	
	SAXReader reader = new SAXReader();
	Document document = reader.read(new File(Util.FILE_PATH));			
    Element root = document.getRootElement();
    
    Node node = root.selectSingleNode("//date[@day='"+dateStr+"']");

    if(node!=null){
    	for(Element e : (List<Element>)node.selectNodes("./food")){ 
    		String dish = e.attributeValue("name");
    		out.print("<tr><td>");
    		out.print(dish);
    		out.print("</td><td>");
    		List<Element> persons = e.selectNodes("./person");
    		count += persons!=null ? persons.size() : 0;
    		out.print(persons!=null ? persons.size() : 0);
    		out.print("</td><td>");
    		for(Element p : persons)
    			out.print(p.attributeValue("name")+", ");
    		out.print("</td></tr>");    		
    	}    	
    }
    out.print("<tr><td><b>合计：</b></td><td><b>" + count + "</b></td><td></td></tr>");
	%>	
	</table>
	</div>
</body>
</html>