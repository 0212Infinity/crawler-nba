from selenium import webdriver  # 导入库
import time
import csv

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
    teamDict['city'] = teamCity[i].text
    teamDict['name'] = teamName[i].text
    teamDict['dataUrl'] = dataBtn[i].get_attribute("href")
    data_dic.append(teamDict)

with open('data/teamBaseInfo.csv', 'w', newline='') as csv_file:
    keys = []
    for key in data_dic[0].keys():
        keys.append(key)
    # 设置csv的标题
    writer = csv.DictWriter(csv_file, fieldnames=keys)
    # 写入标题
    writer.writeheader()
    # 写入数据
    for dict in data_dic:
        writer.writerow(dict)
