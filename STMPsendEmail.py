#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header




def sendEmail(message,From,To,subject,receivers,sender):
    '''
    :param message: text
    :param From: email
    :param To: email
    :param subject: subject = 'Python SMTP 邮件测试'
    :param receivers:  receivers = ['838522868@qq.com']
    :param sender: sender = '601114286@qq.com'
    :return:
    '''
    email = open('email.txt', 'r')
    mail_host = email.readline().split(':')[1].strip()
    mail_user = email.readline().split(':')[1].strip()
    mail_pass = email.readline().split(':')[1].strip()
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header(From, 'utf-8')
    message['To'] = Header(To, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print e
        print "Error: 无法发送邮件"

sendEmail('哈哈','601114286','838522868@qq.com','标题','838522868@qq.com','601114286@qq.com')