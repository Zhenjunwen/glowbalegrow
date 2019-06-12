import datetime
import json


class AutoRequests:
    # def __init__(self,mainself):
    #     self.mainself = mainself

    def trytorequest(self):
        print("【%s】%s" % (self.method, self.doc))
        self.starttime = datetime.datetime.now()
        try:
            if self.method == "GET":
                self.req = self.s.get(self.url, params=self.params)  # params传递明文参数
            elif self.method == "POST":
                self.req = self.s.post(self.url, params=self.params, data = self.data)  # params传递明文参数
            else:
                print("请检查请求方法是否正确")
                raise AssertionError("请求方法不对")
        except AssertionError as e:
            print("ConnectionError:连接失败，尝试重新连接")
            raise e
        #print(json.loads(self.req.text))
        self.endtime = datetime.datetime.now()
        self.usingtime = (self.endtime - self.starttime).total_seconds()
        print(self.req.status_code, self.usingtime)
        try:
            self.reqdict = json.loads(self.req.text)
        except json.JSONDecodeError:
            print('返回的不是json格式')


    def assertmethod(self, type):
        if type =='eq':
            return self.assertEqual
        elif type =='in':
            pass
        elif type =='gt':
            pass
        elif type =='lt':
            pass
        else:
            raise AssertionError("用例指定的断言方法不对")

    def errornoter(self, type, note):
        errordoc = self.funcname + ' '+ self.method + ' '+ self.doc
        if type == 'error':
            self.verificationErrors.append((errordoc, note))
        elif type == 'timeout':
            self.verificationTimeout.append((errordoc, note))


    def validator(self):
        if self.req.status_code !=200:
            self.errornoter('error', '状态码是%d' % self.req.status_code)
            # raise AssertionError("状态码不对")

        if self.usingtime > 1 :
            # print(self.usingtime)
            self.errornoter('timeout', '%s秒' % self.usingtime)

        if self.validate == [{}]:
            print("没有配置断言")
            return

        for i in self.validate:
            method = list(i.keys())[0]
            #print(i)
            listofkey = i[method][0].split('.')
            #print(listofkey)
            reqvalue = self.getdictvalue(self.reqdict, listofkey)
            # print(reqvalue)
            expectvalue = i[method][1]
            assertor = self.assertmethod(method)
            self.assertor(assertor, reqvalue, expectvalue)

    def assertor(self, assertor, reqvalue, expectvalue):
        try:
            assertor(reqvalue, expectvalue,
                     msg="【%s】%s\n(%s)不等于(%s)\n接口：%s\n返回：%s" %
                         (self.method, self.doc, str(reqvalue)[0:40], str(expectvalue)[0:40], self.uri, str(self.reqdict)))
        except AssertionError as e:
            self.errornoter('error', e)
            raise e

    def getdictvalue(self, reqraw, list):  # a是返回参数的字典形式，b是字典层级数，c是字典key列表，n是计数器
        #print("----------")
        #print("list个数", len(list))
        if len(list) ==1 :
            return reqraw[list[0]]
        try:
            if isinstance(reqraw, dict):
                #print(list[0])
                newreqraw = reqraw[list[0]]
            else:
                #print(int(list[0]))
                newreqraw = reqraw[int(list[0])]
                # print(newreqraw)
        except (TypeError, KeyError, IndexError) as e:
            errornote = str(e) + "；没有这个参数[" + list[0] + "]"
            # print(errornote)
            # time.sleep(.5)
            return errornote

        newlist = list[1::]
        #print(newlist)
        #print("list个数", len(newlist))
        if newlist == []:
            return newreqraw
        return self.getdictvalue(newreqraw, newlist)