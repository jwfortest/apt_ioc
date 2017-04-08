# -*- coding:utf-8 -*-

import feedparser
import re
import csv
import opml
import MySQLdb
import os
import json

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
        readRss(outline.xmlUrl,outline.title)


def readRss(url,rsstitle):
    d = feedparser.parse(url)
    newslist = []
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
        getIocFromUrl(new.link)
    # createhtml(rsstitle,newslist)
    # connectDb()
    # print "--------------------------------"


def createhtml(rsstitle,list):
    dirname = r'./'+rsstitle
    os.mkdir(dirname)
    for item in list:
        filename = item.title.encode('utf-8') + ".html"
        filename = filename.replace('/', '')
        print filename
        f = open(dirname + "/" + filename, "w")
        try:
            f.write(item.content.encode('utf-8'))
            f.write(item.link.encode('utf-8'))
        except Exception, e:
            print('\033[1;31;40m')
            print e
        f.close()


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

def connectDb(text):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "root", "apt_ioc_pro", charset="utf8")
    # print text
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # print text['file']
    try:
        # 使用execute方法执行SQL语句
        cursor.execute("INSERT INTO rss_ioc values(null,'%s','%s','%s','%s')" % (text['file'], text['type'], text['match'].encode('utf-8').replace('\'',''), text['page']))
        db.commit()
    except Exception,e:
        print e
        print "sql arg: "+text['file'], text['type'], text['match'], text['page']
        db.rollback()

    # 关闭数据库连接
    db.close()

def getIocFromUrl(url):
    cmd = 'iocp ' + url + ' -p ./patterns.ini -i html -o json -l request,BeautifulSoup'
    try:
        tmps = os.popen(cmd).readlines()
        for tmp in tmps:
            text = json.loads(tmp)
            connectDb(text)
    except Exception,e:
        print e


# newslist=[]
readRssList('./RSS_Bot.opml')
# readRss('http://bobao.360.cn/rss?type=news')
