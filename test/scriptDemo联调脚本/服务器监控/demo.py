# !_*_coding:utf-8_*_

import re
import os
import wx
import thread
import pychartdir
import csv


class GetCpuStats():

    def __init__(self, name):
        self.pro_name = name

    def startWatch(self):
        _shell = 'adb shell top -s cpu -n 1| findstr %s' % self.pro_name
        result = os.popen(_shell).read()
        return self.getInfo(result)

    def getInfo(self, _result):
        return [re.findall('(\d+)%', _result), re.findall('K\s(\d+)K', _result)]


class MyFrame(wx.Frame):
    flag = False
    _label = []
    _data = []
    _label02 = []
    _data02 = []
    num = 0
    num02 = 0

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title=u'cpu检测小工具', pos=(700, 100), size=(500, 500))
        mPanel = wx.Panel(parent=self)
        mSizer = wx.BoxSizer(orient=wx.VERTICAL)
        btn_start = wx.Button(parent=mPanel, label=u'开始', style=wx.EXPAND)
        mSizer.Add(btn_start)
        btn_stop = wx.Button(parent=mPanel, label=u'停止', style=wx.EXPAND)
        mSizer.Add(btn_stop)
        self.edit = wx.TextCtrl(parent=mPanel, style=wx.EXPAND, value=u'这里输入测试的包名')
        mSizer.Add(self.edit, flag=wx.EXPAND)
        self.edit.Bind(event=wx.EVT_CHOICE, handler=self.requestFocus)
        self.bitmap_cpu = wx.StaticBitmap(parent=mPanel)
        mSizer.Add(self.bitmap_cpu, flag=wx.EXPAND)
        # self.bitmap_mem = wx.StaticBitmap(parent=mPanel)
        # mSizer.Add(self.bitmap_mem, flag=wx.EXPAND)
        mPanel.SetSizer(mSizer)
        mPanel.Fit()
        btn_start.Bind(event=wx.EVT_BUTTON, handler=self.startWatch)
        btn_stop.Bind(event=wx.EVT_BUTTON, handler=self.stopWatch)

    def requestFocus(self, event):
        self.edit.SetValue("")

    def startWatch(self, event):
        self.flag = True
        thread.start_new_thread(self.getInfo, ())

    def stopWatch(self, event):
        self.flag = False

    def getInfo(self):
        while (self.flag):
            _result = GetCpuStats(self.edit.GetValue()).startWatch()
            self.drawPic(_result)
            # self.drawPic_mem(_result)

    def writeCsv(self, _list):
        writer = csv.writer(file('tmp.csv', 'a+'))
        writer.writerow([_list])

    def drawPic(self, _list):
        self.num += 1
        self._label.append(str(self.num))
        self._data.append(_list[0][0])
        self.writeCsv(_list[0][0])
        c = pychartdir.XYChart(500, 400)
        c.setPlotArea(30, 20, 400, 300)
        c.addLineLayer(self._data)
        c.xAxis().setLabels(self._label)
        c.makeChart("tmp.png")
        mImage = wx.Image("tmp.png")
        mImage = mImage.Scale(500, 300)
        self.bitmap_cpu.SetBitmap(wx.BitmapFromImage(mImage))

    def drawPic_mem(self, _list):
        self.num02 += 1
        self._label02.append(str(self.num02))
        self._data02.append(_list[1][0])
        c = pychartdir.XYChart(500, 400)
        c.setPlotArea(60, 40, 400, 300)
        c.addLineLayer(self._data02)
        c.xAxis().setLabels(self._label02)
        c.makeChart("tmp02.png")
        mImage = wx.Image("tmp02.png")
        mImage = mImage.Scale(500, 300)
        self.bitmap_mem.SetBitmap(wx.BitmapFromImage(mImage))


if __name__ == '__main__':
    app = wx.App()
    MyFrame().Show()
    app.MainLoop()