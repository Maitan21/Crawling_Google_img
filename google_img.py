
##  Created by Jho on 2020/04/20.
##  Copyright © jho All rights reserved.

import sys, os
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import urllib
import requests
import random
import time
from selenium.webdriver.common.keys import Keys

def CrawlGoogleImg(searchItem):
    
    ## 초기설정
    folder = "/Users/jho/Documents/Pyhton/downloads"
    url = "https://www.google.com/search"
    webDriver = "/Users/jho/Documents/Pyhton/chromedriver 2"
    size = 300 #갯수

    params ={
    "q":searchItem
    ,"tbm":"isch"
    ,"sa":"1"
    ,"source":"lnms&tbm=isch"
    }

    ### 구글드라이버 실행

    url = url+"?"+urllib.parse.urlencode(params)
    browser = webdriver.Chrome(webDriver)
    browser.get(url)
    html = browser.page_source
    time.sleep(0.5)


    ### 페이지 파싱

    soup_temp = BeautifulSoup(html,'html.parser')
    img4page = len(soup_temp.findAll("img"))


    ### 자동 스크롤
    
    elem = browser.find_element_by_tag_name("body")
    imgCnt =0

    while imgCnt < size*10:
        elem.send_keys(Keys.PAGE_DOWN)
        rnd = random.random()
        time.sleep(rnd)
        imgCnt+=img4page


    ### html 읽어온후 src 파싱

    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    img = soup.findAll("img")

    browser.find_elements_by_tag_name('img')

    fileNum=0
    srcURL=[]

    for line in img:
        if str(line).find('data-src') != -1 and str(line).find('http')<100:  
            print(fileNum, " : ", line['data-src'])  
            srcURL.append(line['data-src'])
            fileNum+=1


    ### 폴더 생성및 이미지 저장

    saveDir = "/Users/jho/Documents/Pyhton/downloads/"+searchItem

    try:
        if not(os.path.isdir(saveDir)):
            os.makedirs(os.path.join(saveDir))
    except OSError as e:
            print("폴더생성 오류")
            raise

    for i,src in zip(range(fileNum),srcURL):
        urllib.request.urlretrieve(src, saveDir+"/"+str(i)+".jpg")
        print(i,"saved")

    print(searchItem,"저장 완료")

    browser.quit()


##키워드 입력 
args = ['치와와','말티즈','포메라니안']
for i,keyword in enumerate(args):
    CrawlGoogleImg(keyword)