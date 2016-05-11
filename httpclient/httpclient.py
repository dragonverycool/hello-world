#-*- coding: utf-8 -*-

import json
import sys
import urllib
import urllib2
import xml.etree.ElementTree as ET
import wx
from wx.lib.embeddedimage import PyEmbeddedImage
from wx.lib.pubsub.utils.xmltopicdefnprovider import indent
from threading import Thread
from wx.lib.pubsub import pub as Publisher
import time as mytime
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

xml_Path = "data.xml"
ayg = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABDBJ"
    "REFUWIWtlt9rHFUUxz/nzOymNv1hoRXblFpR2wfRJx/8D3wpFF+aJiXQ9EfiDygUH3zwqfjr"
    "wUoRoVgD2qLVqChafyAiqIgg+CRFsE3atNJfJjEksU22u3vv8WFnJ7O7szOb4oGBmXvPOd/v"
    "/d5z5x4hsqsDQ1vU2WXamLWbyDFpzmM2v3Fbzzo5csTH89f6DrwhIof+T+A8IgVZsXb96Tfn"
    "w6sDQ1vEWQu41R9boiAiqcmSMaTECI0LEaBipTlA5Hr/wYZFJoG9GR6Lo0VAEFQkTkyGPwKa"
    "4h8vwngrTIL7KJEzw3lP1TzBhg0Ut/Rg5QqlP88jlSqhCIEqGinizPCRvxWLrNj+EFIsUL58"
    "hfL0NKEoYeTfoIjwVNgMXvWeivfc+8JzdD/6cKrUf4+c4ub3PxGqYIDzxuodT3DPQG+q/63f"
    "z3LjlWMUVQlUIaGGXO8/aAZ4M6rmKTvHA6PvxPvdzsx7zvUOArD9o3cR1Wx/My7s3kdXEBDI"
    "knpyLSLgvKfsHVvfexsthJnJ7tR8pcKlgWG6NEBVEUDr7LwZtmb1ssDNrOHJMy0UsFXduIR/"
    "rJszz9Zjr3a+mmqVqaHDTA0fbiGUZfcdfQmX8AkBDMMMgu6VucB1AFssYYuLbX3a1VB499qa"
    "2hggEQEjGugMHEBXdSMr76L4SPpJySJBtGAkUqDml1P1KdJ2P7mDFY8/lhmTTkKoD8c1IFI7"
    "Wp2CA9w8/QkzL76WQbs11pxDE5w04kMgwtwPP2cmSzM/OZ3rkyQx88U3tT9ipHiNgAiKMHXi"
    "ZO4K4vFKZdlkAWZGP0OReGsiBUBFCFTwpVJHiaoTfy0L2MxwC4uEGl1O0XiiBoRQlAt7n2kI"
    "ame3z/6x5Hf7dkckLu57lkC0oTAbCAQqhAj/fP51brLSj7/E766DOph8/2NCahjpBKgVY0GF"
    "2Q8/hTYnom5+dm6JzK+/ZaN7z79ffktBa8WXPJgNV5iKoKIUAmW8b3/bY9lsC19913bOnGO8"
    "bz+FQONmpgGzOaBeC0UNGO/b3xGBLLXG+w9Q1ICwae/bE6iTUKVLA8Z6B/HlcjaBlMR+scR4"
    "7yBdGhCqtrRkbQmkkZgYGKZ08VKDz/rjR+P3DaeON8wtnBtjYu/TtZUnwNMUkGtNTWnSDPDe"
    "48yoeIf0bOT+119u5w7AxUPPw+QUBQ0ImprRjraggR3RD0qEogbI1RuM7RrE3Vpo8a3OzjG2"
    "axCdnKbYITjkKFA3M4tbb+c9FfO4YpEHT9akHx8YJnSOUGpNZ0sLntFfdkSgmUS9dff1tipS"
    "SdL6/5zmNjSzeRFZk0dARCC6300EafpNp1V5Hrj37NRN23rW5YE3J6zXRvJZLjjA5tGRMwJw"
    "fs+eNats5VxeQNKyLqpOwDd9MNLah13ZfeCEqgzdKYlOgL1n5+bRkTP17/8Ay4/gDHiq/QoA"
    "AAAASUVORK5CYII=")

APIKEY = None
SECRETKEY = None

