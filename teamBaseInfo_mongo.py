# -*- coding: utf-8 -*-
from selenium import webdriver
from pymongo import MongoClient

browser = webdriver.Chrome(executable_path='chromedriver.exe')

# 球队列表
mainUrl = "https://china.nba.com"
url = mainUrl + "/teamindex"
browser.get(url)

teamCity = browser.find_elements_by_xpath('//div[@class="nba-team-info"]/a/span/span[1]')
teamName = browser.find_elements_by_xpath('//div[@class="nba-team-info"]/a/span/span[2]')
dataBtn = browser.find_elements_by_xpath('//div[@class="nba-team-info"]/div[1]/a[1]')

data_dic = list()
for i in range(len(teamCity)):
    teamDict = dict()
    teamDict['_id'] = i
    teamDict['city'] = teamCity[i].text
    teamDict['name'] = teamName[i].text
    href = dataBtn[i].get_attribute("href")
    teamDict['dataUrl'] = href
    teamDict['code'] = href[href.rindex('/') + 1:]
    data_dic.append(teamDict)

client = MongoClient(host='192.168.218.132', port=27017, username='admin', password='123456')
collection = client['test']['TeamBaseInfo']
records = collection.insert_many(data_dic)

browser.close()
