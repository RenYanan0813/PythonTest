# -*- coding:utf-8 -*-
"""
    author: rony
"""

import os
import re
from tkinter.filedialog import askdirectory,askopenfilename
import time
import numpy as np
import pandas as pd
import xlwt

def count_lines(filepath):
    count = 0
    for index, line in enumerate(open(filepath, 'r')):
        count += 1
    return count

#清理服务监控数据
def getMainData(file_path, catch_data_file):
    try:
        with open(file_path, 'r+') as fp:
        # for index, line in enumerate(open(file_path, 'r')):
            num_lines = count_lines(file_path)
            lenghts = fp.readlines()
            start_time = time.time()
            for i in range(num_lines):
                with open(catch_data_file, 'a') as cf:
                    if lenghts[i] == '\n' or lenghts[i] == None or "grep" in lenghts[i] or "sar" in lenghts[i]\
                            or "bash" in lenghts[i] or "<defunct>" in lenghts[i] or "sadc" in lenghts[i] or "ps" in lenghts[i] \
                            or "tail" in lenghts[i] or "%" in lenghts[i] or "sshd" in lenghts[i] or "df" in lenghts[i]:
                    # if '' == line or line == '' or line == None or "grep" in line or "sar" in \
                    #         line \
                    #         or "bash" in line or "<defunct>" in line or "sadc" in line or "ps" in \
                    #         line \
                    #         or "tail" in line or "%" in line or "sshd" in line:
                        pass
                    # elif len(lenghts[i].split()) == 0:
                    #     pass
                    else:
                        if "某些服务使用 cpu 情况" in lenghts[i]:
                            lenghts[i] = str(re.findall('(\d{8}).*(\d{2}:\d{2}:\d{2}).*(\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', lenghts[i]))
                            lenghts[i] = lenghts[i].replace('[(', '').replace(')]', '').replace('\\', '').replace(',', '').replace('\'','')
                            cf.write(lenghts[i])
                        else:
                            lenghts[i] = lenghts[i].replace('...', ' ')
                            cf.write(lenghts[i])
                end_time = time.time()
                if i%100 == 0:
                    print("正在清理数据中，已用时***** %s 秒 ......."%(int(end_time - start_time)))
    except IOError as e:
        e.with_traceback()
    finally:
        # fp.close()
        cf.close()

#txt 转换成 csv
def txt_2_csv(txt_file, csv_file):
    txt = np.loadtxt(txt_file)
    txtDF = pd.DataFrame(txt)
    txtDF.to_csv(csv_file, index=False)

#txt 转换成 csv
def txt_2_exl(txt_file, exl_file):
    data = pd.read_csv(txt_file)
    df = pd.DataFrame(data)
    df.head()
    writer = pd.ExcelWriter(exl_file)
    df.to_excel(writer, 'Sheet1')

# 将 txt 的内容转换成 Excel 格式
def txt_xls(filename,xlsname):
    try:
        f = open(filename)
        xls = xlwt.Workbook()
        #生成excel的方法，声明excel
        sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True)
        x = 0   #在excel开始写的位置（y）

        while True:     #循环读取文本里面的内容
            line = f.readline()     #一行一行的读
            if not line:    #如果没有内容，则退出循环
                break
            for i in range(len(line.split(' '))):   #\t即tab健分隔
                item = line.split(' ')[i]
                sheet.write(x,i,item)      #x单元格经度，i单元格纬度
            x += 1  #另起一行
        f.close()
        xls.save(xlsname)        #保存为xls文件
    except:
        raise


if __name__ == "__main__":
    #获取要分析文件的路径
    path_file = askopenfilename()
    FILE_NAME = path_file.split('/')[-1].replace('.txt', '')
    data_txt_file = "data\%s.txt"%(FILE_NAME, )
    data_csv_file = "data\%s.csv"%(FILE_NAME, )
    data_exl_file = "data\%s.xlsx" % (FILE_NAME,)
    getMainData(path_file, data_txt_file)
    txt_xls(data_txt_file, data_exl_file)