# -*- coding: utf-8 -*-
import scrapy
import re
import random
import time
from zhihuqs.items import ZhihuqsItem

class ZhihuqSpider(scrapy.Spider):

    name = 'zhihuq'
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/question/22913650']

    #用于停止抓取的标志
    __stop_flag = 0


    def parse(self, response):

        #提取标题
        title = response.selector.xpath("/html/head/title[1]/text()").extract_first()[0:-5].encode("utf-8")
        
        #出现安全验证停止抓取
        if title == "安全验证":
            self.__stop_flag = 5

        if title and (title!="安全验证"):
            #提取标签
            head_list = response.css("#root > div > main > div > meta:nth-child(3)").xpath("@content").extract_first().encode("utf-8")
            #获取点赞数
            praise_num = response.css("#QuestionAnswers-answers > div > div > div:nth-child(2) > div > div:nth-child(1) > div > meta:nth-child(3)").xpath("@content").extract_first().encode("utf-8")
        #    if int(praise_num) > 100 :

            item = ZhihuqsItem()
            item['title'] = title
            item['head_list'] = head_list
            item['praise_num'] = praise_num

            return item



        #    return{
           #        'title':title,
           #        'head_list':head_list,
           #        'praise_num':praise_num
           #    }

    def start_requests(self):

        url_base = r"https://www.zhihu.com/question/"
 
        #读取上次一结束的位置
        with open("count.txt","r") as f:
            start_index = int(f.read());


        for i in range(start_index,23999999):
            url = url_base + str(i)

            if self.__stop_flag > 0 :
                break
            
            #时刻写入正在读取的位置，这段代码有很大问题，会不断的打开关闭文件，不过可以刚好当作一个延时使用
            with open("count.txt","w") as f:
                f.write(str(i))
            yield scrapy.Request(url,callback=self.parse)
