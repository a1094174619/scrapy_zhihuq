# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as settings


class ZhihuqsPipeline(object):

    def __init__(self):

        dbargs = dict(
            host = '149.28.70.56' ,
            db = 'zhihuQ',
            user = 'root', #replace with you user name
            passwd = 'a745539566.', # replace with you password
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )    
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)


    '''
    The default pipeline invoke function
    '''
    def process_item(self, item,spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item

    def insert_into_table(self,conn,item):
        conn.execute('insert into zhihu_question(title,head_list,praise_num) values(%s,%s,%s)', (item['title'],item['head_list'],item['praise_num']))