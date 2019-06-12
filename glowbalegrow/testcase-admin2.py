#coding=utf-8
import unittest
import time
import datetime
import requests
import json,re
from tools import HTMLTestRunner_oujn, sendemail
from tools.asserttool import getdictassert


env = "PD"
emailmode = 0




if env == "DEV":
    rqurl = "http://dev.user.kuaizi.co"
    loginurl = "http://dev.www.kuaizitech.com"
elif env == "DEV2":
    rqurl = "http://dev2.user.kuaizi.co"
    loginurl = "http://dev.www.kuaizitech.com"
elif env == "TEST":
    rqurl = "http://test.user.kuaizi.co"
    loginurl = "http://test.www.kuaizitech.com"
else:
    rqurl = "https://user.kuaizi.co"
    loginurl = "http://www.kuaizitech.com"



setupdata = "loaddata/loginready.json"
allcase = ["loaddata/tagManager.json"] # 测试用
allcase1 = ["loaddata/common.json",
           "loaddata/creative_selection_pool.json",
           "loaddata/creative_pool.json",
           "loaddata/autoPush.json",
           "loaddata/dccenter.json",
           "loaddata/dccenter_banner.json",
           "loaddata/dccenter_carousel.json",
           "loaddata/productlib.json"
           "loaddata/tagManager.json"
           ]
reportpath = "report/"


class MyTestCase(unittest.TestCase):
    reportpath = ""
    auto_send_email = 0

    @classmethod
    def setUpClass(self):
        print("测试初始化")
        self.s = requests.Session()
        self.verificationErrors = []
        self.verificationTimeout = []
        self.verificationFomat = []
        time.sleep(1)
        logindata = json.load(open(setupdata,encoding="utf-8"))["RECORDS"]   # 加载登录数据

        # 登录后台
        print("【%s】%s" % (logindata[0]['Request_Method'], logindata[0]['Document']))
        reqlogin = self.s.post(loginurl+logindata[0]['Request_URL'], data=logindata[0]['Request_Data'])
        print(reqlogin.status_code)  # 获取加载code
        assert (200 == reqlogin.status_code)  # 断言连接是否成功
        if reqlogin.status_code != 200:
            self.verificationErrors.append(("loginready", logindata[1]['Request_Method'], logindata[1]['Document']))

        ssid = re.findall('=([\s\S]*?);', reqlogin.headers["Set-Cookie"])[0]


        # 登录广告主后台
        print("【%s】%s" % (logindata[1]['Request_Method'], logindata[1]['Document']))
        reqlogin = self.s.get(rqurl + logindata[1]['Request_URL'] + ssid, data=logindata[1]['Request_Data'])
        print(reqlogin.url)
        token = re.findall('token=([\s\S]*)', reqlogin.url)[0]
        print(token)
        self.s.headers.update({'token': token})  # 把token加入session的headers

        print(reqlogin.status_code)  # 获取加载code
        assert (200 == reqlogin.status_code)  # 断言连接是否成功
        if reqlogin.status_code != 200:
            self.verificationErrors.append(("loginready", logindata[1]['Request_Method'], logindata[1]['Document']))

        print("\n登录完成\n------------")

    def setUp(self):
        pass

    def clear(self):
        pass

    def getTest(self, rqset, funcname):  # 定义的函数，最终生成的测试用例的执行方法
        # print(funcname)
        start = datetime.datetime.now()
        try:
            if rqset['Request_Method'] == "GET":
                print("【%s】%s" % (rqset['Request_Method'], rqset['Document']))
                req = self.s.get(rqurl+rqset['Request_URL'], params=rqset['Request_Params'])  # params传递明文参数
            elif rqset['Request_Method'] == "POST":
                print("【%s】%s" % (rqset['Request_Method'], rqset['Document']))
                req = self.s.post(rqurl + rqset['Request_URL'], params=rqset['Request_Params'], data=rqset['Request_Data'])  # params传递明文参数
            else:
                print("【%s】%s【没有请求】" % (rqset['Request_Method'], rqset['Document']))
        except:
            print("ConnectionError:连接失败，尝试重新连接")
            raise "ConnectionError:连接失败，尝试重新连接"

        end = datetime.datetime.now()
        usingtime = (end - start).total_seconds()
        print(req.status_code, usingtime)

        if req.status_code != 200:
            self.verificationErrors.append((funcname, rqset['Request_Method'], rqset['Document']))
        elif usingtime > 3:
            self.verificationTimeout.append((funcname, rqset['Request_Method'], rqset['Document'], usingtime))
        assert (200 == req.status_code), "返回码是%s:【%s】%s" %(str(req.status_code), rqset['Request_Method'], rqset['Document'])



        try:
            json.loads(req.text)
        except json.JSONDecodeError as e:
            self.verificationFomat.append((funcname, rqset['Request_Method'], rqset['Document']))
            assert (e == None), "【%s】%s\n返回数据格式不正确\n接口：%s\n返回：%s" % (rqset['Request_Method'], rqset['Document'],rqset['Request_URL'], req.text)
            raise e

        if len(rqset["assertRq"]) != 0:
            a, e = getdictassert(req.text, rqset)  # 传入返回数据，进行判断
            if e is not None:
                a = (funcname,) + a
                self.verificationErrors.append(a)
                raise e




    @staticmethod
    def getTestFunc(arg1, funcname):
        def func(self):
            self.getTest(arg1, funcname)
            #testtest(arg1)
        return func

    def tearDown(self):
        #print self.verificationErrors
        pass

    @classmethod
    def tearDownClass(self):
        #print "class tearDown"
        time.sleep(1)
        if self.verificationTimeout != []:
            print("======超过3秒的接口======")
            for funcname, method, doc, usingtime in self.verificationTimeout:
                print(funcname, method, doc, usingtime)

        if self.verificationFomat != []:
            print("======格式错误的接口======")
            for funcname, method, doc in self.verificationFomat:
                print(funcname, method, doc)

        if self.verificationErrors != []:
            print("======有问题的接口======")
            for funcname, method, doc in self.verificationErrors:
                print(funcname, method, doc)
            print("需要发送邮件")
            MyTestCase.auto_send_email = 1
        else:
            print("全部通过！")
        time.sleep(1)
        #print self.verificationErrors


