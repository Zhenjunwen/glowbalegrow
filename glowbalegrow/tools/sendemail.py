#coding=utf-8
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(filepath, env):
    print (filepath)
    msg_from = 'oujin@kuaizi.ai'                                 #发送方邮箱
    passwd = 'Oujing3.14'
    msg_to = 'oujin@kuaizi.ai'                                   #收件人邮箱
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = env+'-接口自动化测试报告--' + now                           #主题
    #content = "这是我使用python smtplib及email模块发送的邮件"

    f = open(filepath,mode='r',encoding='utf-8')
    content = f.read()
    #print content
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
        print ("发送成功")
    except (s.SMTPException, e):
        print ("发送失败")
        print (e)
    finally:
        s.quit()
