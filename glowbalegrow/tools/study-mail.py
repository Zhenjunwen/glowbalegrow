#coding=utf-8
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#msg_from = '523234182@qq.com'                                 #发送方邮箱
#passwd = 'wqwqtznmocwubjie'                                   #填入发送方邮箱的授权码
msg_from = 'oujin@kuaizi.co'                                 #发送方邮箱
passwd = 'Oujing3.14'
msg_to = 'oujin@kuaizi.co'                                  #收件人邮箱
now = time.strftime("%Y-%m-%d %H:%M:%S")
subject = '接口自动化测试报告--' + now                      #主题
#content = "这是我使用python smtplib及email模块发送的邮件"

f = open("D:\\oujn_master\\glowbalegrow\\report\\result2018-12-25_15-23-59.html", 'r')
#f = open("D:\\oujn_master\\glowbalegrow\\report\\result2018-12-20_17-43-15.html", 'r')#经典原版

content = f.read()
print content
f.close()
msg = MIMEText(content, _subtype='html', _charset='utf-8')

msg['Subject'] = subject
msg['From'] = "环球易购接口监控"
msg['To'] = msg_to


try:
    #s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print "发送成功"
except s.SMTPException, e:
    print "发送失败"
finally:
    s.quit()
