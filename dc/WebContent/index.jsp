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
	overflow:auto;
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
<script>
function dingcan(e){
	document.getElementById("dish").value = e.parentNode.parentNode.firstChild.innerText;
	var name = prompt("请输入订餐人姓名，一次一人","");
	if(name){
		document.getElementById("user").value = name.trim();
		document.getElementById("dingcan").submit();
	}
}


function addDish(){
	var name = prompt("请输入菜名","");
	if(name){
		document.getElementById("addDish").value = name.trim();
		document.getElementById("jiacai").submit();
	}
}

</script>
</head>
<body>

	<div id="backDiv">
		<img src="<%=request.getContextPath()%>/backgd.jpg" width="100%" height="100%" />
	</div>
	 
	<div id = "bodyDiv" >
	<table class="gridtable">
		<tr>
			<th>菜单</th>
			<th>数量</th>
			<th>订餐人</th>
			<th>   </th>
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
 //   	List list = node.selectNodes("./food");
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
    		out.print("</td><td>");
    		out.print("<a href='#' onclick=dingcan(this)>订餐</a>");
    		out.print("</td></tr>");
    	}
    }
	%>	
	</table>
	<form id="dingcan" action="LunchServlet" method="post">
		<input type="hidden" id="user" name="user"/>
		<input type="hidden" id="dish" name="dish"/>
	</form>
	<!-- 
	<form action="LunchServlet" method="post">
		姓名：<input type="text" name="user"/><br/>
		菜：<input type="text" name="dish"/><br/>
		<input type="submit" value="提交"/>
	</form>
	 -->
	 <form id="jiacai" action="AddDish" method="post">
		<input type="hidden" id="addDish" name="addDish"/>
	</form>
	<br><font color="red">共<%=count %>份（如需更改，用原名字重新订即可）<br></font><br><br>
	<a href="#" onclick="addDish();">加菜</a>
	<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
	<a href="#" onclick="window.open('<%=request.getContextPath()%>/list.jpg');">菜单</a>
	<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
	<a href="#" onclick="window.open('ShowXml');">记录</a>
	<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
	<br><br>&nbsp;&nbsp;
	<a href="#" onclick="window.open('upload');">上传菜单</a>
	<span>&nbsp;&nbsp;&nbsp;</span>
	<a href="#" onclick="window.open('excel.jsp');">导出</a>
	<br><br><br>
	</div>
</body>
</html>