class ExamplePanel(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        grid = wx.GridBagSizer(hgap=4, vgap=5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        #接口列表
        # self.lc = wx.ListCtrl(self, -1,size=(200,580), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        # self.lc.InsertColumn(0, u'接口名', width=200)
        # for x in range(len(d)):
        #     self.lc.InsertStringItem(x,d[x])
        self.listBox = wx.ListBox(self, -1,(0,0),(200,800),[], wx.LB_SINGLE)
        #读取xml文件
        tree = ET.parse(xml_Path)
        root = tree.getroot()
        for interface in root.findall('interface'):
            self.listBox.Append(interface.get("name"))
        self.Bind(wx.EVT_LISTBOX, self.ItemClick, self.listBox)

        #接口名
        self.lblName = wx.StaticText(self, label=u"接口名：")
        grid.Add(self.lblName, pos=(0,0))

        #接口名输入框
        self.editName = wx.TextCtrl(self, size=(400,20))
        grid.Add(self.editName, pos=(0,1), span=(1,3))

        # Checkbox debug模式
        self.debug = wx.CheckBox(self, label=u"debug模式", pos=(20,180))
        # self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.debug)
        grid.Add(self.debug, pos=(0,4),flag=wx.EXPAND|wx.RIGHT|wx.LEFT,border=15)

        #地址
        self.lblURL = wx.StaticText(self, label=u"地址URL：")
        grid.Add(self.lblURL, pos=(1,0))

        #地址输入框
        self.editUrl = wx.TextCtrl(self, size=(500,20))
        grid.Add(self.editUrl, pos=(1,1), span=(1,4),border=0)

        #标签页
        self.nb = wx.Notebook(self, size=(570, 450))
        self.jsonPage = cjlists(self.nb)
        self.resultPage = cjview(self.nb)
        self.loginPage = loginTab(self.nb)
        self.nb.AddPage(self.jsonPage, u"JSON参数")
        self.nb.AddPage(self.resultPage, u"运行结果")
        self.nb.AddPage(self.loginPage, u"登录")
        grid.Add(self.nb, pos=(2,0), span=(1,5), border=1)

        # 保存按钮
        self.saveBtn = wx.Button(self, label=u"保存" ,size=(80,30))
        btnSizer.Add(self.saveBtn, flag=wx.LEFT,border=20)
        self.Bind(wx.EVT_BUTTON, self.Save, self.saveBtn)

        # 删除按钮
        self.delBtn = wx.Button(self, label=u"删除",size=(80,30))
        btnSizer.Add(self.delBtn, flag=wx.LEFT,border=30)
        self.Bind(wx.EVT_BUTTON, self.Delete, self.delBtn)

        # 格式化按钮
        self.formatBtn = wx.Button(self, label=u"格式化",size=(80,30))
        btnSizer.Add(self.formatBtn, flag=wx.LEFT,border=30)
        self.Bind(wx.EVT_BUTTON, self.DoFormat, self.formatBtn)

        # 提交按钮
        self.submitBtn =wx.Button(self, label=u"提交",size=(80,30))
        btnSizer.Add(self.submitBtn, flag=wx.LEFT,border=30)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.submitBtn)

        # 关闭按钮
        self.closeBtn =wx.Button(self, label=u"关闭",size=(80,30))
        btnSizer.Add(self.closeBtn,  flag=wx.LEFT,border=30)
        self.Bind(wx.EVT_BUTTON, self.closebutton, self.closeBtn)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

        #登录按钮
        self.Bind(wx.EVT_BUTTON, self.login, self.loginPage.loginBtn)

        #登录框绑定数据
        for login in root.findall('login'):
            self.loginPage.loginURL.Append(login.find("URL").text)
        self.Bind(wx.EVT_COMBOBOX, self.loginSelected, self.loginPage.loginURL)

        grid.Add(btnSizer, pos=(3,0), span=(1,5), flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=0)

        mainSizer.Add(self.listBox)
        mainSizer.Add(grid, 0, wx.ALL, 10)
        self.SetSizerAndFit(mainSizer)

        Publisher.subscribe(self.updateDisplay, "update")
        Publisher.subscribe(self.failDisplay, "fail")

    def updateDisplay(self, msg):
        self.resultPage.result.SetValue(msg)

    def failDisplay(self, msg):
        self.resultPage.result.SetValue(u"请求失败……")
        self.resultPage.result.AppendText(msg)

    def Save(self, event):
        tree = ET.parse(xml_Path)
        root = tree.getroot()
        req = "./interface[@name='{0}']".format(self.editName.GetValue())
        nodes = root.findall(req)
        if len(nodes):
            node = nodes[0]
            if(node.get("name")!=self.listBox.GetStringSelection()):
                dlg = wx.MessageDialog(None, u"接口名已经存在，是否覆盖？", u"提示", wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_NO:
                    return
                dlg.Destroy()
            node.find("URL").text = self.editUrl.GetValue()
            node.find("json").text = self.unformat(self.jsonPage.text.GetValue())
        else:
            node = ET.Element("interface", {'name' : self.editName.GetValue()})
            addressNode = ET.SubElement(node, 'address')
            mothodNode = ET.SubElement(node, 'method')
            URLNode = ET.SubElement(node, 'URL')
            jsonNode = ET.SubElement(node, 'json')
            URLNode.text = self.editUrl.GetValue()
            jsonNode.text = self.jsonPage.text.GetValue()
            root.append(node)
        indent(root)
        tree.write(xml_Path,encoding='utf-8')
        self.listBox.Clear()
        for interface in root.findall('interface'):
            self.listBox.Append(interface.get("name"))

    def Delete(self, event):
        dlg = wx.MessageDialog(None, u"添加一个不容易，确定要删？", u"提示", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_NO:
            return
        dlg.Destroy()
        tree = ET.parse(xml_Path)
        root = tree.getroot()
        req = "./interface[@name='{0}']".format(self.listBox.GetStringSelection())
        node = root.findall(req)[0]
        root.remove(node)
        tree.write(xml_Path,encoding='utf-8')
        self.listBox.Clear()
        self.editUrl.Clear()
        self.editName.Clear()
        self.jsonPage.text.Clear()
        self.resultPage.result.Clear()
        for interface in root.findall('interface'):
            self.listBox.Append(interface.get("name"))

    def DoFormat(self, event):
        selectObj = None
        if(self.nb.GetSelection()==0):
            selectObj = self.jsonPage.text
        else:
            selectObj = self.resultPage.result
        try:
            # eval(param)
            param = selectObj.GetValue()
            if param.strip() == "":
                return
            param = json.loads(param)
        except Exception,e :
            self.nb.SetSelection(1)
            self.resultPage.result.SetValue(e.message)
            return
        selectObj.SetValue(json.dumps(param , indent=4, ensure_ascii=False))

    def ItemClick(self, event):
        # self.listBox.GetStringSelection(ensure_ascii=False)
        self.editName.Clear()
        self.editUrl.Clear()
        self.jsonPage.text.Clear()
        self.resultPage.result.Clear()
        self.nb.SetSelection(0)
        tree = ET.parse(xml_Path)
        root = tree.getroot()
        req = "./interface[@name='{0}']".format(self.listBox.GetStringSelection())
        node = root.findall(req)[0]
        if node.get("name") != None:
            self.editName.SetValue(node.get("name"))
        if node.find("URL").text != None:
            self.editUrl.SetValue(node.find("URL").text)
        if node.find("json").text != None:
            self.jsonPage.text.SetValue(node.find("json").text)

    def loginSelected(self, event):
        self.loginPage.loginName.Clear()
        self.loginPage.loginPwd.Clear()
        self.nb.SetSelection(2)
        tree = ET.parse(xml_Path)
        root = tree.getroot()
        req = "./login[URL='{0}']".format(self.loginPage.loginURL.GetValue())
        node = root.findall(req)[0]
        if node.find("account").text != None:
            self.loginPage.loginName.SetValue(node.find("account").text)
        if node.find("pwd").text != None:
            self.loginPage.loginPwd.SetValue(node.find("pwd").text)

    def OnSubmit(self, event):
        if self.editUrl.GetValue().strip()=="":
            return
        self.nb.SetSelection(0)
        self.resultPage.result.SetValue(u"请求已提交，等待响应……")
        self.nb.SetSelection(1)
        try:
            global APIKEY
            global SECRETKEY
            url = self.editUrl.GetValue().replace("http://","")
            req = urllib2.Request("http://{0}".format(url))
            if APIKEY != None:
                timestamp =  long(mytime.time()*1000)
                req.add_header('apikey', APIKEY)
                loginList = [str(timestamp), SECRETKEY, APIKEY]
                loginList.sort()
                # if(SECRETKEY<APIKEY):
                req.add_header('sign', self.get_md5_value(str(loginList)))
                # else:
                #     req.add_header('sign', self.get_md5_value(str(timestamp) + APIKEY + SECRETKEY))
                req.add_header('timestamp', timestamp)
            if self.debug.IsChecked():
                time = 10000
            else:
                time = 3
            if(self.jsonPage.text.GetValue().strip()==""):
                # response = urllib2.urlopen(req, timeout=time)
                HttpThread(req, None, time)
            else:
                params = urllib.urlencode(json.loads(self.jsonPage.text.GetValue()))
                # response = urllib2.urlopen(req, params, timeout=time)
                HttpThread(req, params, time)
            # self.resultPage.result.SetValue(response.read().decode('utf-8'))
        except Exception, e:
            print e
            self.resultPage.result.SetValue(u"请求失败……")
            self.resultPage.result.AppendText(e.message)
            self.nb.SetSelection(1)
        # finally:
        #     if httpClient:
        #         httpClient.close()
        print "Done"
        # global method

    def get_md5_value(self, src):
        myMd5 = hashlib.md5()
        myMd5.update(src)
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    def login(self, event):
        global APIKEY
        global SECRETKEY
        try:
            loginParam = {"username":self.loginPage.loginName.GetValue(),"password":self.loginPage.loginPwd.GetValue()}
            url = self.loginPage.loginURL.GetValue().replace("http://","")
            req = urllib2.Request("http://{0}".format(url))
            params = urllib.urlencode(loginParam)
            response = urllib2.urlopen(req, params, 3)
            resultStr = response.read().decode('utf-8')
            result = json.loads(resultStr)
            if result["logined"] == True:
                APIKEY = result["apikey"]
                SECRETKEY = result["secretkey"]
            self.resultPage.result.SetValue(resultStr)
        except Exception, e:
            print e
            self.resultPage.result.SetValue(u"请求失败……")
            self.resultPage.result.AppendText(e.message)
        finally:
            self.nb.SetSelection(1)

    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for e in elem:
                indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        return elem

    def unformat(self,str):
        return "".join(str.split())

    def closebutton(self, event):
        self.Parent.Close(True)

    def closewindow(self, event):
        self.Parent.Destroy()

# Json参数页
class cjlists(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_THEME)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.EXPAND|wx.BORDER_NONE|wx.TE_PROCESS_TAB)
        self.sizer.Add(self.text,proportion=1,flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=0)
        self.SetSizer(self.sizer)
        # wx.StaticText(self,label='Absolute Positioning1')
        pass

#结果页
class cjview(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_THEME)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.result = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.EXPAND|wx.BORDER_NONE|wx.CB_READONLY|wx.TE_READONLY)
        self.result.SetBackgroundColour("#C9D2A4")
        self.sizer.Add(self.result,proportion=1,flag=wx.LEFT|wx.RIGHT|wx.EXPAND,border=0)
        self.SetSizer(self.sizer)
        pass

class loginTab(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_THEME)
        self.grid = wx.GridBagSizer(hgap=4, vgap=2)

        self.lblURL = wx.StaticText(self, label=u"登录地址：")
        self.grid.Add(self.lblURL, pos=(0,0))

        self.loginURL = wx.ComboBox(self, size=(350, -1), style=wx.CB_DROPDOWN) #choices=self.sampleList
        self.grid.Add(self.loginURL, pos=(0,1))

        self.lblName = wx.StaticText(self, label=u"帐号：")
        self.grid.Add(self.lblName, pos=(1,0))

        self.loginName = wx.TextCtrl(self, size=(200,20))
        self.grid.Add(self.loginName, pos=(1,1))

        self.lblPwd = wx.StaticText(self, label=u"密码：")
        self.grid.Add(self.lblPwd, pos=(2,0))

        self.loginPwd = wx.TextCtrl(self, size=(200,20))
        self.grid.Add(self.loginPwd, pos=(2,1))

        self.loginBtn =wx.Button(self, label=u"登录",size=(80,30))
        self.grid.Add(self.loginBtn, pos=(3,0))

        self.SetSizer(self.grid)
        pass

class HttpThread(Thread):
    def __init__(self, req, params=None, timeout=3):
        """Init Worker Thread Class."""
        self.req = req
        self.timeout = timeout
        self.params = params
        Thread.__init__(self)
        self.start()    # start the thread
    def run(self):
        # This is the code executing in the new thread.
        try:
            if self.params!=None:
                response = urllib2.urlopen(self.req, self.params, self.timeout)
            else:
                response = urllib2.urlopen(self.req, timeout=self.timeout)
            wx.CallAfter(Publisher.sendMessage, topicName="update", msg=response.read().decode('utf-8'))
        except Exception, e:
            print e
            wx.CallAfter(Publisher.sendMessage, topicName="fail", msg=e.message.decode('utf-8'))

app = wx.App(False)
frame = wx.Frame(None,-1, title=u'接口测试2.0--哥就像巴黎欧莱雅 你值得拥有', size=(800,600))
# frame.SetIcon(wx.Icon("ayg.ico",wx.BITMAP_TYPE_ICO))
frame.SetIcon(ayg.GetIcon())
panel = ExamplePanel(frame)
frame.Center()
frame.Show()
app.MainLoop()