class GenerateTestSuit():
    def __init__(self, casename):
        self.case = casename

    def generateTestCases(self):
        a = 1
        for i in self.case:
            jsonraw = json.load(open(i, encoding="utf-8"))
            jsondata = jsonraw["RECORDS"]
            self.filename = jsonraw["filename"]
            print(i + str(len(jsondata)))
            b = 0
            d = 0
            c = 1
            for j in jsondata:
                if c == 10:
                    c = 0
                    b = b + 1
                    if b == 10:
                        b = 0
                        d = d + 1
                funcname = "test_func_%s_%s_%s%s%s" % (a, self.filename, d, b, c)
                print(funcname + "【%s】%s" % (j['Request_Method'], j['Document']))
                setattr(MyTestCase, funcname, MyTestCase.getTestFunc(j, self.filename))  # 通过setattr自动为TestCase类添加成员方法，方法以“test_func_”开头
                c = c + 1


            a = a + 1



if __name__ == '__main__':

    #加载json文件，把测试数据加载进去
    __sample = GenerateTestSuit(allcase)
    __sample.generateTestCases()

    # __generateTestCases()


    #unittest.main()
    # pass

    #定义一个单元测试容器
    testunit = unittest.TestSuite()

    #将测试用例加入到测试容器中
    testunit.addTest(unittest.makeSuite(MyTestCase))

    if emailmode == 1:
        #定义个报告存放路径，支持相对路径
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        filename = "report/%sresult%s.html" % (env, now)
        fp = open(filename, 'wb')
        MyTestCase.reportpath = filename
        print(MyTestCase.reportpath)

        #定义测试报告
        runner = HTMLTestRunner_oujn.HTMLTestRunner(stream=fp, title=u'环球易购接口监控报告', description=u'用例执行情况：', verbosity=2)
        # 运行测试用例
        runner.run(testunit)
        # print("结束")
        # print(MyTestCase.verificationErrors)
        time.sleep(1)
        fp.close()

        if MyTestCase.auto_send_email == 1:
            sendemail.send_email(filename, env)
    else:
        runner = unittest.TextTestRunner()
        # 运行测试用例
        runner.run(testunit)
