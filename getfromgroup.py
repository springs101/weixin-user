from wxpy import *
import json, sys, requests
from sentReport.city import cityname
import pkuseg
import re
from pyecharts import *

bot = Bot(console_qr=1, cache_path="botoo.pkl")

def setMsgToGroup():
    setreport('北京')
    return
def setreport(cityname):
    print("开始")
    # 搜索名称含有 "游否" 的男性深圳好友
    my_friend = bot.groups().search('机器人测试群')[0]
    # 发送文本给好友
    my_friend.send(getwehther(cityname))
    print("完成")
    return

def getwehther(cityname):
    outputstr=''
    # 输入地点
    print('输出地址：'+cityname)
    weatherPlace = cityname
    if weatherPlace == 'E' or weatherPlace == 'e':
        sys.exit(0)  # 关闭程序
    # 下载天气JSON
    weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % (
        weatherPlace)
    response = requests.get(weatherJsonUrl)
    try:
        response.raise_for_status()
    except BaseException:
        print("网址请求出错")
        # 将json文件格式导入成python的格式
    weatherData = json.loads(response.text)
    # 以好看的形式打印字典与列表表格
    # import pprint
    # pprint.pprint(weatherData)
    w = weatherData['data']
    outputstr+=("\t\r"+w['city'])
    # 日期
    date_a = []
    # 最高温与最低温
    highTemp = []
    lowTemp = []
    # 天气
    weather = []
    # 进行五天的天气遍历
    for i in range(len(w['forecast'])):
        date_a.append(w['forecast'][i]['date'])
        highTemp.append(w['forecast'][i]['high'])
        lowTemp.append(w['forecast'][i]['low'])
        weather.append(w['forecast'][i]['type'])
        # 输出
        outputstr+=("\t\r日期：" + date_a[i])
        outputstr+=("\t\r天气：" + weather[i])
        outputstr+=("\t\r温度：最" + lowTemp[i] + '℃~最' + highTemp[i] + '℃')
        outputstr+=("\t\r")
    outputstr+=("\n\r今日着装：" + w['ganmao'])
    outputstr+=("\t\r当前温度：" + w['wendu'] + "℃")
    print("完结获取")
    print(outputstr)
    return outputstr
def tulin_reply(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "ffc83115b4014e80b5d1c6c22c6db11a"
    payload = {
                     "key": api_key,
                     "info": text,
                 }
    # 接口要求传json格式字符串,返回数据是json格式
    result= requests.post(url, data=json.dumps(payload)).json()
    # result = json.loads(r.text)
    return result["text"]
def getcityname(text):
    seg = pkuseg.pkuseg()   #以默认配置加载模型
    srcArray = seg.cut(text)    #进行分词
    print(srcArray)

    for val in cityname:
        if val in srcArray:
            print('faxian'+val)
            return val
    print('not find')
    return None
def action():
    friends_stats = bot.friends().stats()
    print(friends_stats)
    attr = []
    v1 = []
    friends_loc = []
    for province, count in friends_stats['sex'].items():
        friends_loc.append([province, count])

    friends_loc.sort(key=lambda x: x[1], reverse=True)
    for p, c in friends_loc[:5]:
        attr.append(p)
        v1.append(c)

    pie = Pie('省份数量统计')
    pie.add('', attr, v1, is_label_show=True, center=[50, 60])
    pie.render()

@bot.register([Group],NOTE)
def welcome(msg):
    print("收到提示信息")
    print(msg.text)
    pattern = re.compile('"(.*)"')
    text = msg.text
    invitename=pattern.findall(text)
    print(invitename)
    if '加入' in text:
        return "热烈欢迎"+invitename[0]+"加入本群！"
    else:
        print("不是邀请！")

    return None

@bot.register([Group],TEXT)
def auto_reply(msg):

    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
            if u"姿美堂扯淡" in msg.text:
                print(msg.chat)
                return '警告，请各位注意言行！'
            return
    else:
            # 回复消息内容和类型
            if u'天气' in msg.text:
                newcity=getcityname(msg.text)
                if newcity == None:
                    return "抱歉，您要求城市不在服务序列"
                else:
                    return  setreport(newcity)
            else:
                return tulin_reply(msg.text)

embed()
