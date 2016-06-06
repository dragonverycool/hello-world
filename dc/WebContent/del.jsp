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
<title>删除</title>
</head>
<body>
	
	<form action="del" method="post">
		姓名：<input type="text" id="ren" name="ren"/><br/>
		菜：<input type="text" id="cai" name="cai"/><br/>
		<input type="submit" value="提交"/>
	</form>
	
</body>
</html>