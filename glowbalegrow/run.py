#coding=utf-8
import unittest
import time

import os
import requests
import json
from tools import HTMLTestRunner_oujn, sendemail
from tools.AutoRequests import AutoRequests
import sys
sys.path.append("\\testcases")
import os
import traceback


env = "PD"
emailmode = 0
#filenames = ['loaddata/GbegUser/creative_pool.json']
filenames = 'loaddata'
reportpath = "report/"


setupdata = "loaddata/loginready.json"
if env == "DEV":
    rqurl = "http://dev.user.kuaizi.co"
    loginurl = "http://dev.www.kuaizitech.com"
elif env == "DEV2":
    rqurl = "http://dev2.user.kuaizi.co"
    loginurl = "http://dev2.www.kuaizitech.com"
elif env == "TEST":
    rqurl = "http://test.user.kuaizi.co"
    loginurl = "http://test.www.kuaizitech.com"
else:
    rqurl = "https://user.kuaizi.co"
    loginurl = "http://www.kuaizitech.com"



# 遍历指定目录，显示目录下的所有文件名
def makejson2testsuit(filepath='loaddata'):
    print('\n[导入目录]开始遍历指定目录，接收的目录为：'+ str(filepath))
    testsuitdata = []
    if filepath == 'loaddata':
        print('\n[导入目录]默认导入全目录：' + str(filepath))
        allDir = list(map(lambda x:os.path.join('%s/%s' % (filepath, x)),os.listdir(filepath))) #listdir方法列出文件夹下全部文件和文件夹名字，用list装起来
        print(allDir)
        allDir = list(filter(lambda x: os.path.isdir(x),allDir))
        print(allDir)
        arry = maketestsuitforpath(allDir)

        print("===")
        print(arry)
        return arry
        for dirinparh1 in allDir:
            arry = []
            testcasedata = {}
            #child = os.path.join('%s/%s' % (filepath, dirinparh1)) #path.join方法，拼出第一级目录下的文件的相对路径
            print(child)
            #遍历第一级目录，过滤出文件夹，对文件夹下的json文件进行搜索
            if os.path.isfile(child):   #os.path.isfile()方法判断这个这个目录，是不是文件
                print(child+"是个文件，跳过")
                continue
            else:
                #print(child +':是个目录，进行二级目录收集json文件')
                testsuitdata = maketestsuitforpath(child)
                print(testsuitdata)
                # modulepath = os.listdir(child)  #列出文件夹下的所有文件，用list装起来
                # testcasedata["module"] = dirinparh1 #先把文件夹的名字存入字典
                # for modules in modulepath:  #遍历二级目录下的所有文件，记录json格式文件
                #     module = os.path.join('%s/%s' % (child, modules))
                #     arry = maketestsuitforfile(module,arry)
                # testcasedata["datapath"] = arry
            testsuitdata.append(testcasedata)
    else:
        testsuitdata = maketestsuitforpath(filepath)
    return testsuitdata


def maketestsuitforpath(filenames):
    print(filenames)
    testsuitdata = []
    for i in filenames:
        print(i)
        parhtosearch = i.split('/') #分隔传入的路径，看是2级还是3级
        arry = []
        testcasedata = {}
        #testcasedata["module"] = parhtosearch[1]
        if len(parhtosearch) == 2:
            arry  = maketestsuitfordir(i)
        elif len(parhtosearch) == 3:
            arry = maketestsuitforfile(i,arry)
        testcasedata["datapath"] = arry
        testsuitdata.append(testcasedata)
    return testsuitdata


def maketestsuitforfile(i,arry):
    if os.path.splitext(i)[1] in ['.json']:  # path.splitext方法，截断目录和后缀名，返回一个list
        arry.append(i)
    return arry


def maketestsuitfordir(i):
    print(i)
    arry = []
    modulepath = os.listdir(i)
    for modules in modulepath:  # 遍历二级目录下的所有文件，记录json格式文件
        module = os.path.join('%s/%s' % (i, modules))
        maketestsuitforfile(module, arry)
    return arry


def import_class(import_str):
    """Returns a class from a string including module and class.

    .. versionadded:: 0.3
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))

def improt_allclass(testsuitdata):
    print("\n开始批量导入class...")
    testcasepath = 'testcases'
    testsuitname = []
    for testcasedata in testsuitdata:
        modulename = testcasedata["module"]
        importname = import_class(testcasepath + '.' + modulename + '.' + modulename)
        #print(importname)
        testcasedata["moduleclass"] = importname
        testsuitname.append(importname)
    return testsuitname

def maketestsuit(testsuitdata):
    print("\n开始为class导入json用例...")
    for testsuit in testsuitdata:
        modulename = testsuit["moduleclass"]
        jsoncase = testsuit["datapath"]
        a = 1
        for i in jsoncase:
            jsonraw = json.load(open(i, encoding="utf-8"))
            if jsonraw["skip"] == True:
                print("跳过")
                continue
            jsondata = jsonraw["RECORDS"]
            filename = jsonraw["filename"]
            print(i + str(len(jsondata)))
            b = 1
            for j in jsondata:
                num = ('0000' + str(b))[-3::]
                funcname = "test_func_%s_%s_%s" % (a, filename, num)
                print(funcname + "【%s】%s" % (j['Request_Method'], j['Document']))
                setattr(modulename, funcname,
                        modulename.getTestFunc(j, filename))  # 通过setattr自动为TestCase类添加成员方法，方法以“test_func_”开头
                modulename.loginurl = loginurl
                modulename.rqurl = rqurl
                modulename.setupdata = setupdata
                b += 1
            a = a + 1
        #print(modulename.__dict__)

if __name__ == '__main__':
    testsuitdata = makejson2testsuit(filenames)
    #print(testsuitdata)
    testsuitlist = improt_allclass(testsuitdata)
    print(testsuitlist)
    maketestsuit(testsuitdata)
    testunit = unittest.TestSuite()
    for importname in testsuitlist:
        testunit.addTest(unittest.makeSuite(importname))

    if emailmode == 0:
        print("文字模式")
        runner = unittest.TextTestRunner()
        runner.run(testunit)

    elif emailmode == 1:
        # 定义个报告存放路径，支持相对路径
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        filename = reportpath + "%sresult%s.html" % (env, now)
        fp = open(filename, 'wb')
        reportpath = filename
        print(reportpath)

        # 定义测试报告
        runner = HTMLTestRunner_oujn.HTMLTestRunner(stream=fp, title=u'环球易购接口监控报告', description=u'用例执行情况：', verbosity=2)
        # 运行测试用例
        getresult = runner.run(testunit)
        time.sleep(1)
        fp.close()
        print(getresult.failure_count)
        print(getresult.error_count)

        if getresult.failure_count != 0 or getresult.error_count != 0:
            sendemail.send_email(filename, env)


