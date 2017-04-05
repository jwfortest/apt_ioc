# -*- coding:utf-8 -*-
import os
import os.path
import json
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')
rootdir = "."                                # 指明被遍历的文件夹

def getIoc():
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in  dirnames:                       #输出文件夹信息
        #     print "parent is:" + parent
        #     print  "dirname is" + dirname

        for filename in filenames:                        #输出文件信息
            print "-----------" + filename
            if filename.endswith("pdf"):
                # print "filename is:" + filename
                abpath = os.path.join(parent,filename)
                # print "the full name of the file is:" + abpath #输出文件路径信息
                cmd = 'iocp '+abpath+' -p /Users/sujunwei/我的工作/PycharmProjects/ioc_parser-master-1/iocp/data/patterns.ini -i pdf -o json -l pdfminer'
                # print cmd
                try:
                    tmps = os.popen(cmd).readlines()
                    for tmp in tmps:
                        text = json.loads(tmp)
                        year = parent.replace('./','')
                        if(text['match'].find('­')>0):
                            text['match'] = text['match'].replace('­', '_')
                        if (text['match'].find('-') > 0):
                            text['match'] = text['match'].replace('-', '_')
                        if (text['match'].find('‐') > 0):
                            text['match'] = text['match'].replace('‐', '_')
                        if (text['match'].find('ﬁ') > 0):
                            text['match'] = text['match'].replace('ﬁ', 'fi')
                        if (text['match'].find('�') > 0):
                            text['match'] = text['match'].replace('�', 'fi')
                        connectDb(text,year)
                except ValueError,Argument:
                    print "cmderror"
                    print Argument
                    print "cmd :"+cmd

def reNameFile():

    for parent,dirnames,filenames in os.walk(rootdir):

        for filename in filenames:
            if(filename.endswith("pdf")):
                if(filename.find('(') or filename.find(')')):
                    file = os.path.join(parent, filename)
                    filename = filename.replace('(','')
                    filename = filename.replace(')', '')
                    os.rename(file,os.path.join(parent, filename))

def testjson():
    jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';

    text = json.loads(jsonData)
    print type(text)

def connectDb(text,pdfyear):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "root", "apt_ioc_pro", charset="utf8")
    # print text
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # print text['file']
    try:
        # 使用execute方法执行SQL语句
        cursor.execute("INSERT INTO ioc values(null,'%s','%s','%s','%s','%s')" % (text['file'], pdfyear, text['type'], text['match'], text['page']))
        db.commit()
    except BaseException,Argument:
        print Argument
        print "sql arg: "+text['file'], pdfyear, text['type'], text['match'], text['page']
        db.rollback()

    # 关闭数据库连接
    db.close()

# reNameFile()
getIoc()
# testjson()

# test = 'http://www.cyberesi.com/2011/03/17/msupdate-­‐exe-­‐favorites-­‐dat-­‐analysis'
#
# # result = test.find('-­')
# test = test.replace('e','-')
# if(test):
#     print test