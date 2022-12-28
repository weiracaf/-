import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Timeline
# 读取数据
df = pd.read_csv('weather.csv', encoding='gb18030')
# print(df['日期'])
df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))  # apply函数使用！，把字符串类型转为datetime类型
# print(df['日期'])
df['month'] = df['日期'].dt.month
# print(df['month'])
# 最终数据类型
# month   tianqi（天气）     count（天气对应出现次数）

df_agg = df.groupby(['month', '天气']).size().reset_index()
# print(df_agg)
#  groupby(['列1']，['列2'])返回一个聚合的DataFramGroupyBy的聚合对象
# 设置df_agg列名
df_agg.columns = ['month', 'tianqi', 'count']
# print(df_agg)
data = df_agg[df_agg['month'] == 1][['tianqi', 'count']]\
    .sort_values(by='count', ascending=False).values.tolist()   # 排序第一月数据依据count，且从大到小排
# print(data)
# 画图
timeline = Timeline()
# 播放设置时间间隔 1s
timeline.add_schema(play_interval=1000)     # 计量单位为ms
for month in df_agg['month'].unique():
    data = (
         df_agg[df_agg['month'] == month][['tianqi', 'count']]
        .sort_values(by='count', ascending=False)
        .values.tolist()
    )
    # 绘制柱状图
    bar = Bar()
    # x轴数据：天气名称
    bar.add_xaxis([x[0] for x in data])
    # y轴数据：出现次数
    bar.add_yaxis('', [x[1] for x in data])
    # 让柱状图横着放
    bar.reversal_axis()  # 翻转xy轴
    # 将count放在柱状图右边
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    # 设置下图表的名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title="邯郸2021年每月天气变化"))
    # 将设置好的bar对象放到时间轮播图中，并且标签选择月份   格式：‘月份’+‘月’
    timeline.add(bar, f'{month}月')
timeline.render('weather.html')     # 最后把轮播图渲染成HTML文件
