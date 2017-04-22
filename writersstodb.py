#-*- coding:utf-8 -*-

import MySQLdb
import opml
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')
#获得数据库连接
def createDbConnect():
    db = open('db.txt','r')
    ip = db.readline().split(':')[1].strip()
    port = db.readline().split(':')[1].strip()
    username = db.readline().split(':')[1].strip()
    password = db.readline().split(':')[1].strip()
    dbname = db.readline().split(':')[1].strip()

    dbconnet = MySQLdb.connect(ip, username, password, dbname, charset="utf8")
    return dbconnet


def SaveRssFromOpml(path='./RSS_Bot.opml'):
    file = open(path)
    dom = opml.parse(path)
        # print outline.xmlUrl
    db = createDbConnect()
    cursor = db.cursor()
    for outline in dom:
        try:
            # 使用execute方法执行SQL语句
            cursor.execute("INSERT INTO rss_list values(null,'%s','%s','%s','%s')" % (outline.title, outline.text, outline.type, outline.xmlUrl))
        except Exception,e:
            print e
            print "sql arg: "+outline.title, outline.text, outline.type, outline.xmlUrl
            db.rollback()
    db.commit()
    # 关闭数据库连接
    db.close()
def connectDb(text):
    # 打开数据库连接
    db = createDbConnect()
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
    cmd = 'iocp ' + url + ' -p ./patterns.ini -i txt -o json -l request,BeautifulSoup'
    try:
        tmps = os.popen(cmd).readlines()
        for tmp in tmps:
            text = json.loads(tmp)
            print text
            # connectDb(text)
    except Exception,e:
        print e
        print cmd

def readFile(path=r'./originhtml/'):
    dirlist = os.listdir(path)
    for dir in dirlist:
        dirname = path+dir
        if os.path.isdir(dirname):
            flist = os.listdir(dirname)
            for f in flist:
                filename = dirname+'/'+f
                print filename
                getIocFromUrl(filename)


readFile()
# SaveRssFromOpml()