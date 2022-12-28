import requests
from lxml import etree
import csv


# 爬虫代码
def getWeather(url):
    weather_info = []  # [{'日期'：...，‘最高气温’，...}]   最后以字典存储最后的每一天的数据存在列表里
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36 '
    }
    resp = requests.get(url, headers=headers)
    # 数据处理xpath
    resp_html = etree.HTML(resp.text)
    # xpath提取当页的所有数据（每个月）
    resp_list = resp_html.xpath("//ul[@class='thrui']/li")
    for li in resp_list:
        # 每天的数据放入字典
        day_weather_info = {}
        # 日期
        day_weather_info['data_time'] = li.xpath('./div[1]/text()')[0].split(' ')[0]    # xpath
        # 返回的是一个列表我们想把对应的星期日去掉可以用分隔符split
        # 最高气温
        high = li.xpath("./div[2]/text()")[0]   # 涉及xpath语法
        day_weather_info['high'] = high[0]+'℃'
        # 最低气温
        low = li.xpath('./div[3]/text()')
        day_weather_info['low'] = low[0]
        # 天气状况
        day_weather_info['weather'] = li.xpath("./div[4]/text()")[0]
        weather_info.append(day_weather_info)
    # 返回数据
    # print(weather_info)
    return weather_info

# 全年的数据
weathers = []

# 看url的规则，在http://www.tianqi.com查找邯郸2021年的历史天气
# url规律 ...+年份+月份.html --某个城市的对应年月信息
for month in range(1, 13):  # 1-12
    if month < 10:
        weather_time = '2021' + ("0" + str(month))
    else:
        weather_time = '2021' + str(month)
    url = f'https://lishi.tianqi.com/handan/{weather_time}.html'
    # 爬取每个月天气数据
    weather = getWeather(url)
    # 每月数据存入年数据
    weathers.append(weather)
print(weathers)

# 数据写入（一次性写入）  csv
with open('weather.csv', 'w', newline='') as csvfile:   # 生成对应的csv文件
    writer = csv.writer(csvfile)
    # 写入列名：columns_name
    writer.writerow(['日期', '最高气温', '最低气温', '天气'])
    # 一次性写入多行用writerrows（写入数据同样也是列表，一个列表对应一行）
    # writer.writerows([list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])列表推导式
    list_year = []
    for month_weather in weathers:  # 先循环每个月的数据（从年数据里），数据类型为[[{}][{}]]列表里面存放列表，里面的列表存放字典
        for day_weather_dict in month_weather:  # 再循环每天数据（从月数据里）[{}]字典里存储每天的信息
            list_year.append(list(day_weather_dict.values()))
    writer.writerows(list_year)     # 数据写入
