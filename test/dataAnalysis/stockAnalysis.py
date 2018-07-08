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

yf.pdr_override()
start = datetime(2018,7,2)
#阿里巴巴股票的数据获取
alibaba = pdr.get_data_yahoo('BABA', start="2017-07-01", end="2018-07-08")

print(alibaba)