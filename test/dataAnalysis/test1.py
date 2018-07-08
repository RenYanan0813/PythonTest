#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

from pandas_datareader import data as pdr
import plotly.offline as py_offline
import plotly.graph_objs as go
import fix_yahoo_finance as yf

# py_offline.init_notebook_mode(connected=True)

yf.pdr_override()
mcd = pdr.get_data_yahoo("BABA", start="2018-07-01", end="2018-07-08")
# mcd_candle = go.Candlestick(x=mcd.index,
#                             open=mcd.Open,
#                             high=mcd.High,
#                             low=mcd.Low,
#                             close=mcd.Close,
#                             increasing=dict(line=dict(color= '#00FF00')),
#                             decreasing=dict(line=dict(color= '#FF0000'))
#                            )
# data = [mcd_candle]
#
# layout = go.Layout(
#     plot_bgcolor='rgb(59,68,75)'
# )
#
# fig = go.Figure(data=data, layout=layout)
print(mcd)