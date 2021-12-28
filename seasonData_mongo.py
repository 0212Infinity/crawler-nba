# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from pymongo import MongoClient

browser = webdriver.Chrome(executable_path='chromedriver.exe')
client = MongoClient(host='192.168.218.132', port=27017, username='admin', password='123456')
collectionByTeamBaseInfo = client['test']['TeamBaseInfo']
collectionBySeasonData = client['test']['SeasonData']


# 1-常规赛平均 2-常规赛总计 3-季后赛平均 4-季后赛总计

# 封装写入
def encapsulatedInto(title, data, type, id):
    # 标题
    keys = []
    titleLen = len(title)
    for i in title:
        keys.append(i.text)

    data_dic = list()
    index = 0
    teamDict = {}
    for i in data:
        teamDict[keys[index % titleLen]] = i.text
        index += 1
        if index % titleLen == 0:
            jsonDict = {}
            jsonDict['jsonStr'] = teamDict
            jsonDict['type'] = type
            jsonDict['teamBaseInfo_id'] = id
            data_dic.append(jsonDict)
            teamDict = {}
    collectionBySeasonData.insert_many(data_dic)


def getData(url, id):
    browser.get(url)
    time.sleep(3)

    # 常规赛 regular season
    # 平均
    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 1, id)

    # 总计
    btn = browser.find_element_by_xpath(
        '//*[@id="main-container"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div[2]')
    btn.click()

    time.sleep(5)

    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 2, id)

    # 季后赛 post season
    # 平均
    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 3, id)

    # 总计
    btn = browser.find_element_by_xpath(
        '//*[@id="main-container"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]')
    btn.click()

    time.sleep(5)

    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 4, id)


teams = collectionByTeamBaseInfo.find()
for team in teams:
    print('开始爬取=>{}_{}'.format(team['city'], team['name']))
    getData(team['dataUrl'], team['_id'])

browser.close()
