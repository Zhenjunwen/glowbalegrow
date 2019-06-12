#coding=utf-8
import unittest
import time
import requests
import json
from tools.AutoRequests import AutoRequests



class GbegUser(unittest.TestCase, AutoRequests):
    loginurl = ''
    rqurl = ''
    setupdata = ''
    @classmethod
    def setUpClass(cls):
        print("测试初始化")
        cls.s = requests.Session()
        cls.verificationErrors = []
        cls.verificationTimeout = []
        time.sleep(1)
        logindata = json.load(open(GbegUser.setupdata,encoding="utf-8"))["RECORDS"]   # 加载登录数据

        #登录后台
        print("【%s】%s" % (logindata[2]['Request_Method'], logindata[2]['Document']))
        reqlogin = cls.s.post(GbegUser.rqurl+logindata[2]['Request_URL'], data=logindata[2]['Request_Data'])
        print(reqlogin.url)
        # print(reqlogin.text)
        if reqlogin.status_code != 200:
            cls.verificationErrors.append(("loginready", logindata[2]['Request_Method'], logindata[2]['Document']))
        token = json.loads(reqlogin.text)["data"]["token"] # 获取token
        cls.s.headers.update({'token': token})  # 把token加入session的headers

        print(reqlogin.status_code)  # 获取加载coed
        assert (200 == reqlogin.status_code)  # 断言连接是否成功
        print("------------")

    def setUp(self):
        pass

    def clear(self):
        pass

    def getTest(self, rqset, funcname):  # 定义的函数，最终生成的测试用例的执行方法
        self.funcname = funcname
        self.method = rqset['Request_Method']
        self.doc = rqset['Document']
        self.uri = rqset['Request_URL']
        self.url = GbegUser.rqurl + self.uri
        self.params = rqset['Request_Params']
        self.data = rqset['Request_Data']
        self.validate = rqset['validate']

        # 开始请求
        self.trytorequest()
        self.validator()


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
    def tearDownClass(cls):
        #print "class tearDown"
        time.sleep(1)
        if cls.verificationTimeout != []:
            print("======超过1秒的接口======")
            for errordoc, note in cls.verificationTimeout:
                print(errordoc, note)

        if cls.verificationErrors != []:
            print("======有问题的接口======")
            #print(cls.verificationErrors)
            for errordoc in cls.verificationErrors:
                print(errordoc[0])
            print("需要发送邮件")
            GbegUser.auto_send_email = 1
        else:
            print("全部通过！")
        time.sleep(1)
        #print self.verificationErrors

# # 生成测试用例
# class GenerateTestSuit():
#     def __init__(self, casename):
#         self.case = casename
#
#     def generateTestCases(self):
#         a = 1
#         for i in self.case:
#             jsonraw = json.load(open(i, encoding="utf-8"))
#             jsondata = jsonraw["RECORDS"]
#             self.filename = jsonraw["filename"]
#             print(i + str(len(jsondata)))
#             b = 0
#             c = 1
#             for j in jsondata:
#                 if c == 10:
#                     c = 0
#                     b = b + 1
#                 funcname = "test_func_%s_%s_%s%s" % (a, self.filename, b, c)
#                 print(funcname + "【%s】%s" % (j['Request_Method'], j['Document']))
#                 setattr(GbegUser, funcname, GbegUser.getTestFunc(j, self.filename))  # 通过setattr自动为TestCase类添加成员方法，方法以“test_func_”开头
#                 c = c + 1
#             a = a + 1



#if __name__ == '__main__':

    #加载json文件，把测试数据加载进去
    # __sample = GenerateTestSuit(allcase)
    # __sample.generateTestCases()

    # __generateTestCases()


    #unittest.main()
    # pass

    #定义一个单元测试容器
    # testunit = unittest.TestSuite()
    #
    # #将测试用例加入到测试容器中
    # testunit.addTest(unittest.makeSuite(GbegUser))
    #
    # if emailmode == 1:
    #     #定义个报告存放路径，支持相对路径
    #     now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
    #     filename = reportpath + "%sresult%s.html" % (env, now)
    #     fp = open(filename, 'wb')
    #     reportpath = filename
    #     print(reportpath)
    #
    #     #定义测试报告
    #     runner = HTMLTestRunner_oujn.HTMLTestRunner(stream=fp, title=u'环球易购接口监控报告', description=u'用例执行情况：', verbosity=2)
    #     # 运行测试用例
    #     runner.run(testunit)
    #     # print("结束")
    #     # print(MyTestCase.verificationErrors)
    #     time.sleep(1)
    #     fp.close()
    #
    #     if GbegUser.auto_send_email == 1:
    #         sendemail.send_email(filename, env)
    # else:
    #     runner = unittest.TextTestRunner()
    #     # 运行测试用例
    #     runner.run(testunit)
