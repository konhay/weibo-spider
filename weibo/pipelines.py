# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeiboPipeline(object):
    def process_item(self, item, spider):
        return item

#weibo project only
#pip install MySQL-Python(maybe error) or download from https://pypi.python.org/pypi/MySQL-python/1.2.5
import MySQLdb
from items import InformationItem, TweetsItem

DEBUG = True

if DEBUG:
    dbuser = 'root'
    #dbpass = '123456'
    dbpass = ''
    dbname = 'tweetinfo'
    #dbhost = '127.0.0.1'
    dbhost = '172.10.238.4'
    #dbhost = '172.16.0.225'
    dbport = '3306'
else:
    dbuser = 'XXXXXXXX'
    dbpass = 'XXXXXXX'
    dbname = 'tweetinfo'
    dbhost = '127.0.0.1'
    dbport = '3306'


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 建立需要存储数据的表

        # 清空表（测试阶段）：
        # self.cursor.execute("truncate table followinfo;")
        # self.conn.commit()
        # self.cursor.execute("truncate table tweets;")
        # self.conn.commit()

    def process_item(self, item, spider):
        # curTime = datetime.datetime.now()
        if isinstance(item, InformationItem):
            print "开始写入关注者信息"
            try:
                self.cursor.execute("""INSERT INTO followinfo (id, Info, Num_Tweets, Num_Follows, Num_Fans, HomePage) 
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                    (
                                        item['_id'].encode('utf-8'),
                                        item['Info'].encode('utf-8'),
                                        item['Num_Tweets'].encode('utf-8'),
                                        item['Num_Follows'].encode('utf-8'),
                                        item['Num_Fans'].encode('utf-8'),
                                        item['HomePage'].encode('utf-8'),
                                    )
                                    )

                self.conn.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        elif isinstance(item, TweetsItem):
            print "开始写入微博信息"
            try:
                self.cursor.execute("""INSERT INTO tweets (id, Contents, Time_Location, Pic_Url, Zan, Transfer, Comment) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                    (
                                        item['_id'].encode('utf-8'),
                                        item['Content'].encode('utf-8'),
                                        item['Time_Location'].encode('utf-8'),
                                        item['Pic_Url'].encode('utf-8'),
                                        item['Like'].encode('utf-8'),
                                        item['Transfer'].encode('utf-8'),
                                        item['Comment'].encode('utf-8')
                                    )
                                    )
                self.conn.commit()

            except MySQLdb.Error, e:
                print "出现错误"
                print "Error %d: %s" % (e.args[0], e.args[1])

        return item