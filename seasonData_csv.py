from selenium import webdriver  # 导入库
import time
import csv
from itertools import islice

browser = webdriver.Chrome(executable_path='chromedriver.exe')


# 封装写入
def encapsulatedInto(title, data, fileName):
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
            data_dic.append(teamDict)
            teamDict = {}

    # fileName = 'regularSeason_avg_' + str[url.rindex('/') + 1:] + '.csv'
    with open(fileName, 'w', newline='') as csv_file:
        # 设置csv的标题
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # 写入标题
        writer.writeheader()
        # 写入数据
        for dict in data_dic:
            writer.writerow(dict)


def getData(url):
    browser.get(url)
    time.sleep(3)

    # 常规赛 regular season
    # 平均
    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 'data/regularSeason_avg_' + url[url.rindex('/') + 1:] + '.csv')

    # 总计
    btn = browser.find_element_by_xpath(
        '//*[@id="main-container"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div[2]')
    btn.click()

    time.sleep(5)

    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[1]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 'data/regularSeason_total_' + url[url.rindex('/') + 1:] + '.csv')

    # 季后赛 post season
    # 平均
    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 'data/postSeason_avg_' + url[url.rindex('/') + 1:] + '.csv')

    # 总计
    btn = browser.find_element_by_xpath(
        '//*[@id="main-container"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]')
    btn.click()

    time.sleep(5)

    title = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/th[not(contains(@class, "ng-hide"))]')

    data = browser.find_elements_by_xpath(
        '//div[@class="sib-table-container sib-table-single-team-stats team-stats"]/div[2]//nba-stat-table/div/div[@class="nba-stat-table__overflow"]/table//tr/td[not(contains(@class, "ng-hide"))]')

    encapsulatedInto(title, data, 'data/postSeason_total_' + url[url.rindex('/') + 1:] + '.csv')


with open('data/teamBaseInfo.csv', 'r') as read_file:
    reader = csv.reader(read_file)
    # for row in reader:
    for row in islice(reader, 1, None):
        print('开始爬取=>{}_{}'.format(row[0], row[1]))
        getData(row[2])

browser.close()
