#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

#基本信息
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

#股票数据的读取
from pandas_datareader import data as pdr
import plotly.graph_objs as go
import fix_yahoo_finance as yf

#可视化
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from datetime import datetime

#修复连接yahoo的错误
yf.pdr_override()
#阿里巴巴股票的数据获取
alibaba = pdr.get_data_yahoo('BABA', start="2017-07-01", end="2018-07-08")
#写入csv文件里
alibaba.to_csv('./BABA.csv')
alibabaData= pd.read_csv('./BABA.csv')
# alibaba.head()

first_twelve = alibabaData[0:20]


# alibabaData['Adj Close'].plot(legend=True)
plt.plot(first_twelve['Date'], first_twelve['Adj Close'])
# 将x轴下面文字旋转90度
plt.xticks(rotation=90)
# 设置x轴的标签
plt.xlabel('Month')
plt.show()