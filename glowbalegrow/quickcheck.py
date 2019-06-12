import json

import re
import requests
import time



sku = "330641301"
type = ["banner","carousel"]

s = requests.Session()
#time.sleep(1)
f = open("loaddata\loginready.json",encoding="utf-8")
print("测试初始化")

logindata = json.load(f,encoding="utf-8")["RECORDS"]   # 加载登录数据
loginurl = 'http://dev.www.kuaizitech.com'
rqurl = 'http://dev.user.kuaizi.co'
#print(logindata)

# 登录后台
print("【%s】%s" % (logindata[0]['Request_Method'], logindata[0]['Document']))
reqlogin = s.post(loginurl+logindata[0]['Request_URL'], data=logindata[0]['Request_Data'])
print(reqlogin.status_code)  # 获取加载code
assert (200 == reqlogin.status_code)  # 断言连接是否成功

ssid = re.findall('=([\s\S]*?);', reqlogin.headers["Set-Cookie"])[0]
print("\n登录完成\n------------")

# 登录广告主后台
print("【%s】%s" % (logindata[1]['Request_Method'], logindata[1]['Document']))
reqlogin = s.get(rqurl + logindata[1]['Request_URL'] + ssid, data=logindata[1]['Request_Data'])
#print(reqlogin.url)
token = re.findall('token=([\s\S]*)', reqlogin.url)[0]
#print(token)
s.headers.update({'token': token})  # 把token加入session的headers

print(reqlogin.status_code)  # 获取加载code
assert (200 == reqlogin.status_code)  # 断言连接是否成功




# 获取账号和id
#print("【%s】%s" % (logindata[1]['Request_Method'], logindata[1]['Document']))
projecturl = '/report/v2/Pub/getProjectAndCampaign'
projectdata = s.get(rqurl + projecturl)
projectdict = json.loads(projectdata.text)
projectarry = []
for i in projectdict["data"]:
    projectarry.append([i["project_id"],i["project_name"]])



#获取产品id
producturl = '/tool/ProductRepository/queryProduct'
productdata = {
    "page":1,
    "prepage":20,
    "tag":1,
    "t":1555573786809,
    "keyword":""
}
productdata["keyword"] = sku
productreq = s.get(rqurl + producturl, params=productdata)
#print(len(json.loads(productreq.text)["data"]["list"]))
productid = json.loads(productreq.text)["data"]["list"][0]["product_id"]
print(productid)




rqdata = {
		"id":23,
		"Document":"组合分析-单图：获取列表数据",
		"Request_Method":"POST",
		"Request_URL":"/report/v2.Combination/queryCombinationStatisticsList",
		"Request_Headers":"",
		"Request_Params":"",
		"Request_Data":{"project_id":"2750299","creative_type":"banner","platform_id":"","campaign_id":"","compare_id":"","ad_set_id":"","creative_id":"","size_id":"","combination_state":"","merge":"false","start_date":"2019-04-01","end_date":"2019-04-14","index":"impression_num,click_num,click_ratio,charge,app_custom_event.fb_mobile_purchase_value,install_unit_price,mobile_app_install","category_id":"","product_id":"223032","select_time":"","latest_serving_date":"","order_field":"","order_type":"","page":"1","page_size":"10"},
        "assertRq":[["code"],["data","total"],["data","summary","impression_num"]],
		"assertExpect":[0,12,"249437"],
		"validate": [
			{"eq": ["code", 0]},
			{"eq": ["data.total", 12]},
			{"eq": ["data.summary.impression_num", "249437"]}]
      	}



rqdata["Request_Data"]["product_id"] = productid




for j,k in projectarry:
    #print(j,k)
    rqdata["Request_Data"]["project_id"] = j
    #print(rqdata["Request_Data"]["project_id"])


    for i in type:
        rqdata["Request_Data"]["creative_type"] = i
        #print(rqdata["Request_Data"]["creative_type"])
        reqcheck = s.post(rqurl+rqdata['Request_URL'], data=rqdata['Request_Data'])
        #print(reqcheck.text)
        reqdict = json.loads(reqcheck.text)
        print(reqdict)
        if reqdict["data"] != []:
            print(j,k,i)
            print(reqdict["data"]["total"])
            print(reqdict["data"]["summary"]["charge"],end="    ")
            print(reqdict["data"]["summary"]["offsite_conversion.fb_pixel_purchase_value"], end="   ")
            print(reqdict["data"]["summary"]["pc_roas"], end="   ")
            print("\n")
        else:
            pass

            #print("=========没有=========")
    #print("\n")
