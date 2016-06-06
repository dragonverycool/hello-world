package com.createw.lunch.servlet;

import java.text.SimpleDateFormat;
import java.util.Date;


public class Util {

	//订餐数据文件保存位置
	public final static String FILE_PATH = "/opt/data.xml";
	
	//版本文件保存位置
//	private static final String PROPERTY_FILE = "/opt/version.properties";  
	
//	public final static String FILE_PATH = "d:/data.xml";
	
	//获取当前日期的字符格式
	public static String getDateString(){
		return new SimpleDateFormat("yyyyMMdd").format(new Date());
	}
	
	//获取当前日期的字符格式
	public static String getDateTimeString(){
		return new SimpleDateFormat("yyyyMMddHHmmss").format(new Date());
	}
	
	
}
