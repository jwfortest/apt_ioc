#-*- coding:utf-8 -*-

import feedparser
import os
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
        readRss(row[0],row[1])

def readRss(rsstitle,url):
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
    createhtml(rsstitle,newslist)
    # connectDb()
    # print "--------------------------------"


def createhtml(rsstitle,list):
    dirname = r'./rss/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    dirname = dirname + rsstitle
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for item in list:
        filename = item.title.encode('utf-8') + ".html"
        filename = filename.replace('/', '')
        print filename
        try:
            f = open(dirname + "/" + filename, "w")
            f.write(item.link.encode('utf-8'))
            f.write('\n')
            f.write(item.content.encode('utf-8'))
        except Exception, e:
            print e
        f.close()
readUrlFromDb()