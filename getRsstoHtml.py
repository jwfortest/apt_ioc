# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import feedparser
import os
import MySQLdb
import urllib
import threading
import json
import socket
socket.setdefaulttimeout(20)
import STMPsendEmail
import time


class News:
    title = ''
    authors = ''
    content = ''
    link = ''
    date = ''
    authors = ''
    tags = ''
    id = ''
    def __init__(self):
        self.title
        self.content
        self.link


def readUrlFromDb():
    db = open('db.txt', 'r')
    ip = db.readline().split(':')[1].strip()
    port = db.readline().split(':')[1].strip()
    username = db.readline().split(':')[1].strip()
    password = db.readline().split(':')[1].strip()
    dbname = db.readline().split(':')[1].strip()

    dbconnet = MySQLdb.connect(ip, username, password, dbname, charset="utf8")
    cursor = dbconnet.cursor()

    sql = "select title,url from rss_list"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        readRss(row[0], row[1])


def readRss(rsstitle, url):
    try:
        d = feedparser.parse(url)
    except socket.timeout as e:
        print e
        print '-----------------------------------------------------------'
        return
    newslist = []
    for e in d.entries:
        new = News()
        new.title = e['title']
        if e.has_key('published'):
            new.date = e['published']
        elif e.has_key('updated'):
            new.date = e['updated']
        if e.has_key('authors'):
            new.authors = e['authors']
        if e.has_key('tags'):
            new.tags = e['tags']
        new.id = e['id']
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
    saveRsshtml(rsstitle, newslist)
    saveOriginHtml(rsstitle, newslist)
    writeJson(rsstitle,newslist)
    # connectDb()
    # print "--------------------------------"


def saveRsshtml(rsstitle, list):
    dirname = r'./rsshtml/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    dirname = dirname + rsstitle
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for item in list:
        filename = item.title + ".html"
        filename = filename.replace('/', '').replace(' ','')
        try:
            if os.path.exists(dirname + "/" + filename):
                # print filename + ' 文件已经存在'
                continue
            f = open(dirname + "/" + filename, "w")
            f.write(item.link)
            f.write('\n')
            f.write(item.content)
            f.close()
        except Exception, e:
            print e
            print dirname + "/" + filename
            os.remove(dirname + "/" + filename)


def saveOriginHtml(rsstitle, list):
    dirname = r'./originhtml/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    dirname = dirname + rsstitle
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for item in list:
        content = urllib.urlopen(item.link).read()
        filename = item.title + ".html"
        filename = filename.replace('/', '').replace(' ','')
        try:
            if os.path.exists(dirname + "/" + filename):
                # print filename + ' 文件已经存在'
                continue
            else:
                print '新增'+filename
            f = open(dirname + "/" + filename, "w")
            f.write(item.link)
            f.write('\n')
            f.write(content)
            f.close()
        except Exception, e:
            print e
            os.remove(dirname + "/" + filename)


def writeJson(rsstitle, list):
    dirname = r'./json/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    dirname = dirname + rsstitle
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for item in list:
        item.content = ''
        itemdict = item.__dict__
        jsoncontent = json.dumps(itemdict)
        filename = item.title + ".json"
        filename = filename.replace('/', '').replace(' ','')
        if os.path.exists(dirname + "/" + filename):
            # print filename + ' 文件已经存在'
            continue
        else:
            print '新增' + filename
        try:
            f = open(dirname + "/" + filename, "w")
            f.write(jsoncontent)
        except Exception, e:
            print e
            f.close()
            os.remove(dirname + "/" + filename)
        f.close()


def startTask():
    try:
        readUrlFromDb()
    except Exception,e:
        print e
        t = time.asctime(time.localtime(time.time()))
        STMPsendEmail.sendEmail('传输下载出现错误'+str(e)+'\n时间为'+t,'838522868@qq.com','apt爬虫错误信息')

# readUrlFromDb()
def printHello():
    print "begin work"
    t = threading.Timer(8*60*60, startTask)
    t.start()


if __name__ == "__main__":
    printHello()
