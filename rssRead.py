# -*- coding:utf-8 -*-

import feedparser
import re
import csv
import opml
import MySQLdb

class News:
    title = ''
    authors = ''
    content = ''
    link = ''

    def __init__(self):
        self.title
        self.content
        self.link


def readRssList(path):
    file = open(path)
    dom = opml.parse(path)
    for outline in dom:
        print outline.xmlUrl
        readRss(outline.xmlUrl)


def readRss(url):
    d = feedparser.parse(url)

    for e in d.entries:
        new = News()
        new.title = e['title']
        # if e.has_key('authors') == True:
        #     new.authors = e['authors'][0]['name']
        if e.has_key('content') == True:
            new.content = e['content'][0]['value']
        else:
            new.content = e['summary_detail']['value']
        # dr = re.compile(r'<[^>]+>', re.S)
        # new.content = dr.sub('',new.content)
        new.link = e['link']
        # print new.title
        # print new.content
        newslist.append(new)
    connectDb()
    # print "--------------------------------"


def writeCsv():
    csvfile = file('rss_csv.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['标题', '内容', '链接'])
    for new in newslist:
        try:
            data = (new.title.encode('utf-8'),new.content.encode('utf-8'),new.link.encode('utf-8'))
            writer.writerow(data)
        except Exception,e:
            print e
            print data
    csvfile.close()

def connectDb():
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "", "apt_ioc_pro", charset="utf8")
    # print text
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # print text['file']
    try:
        for new in newslist:
        # 使用execute方法执行SQL语句
            cursor.execute("INSERT INTO rss values(null,'%s','%s','%s')" % (new.title.encode('utf-8'),new.content.encode('utf-8'),new.link.encode('utf-8')))
        db.commit()
    except BaseException,Argument:
        print Argument
        print new.title.encode('utf-8'), new.content.encode('utf-8'), new.link.encode('utf-8')
        db.rollback()

    # 关闭数据库连接
    db.close()

newslist=[]
readRssList('/Users/sujunwei/work/Apt_Ioc_work/RSS_Bot.opml')
# readRss('http://bobao.360.cn/rss?type=news')
