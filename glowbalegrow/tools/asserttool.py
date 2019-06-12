#coding=utf-8

import time, json


# 拿指定的数据和返回的数据进行比较
def getdictassert(reqraw, rqset):
    reqdict = json.loads(reqraw)
    numofassert = len(rqset["assertRq"])
    for i in range(numofassert):
        assertRq = getdictvalue(reqdict, len(rqset["assertRq"][i]), rqset["assertRq"][i])
        if assertRq == None:
            print (reqraw)
        try:
            assert(assertRq == rqset["assertExpect"][i]), "【%s】%s\n(%s)不等于(%s)\n接口：%s\n返回：%s" % (rqset['Request_Method'], rqset['Document'], str(assertRq)[0:20], str(rqset["assertExpect"][i])[0:20], rqset['Request_URL'], reqraw)
        except AssertionError as e:
            return (rqset['Request_Method'], rqset['Document']), e
    return None, None


# 进入配置的json提取用于校对的数据
def getdictvalue(a, b, c, n=-1):  # a是返回参数的字典形式，b是字典层级数，c是字典key列表，n是计数器
    n = n + 1
    if b == 1:
        # print a[c[0]]
        return a[c[0]]
    elif b == n:
        # print "req_value=", a
        return a
    else:
        #print "n=", n
        #print "dict_key=", c[n]
        try:
            getpara = a[c[n]]
        except (TypeError, KeyError, IndexError) as e:
            print(e)
            print(a)
            print ("没有这个参数["+c[n]+"]")
            time.sleep(.5)
            return None
        # print b, n
        return getdictvalue(getpara, b, c, n)
