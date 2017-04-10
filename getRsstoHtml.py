#-*- coding:utf-8 -*-

import feedparser
import os

class News:
    title = ''
    authors = ''
    content = ''
    link = ''

    def __init__(self):
        self.title
        self.content
        self.link


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
    createhtml(rsstitle,newslist)
    # connectDb()
    # print "--------------------------------"


def createhtml(rsstitle,list):
    dirname = r'./rss/'+rsstitle
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for item in list:
        filename = item.title.encode('utf-8') + ".html"
        filename = filename.replace('/', '')
        print filename
        f = open(dirname + "/" + filename, "w")
        try:
            f.write(item.link.encode('utf-8'))
            f.write('\n')
            f.write(item.content.encode('utf-8'))
        except Exception, e:
            print('\033[1;31;40m')
            print e
        f.close()
