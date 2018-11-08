# -*- coding: utf-8 -*-
"""
用于识别知乎BanIP验证码,并且自动填写
"""

import base64
from selenium import webdriver
import time
from PIL import Image
import sys
import os
import pytesseract

class ZhiHuCaptchaRecognition:

    url = 'https://www.zhihu.com'

    def initTable(self,threshold=140):           # 二值化函数
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        return table


    def VertiImage(self,image="verti.png"):
        im = Image.open(image)     #1.打开图片
        im = im.convert('L')             #2.将彩色图像转化为灰度图
        binaryImage = im.point(self.initTable(), '1') #3.降噪，图片二值化
        # binaryImage.show()
        text = pytesseract.image_to_string(binaryImage, config='-psm 7')
        print("验证码识别结果为:",text)  
        return text

    #自动过知乎BANIP验证码
    def PassVerti(self):
        #option = webdriver.ChromeOptions()
        #option.add_argument('headless')
        #下载知乎验证码,返回验证码图片
        #driver = webdriver.Chrome(chrome_options = option)
        driver = webdriver.Chrome()
        time.sleep(2)
        #driver.maximize_window()  # 将浏览器最大化
        verti_title = u"\u5b89\u5168\u9a8c\u8bc1 - \u77e5\u4e4e"

        driver.get(self.url)
        time.sleep(3)
        count = 0
        while driver.title == verti_title:
            print("开始识别验证码")
            #获取验证码元素
            verti_elem = driver.find_element_by_class_name("Unhuman-captcha")
            secert_base64 = verti_elem.get_attribute("src")
            #去掉"data:image/png;base64,"
            base64_pic = secert_base64.encode("utf-8").replace("data:image/png;base64,","")
            #去除Unicode中的%0A的坑爹换行符
            base64_pic = base64_pic.replace(r"%0A","")
            image = base64.b64decode(base64_pic)

            with open("verti.png","wb") as f:
                f.write(image)

            result_text = self.VertiImage()
            if len(result_text) < 2:
                result_text = result_text + "xxx"
            inputbox_elem = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='进入知乎'])[1]/following::input[1]")
            button_elem = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='进入知乎'])[1]/following::button[1]")
            inputbox_elem.clear()
            inputbox_elem.send_keys(result_text)
            time.sleep(1)
            button_elem.click()
            time.sleep(3)
            count = count + 1

            if count > 15:
                #点击按钮被锁，重新打开界面
                driver.get(self.url)
                time.sleep(3)
                count = 0
        #将验证码填写回去
        driver.quit()
