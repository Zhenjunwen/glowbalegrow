# -*- coding: utf-8 -*-

import requests
import json
import time
from model import Apitest_domain
from db import DBSession
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 创建session对象:
session = DBSession()
s = requests.Session()

url = 'http://user.kuaizi.co'

loginjson = open("loginready.json")
logindata = json.load(loginjson)["RECORDS"]

print "【%s】%s" % (str(logindata[0]['Request_Method']), str(logindata[0]['Document']))
loginmain = s.post(logindata[0]['Request_URL'], data=logindata[0]['Request_Data'])
print loginmain.status_code
#print loginmain.text
#print s.headers

print "【%s】%s" % (str(logindata[1]['Request_Method']), str(logindata[1]['Document']))
loginurl = url + logindata[1]['Request_URL'] + s.cookies.get_dict()['PHPSESSID']
print loginurl
loginglbg = s.get(loginurl)
print loginglbg.status_code
#print loginglbg.text
token = loginglbg.url.rsplit("=")[1]
#print token
s.headers.update({'token': token})  # 把token加入session的headers
#print s.headers



l = open("get_last_synch_time.json")
last_synch_time = json.load(l)["RECORDS"]


def makeGET(rqset):
    # query = session.query(Apitest_domain.id, Apitest_domain.name)
    # query = session.query(Apitest_domain)
    # rqset = query.all()[1]
    #rqset = last_synch_time[0]
    if rqset['Request_Method'] == "GET":
        print "【%s】%s" % (rqset['Request_Method'], rqset['Document'])
        req = s.get(url+rqset['Request_URL'], params=rqset['Request_Params'])  #params传递明文参数
        #print req.url
        print req.text
        #print req.status_code
        assert(200 == req.status_code)
        #reqdict = json.loads(req.text.decode(errors="strict"))
        #getdictassert(reqdict, rqset)

    elif rqset['Request_Method'] == "POST":
        print "【%s】%s" % (rqset['Request_Method'], rqset['Document'])
        req = s.post(url+rqset['Request_URL'], params=rqset['Request_Params'], data=rqset['Request_Data'])  # params传递明文参数
        print req.text
        print req.status_code
        assert (200 == req.status_code)
        reqdict = json.loads(req.text.decode(errors="strict"))
        #print reqdict
        getdictassert(reqdict, rqset)
    else:
        print "【%s】%s【没有请求】" % (rqset['Request_Method'], rqset['Document'])




def getdictassert(reqdict, rqset):
    print rqset["assertRq"]
    print rqset["assertExpect"]
    numofassert = len(rqset["assertRq"])
    print numofassert
    for i in range(numofassert):
        print "========="
        print i
        print rqset["assertRq"][i]
        assertRq = getdictvalue(reqdict, len(rqset["assertRq"][i]), rqset["assertRq"][i])
        assert(assertRq == rqset["assertExpect"][i]), str(assertRq) + "不等于" + str(rqset["assertExpect"][i])


def getdictvalue(a, b, c, n=-1):  # a是返回参数的字典形式，b是字典层级数，c是字典key列表，n是计数器
    n = n + 1
    if b == 1:
        print a[c[0]]
        return a[c[0]]
    elif b == n:
        print "req_value=", a
        return a
    else:
        print "n=", n
        print "dict_key=", c[n]
        try:
            getpara = a[c[n]]
        except (TypeError, KeyError), e:
            print e
            print "没有这个参数["+c[n]+"]"
            time.sleep(.5)
        # print b, n
        return getdictvalue(getpara, b, c, n)

for i in last_synch_time:
    makeGET(i)


# getdictpara()