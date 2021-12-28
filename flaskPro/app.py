import random
from flask import Flask, render_template, make_response
from pymongo import MongoClient
from bson.json_util import dumps, loads
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Radar

app = Flask(__name__, template_folder="templates", static_folder="static")
client = MongoClient(host='192.168.218.132', port=27017, username='admin', password='123456')
collectionByTeamBaseInfo = client['test']['TeamBaseInfo']
collectionBySeasonData = client['test']['SeasonData']
app.config['DEBUG'] = True


# 1-常规赛平均 2-常规赛总计 3-季后赛平均 4-季后赛总计
def get_table(teamBaseInfo_id=0, season_id=1):
    try:
        records = collectionBySeasonData.find({'teamBaseInfo_id': teamBaseInfo_id, 'type': season_id})
        record = loads(dumps(records))
        titles = []
        try:
            for key in record[0]['jsonStr']:
                titles.append(key)
        except Exception:
            print("数据有误")

        rows = []
        if len(titles) > 0:
            for i in record:
                row = []
                jsonStr = i['jsonStr']
                for key in jsonStr:
                    row.append(jsonStr[key])
                rows.append(row)
        return render_template('table_bootstrap.html', titles=titles, rows=rows, departID=teamBaseInfo_id,
                               seasonID=season_id)
    except Exception:
        print('get_table error')


# 随机生成16进制颜色    十六进制颜色#开头后面接6个十六进制数
def random_color():
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num


# 1-常规赛平均 2-常规赛总计 3-季后赛平均 4-季后赛总计
def radarObj(teamId, teamName, season_id=2) -> Radar:
    # value=[[对应schema_name,index],[...]]
    c_schema = [
        # {"name": "AQI", "max": 300.1, "min": 5.5}
    ]
    titles = []
    # 封装最大值
    records = collectionBySeasonData.find_one({'type': season_id})
    record = loads(dumps(records))
    try:
        for title in record['jsonStr']:
            try:
                maxValue = collectionBySeasonData.find({'type': season_id}).collation(
                    {'locale': 'zh', 'numericOrdering': True}).sort([('jsonStr.' + str(title), -1)]).skip(0).limit(1)
                maxStr = loads(dumps(maxValue[0]))['jsonStr'][title]
                if len(maxStr) == 0:
                    maxStr = '0'
                max = float(maxStr)
                titles.append(title)
            except Exception:
                continue
            schemaDic = {}
            schemaDic['name'] = title
            schemaDic['min'] = 0
            schemaDic['max'] = max
            c_schema.append(schemaDic)
    except Exception:
        print("数据有误")

    # 数据封装
    allRecords = collectionBySeasonData.find({'type': season_id, 'teamBaseInfo_id': teamId}).sort([('jsonStr.赛季', 1)])
    allRecord = loads(dumps(allRecords))
    allList = {}
    index = 1
    for json in allRecord:
        values = json['jsonStr']
        saiji = values['赛季'][:4]
        for key in titles:
            listVal = 0
            try:
                listVal = float(values[key])
            except Exception:
                listVal = float(0)
            if allList.__contains__(saiji):
                allList.get(saiji).append(listVal)
            else:
                allList[saiji] = [listVal]
        allList.get(saiji).append(index)
        index += 1

    # minValue = collectionBySeasonData.find({'type': season_id}).collation({'locale': 'zh', 'numericOrdering': True}).sort([('jsonStr.进攻', 1)]).skip(0).limit(1)
    rad = Radar().add_schema(schema=c_schema, shape="circle").set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)).set_global_opts(title_opts=opts.TitleOpts(title=teamName))
    for title in allList:
        testval = allList.get(title)
        rad.add(title, [testval], color=random_color())
        print(testval)
    c = (rad)
    return c


def page_simple_layout_radar(season_id):
    try:
        page = Page(layout=Page.SimplePageLayout)
        teams = collectionByTeamBaseInfo.find()
        codeStr = 'page.add('
        for team in teams:
            # 拼接 radarObj函数执行
            codeStr += 'radarObj(' + str(team['_id']) + ', \'' + str(team['name']) + '\',season_id),'
        codeStr += ')'
        exec(codeStr)
        page.render("templates/radar.html")
    except Exception:
        print('get_radar error')


def createBar(titleName, values):
    teams = collectionByTeamBaseInfo.find().sort([('_id', 1)])
    teamList = []
    for team in teams:
        teamName = team['name']
        teamList.append(teamName)
    c = (
        Bar()
            .add_xaxis(teamList)
            .add_yaxis('', values)
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, interval=0)),
                             title_opts=opts.TitleOpts(title=titleName))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="最小值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )  # .render("bar_different_series_gap.html")
    )
    return c


def page_simple_layout_bar(season):
    try:
        allRecords = collectionBySeasonData.find({'type': 2, 'jsonStr.赛季': season}).sort([('teamBaseInfo_id', 1)])
        allRecord = loads(dumps(allRecords))
        allList = {}
        for json in allRecord:
            values = json['jsonStr']
            for key in values:
                if key == '赛季':
                    continue
                listVal = 0
                try:
                    listVal = float(values[key])
                except Exception:
                    listVal = float(0)
                if allList.__contains__(key):
                    allList.get(key).append(listVal)
                else:
                    allList[key] = [listVal]

        page = Page(layout=Page.SimplePageLayout)
        for key in allList:
            page.add(createBar(key, allList[key]))
        page.render("templates/bar.html")
    except Exception as e:
        print('bar error')
        print(e)


@app.route("/")
def index():
    return render_template("index.html")


# 获取球队列表
@app.route("/getTeamBaseInfo")
def getTeamBaseInfo():
    record = collectionByTeamBaseInfo.find()
    response = make_response(dumps(record))
    response.content_type = 'application/json'
    return response


# 表格
@app.route("/table/<int:teamBaseInfo_id>/<int:season_id>")
def table(teamBaseInfo_id, season_id):
    return get_table(teamBaseInfo_id, season_id)


# 雷达图
@app.route("/radar/<int:season_id>")
def radar(season_id):
    page_simple_layout_radar(season_id)
    return render_template("radar.html")


# 柱状图
@app.route("/bar/<season>")
def bar(season):
    page_simple_layout_bar(season)
    return render_template("bar.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
