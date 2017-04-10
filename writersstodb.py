#-*- coding:utf-8 -*-

import MySQLdb
import opml

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

SaveRssFromOpml()