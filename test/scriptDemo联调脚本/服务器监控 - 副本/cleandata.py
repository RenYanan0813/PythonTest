# -*- coding:utf-8 -*-
"""
    author: rony/renyanan

    更新 20190228
    1. 将所有监控均 简单 的 图形化显示
"""



import os
import re
from tkinter.filedialog import askdirectory,askopenfilename
import time
import numpy as np
import pandas as pd
import xlwt
import matplotlib.pyplot as plt
from datetime import  datetime
import csv

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
            temp_time = ''
            for i in range(num_lines):
                with open(catch_data_file, 'a') as cf:
                    if lenghts[i] == '\n' or (lenghts[i].endswith("svr\n") == False and (lenghts[i] == None or "grep" in lenghts[i] or "sar" in lenghts[i] or " Average" in lenghts[i]\
                            or "bash" in lenghts[i] or "<defunct>" in lenghts[i] or "sadc" in lenghts[i] or "ps" in lenghts[i] or "top" in lenghts[i] \
                            or "tail" in lenghts[i] or "sshd" in lenghts[i] or "df" in lenghts[i] or "Linux" in lenghts[i])) or i == 2 or i == 3:
                        pass
                    else:
                        if "某些服务使用 cpu 情况" in lenghts[i]:
                            temp_time = str(re.findall('(\d{8}).*(\d{2}:\d{2}:\d{2}).*(\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', lenghts[i]))
                            temp_time = temp_time.replace('[(', '').replace(')]', '').replace('\\', '').replace(',', '').replace('\'','')

                        else:

                            cf.write(temp_time)

                            lenghts[i] = lenghts[i].replace('...', ' ')
                            cf.write(lenghts[i])
                end_time = time.time()
                if i%100 == 0:
                    print("正在清理数据中，已用时***** %s 秒 ......."%(int(end_time - start_time)))
    except IOError as e:
        e.with_traceback()
    finally:
        cf.close()
        fp.close()

#清理多余空格，并替换成，
def delMainData(del_file_path, catch_data_file):
    try:
        with open(del_file_path, 'r+') as fp:
        # for index, line in enumerate(open(file_path, 'r')):
            num_lines = count_lines(del_file_path)
            lenghts = fp.readlines()
            start_time = time.time()
            for i in range(num_lines):
                with open(catch_data_file, 'a') as cf:
                    # lenghts[i] = lenghts[i].replace('\\', ',').replace(' ', ',').replace('\'',',').replace('  ', ',').replace('   ', ',').replace('     ', ',')
                    lenghts[i] = str(re.split(r'\s+', lenghts[i]))
                    lenghts[i] = lenghts[i].replace('[', '').replace(']', '').replace('\\', ',').replace('\'', '')
                    cf.write(lenghts[i])
                    cf.write("\n")
                end_time = time.time()
                if i%100 == 0:
                    print("正在清理数据中，已用时***** %s 秒 ......."%(int(end_time - start_time)))
    except IOError as e:
        e.with_traceback()
    finally:
        # fp.close()
        cf.close()
        fp.close()

#对服务的cpu的数据绘图
def svr_csv_2_png(csv_file, num, time_num = 1):
    # 读取CSV文件数据
    filename = csv_file
    i = 0
    with open(filename, encoding='utf-8') as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader
        header_row = next(reader)  # 返回文件中的下一行
        dates, CPUs, lows = [], [], []  # 声明存储日期，最值的列表

        # if i == 1 or i % 600 == 0:
        loop_cnt = 0
        cpu_cnt = 0.0

        try:
            xls = xlwt.Workbook()
            # 生成excel的方法，声明excel
            sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
            x = 0  # 在excel开始写的位置（y）
            hour = ""
            minute = ""
            for row in reader:
                if i == 0 : pass
                else :
                    print(row[time_num])
                    current_date = row[time_num].split(':')
                    if hour == current_date[0] and minute == current_date[1] :
                        cpu_cnt += float(row[num])
                        loop_cnt += 1
                    else :
                        if loop_cnt > 0 :
                            CPU = cpu_cnt / loop_cnt
                            sheet.write(x, 0, hour + ":" + minute)
                            sheet.write(x, 1, str(CPU))
                            x += 1
                        hour = current_date[0]
                        minute = current_date[1]
                        cpu_cnt = 0
                        loop_cnt = 0
                i += 1
            if loop_cnt > 0:
                CPU = cpu_cnt / loop_cnt
                sheet.write(x, 0, hour + ":" + minute)
                sheet.write(x, 1, str(CPU))
                    # current_date = datetime.strptime(row[1], '%H-%M-%S')  # 将日期数据转换为datetime对象

                      # 存储日期
                      # 将字符串转换为数字
                      # 存储CPU
                    # low = int(row[3])
                    # lows.append(low)  # 存储温度最小值
                  # x单元格经度，i单元格纬度

            f.close()
            xls.save(csv_file + '.xls')  # 保存为xls文件
        except:
            raise


    # # 根据数据绘制图形
    # fig = plt.figure(dpi=128, figsize=(10, 6))
    # plt.plot(dates, CPUs, c='red', alpha=0.5)  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    # # plt.plot(dates, lows, c='blue', alpha=0.5)
    # # plt.fill_between(dates, CPUs, lows, facecolor='blue', alpha=0.1)  # 给图表区域填充颜色
    # # plt.title("%s %s's CPU "%(str(row[2][:]), str(row[14][:])), fontsize=24, )
    # plt.title("")
    # plt.xlabel('', fontsize=16)
    # plt.ylabel('Single %CPU', fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=16)
    # fig.autofmt_xdate(bottom=0.2, rotation=70)  # 绘制斜的日期标签
    # plt.savefig(png_file)
    # plt.show()

#对总的cpu的数据绘图
def cpu_csv_2_png(csv_file, png_file):
    # 读取CSV文件数据
    filename = csv_file
    with open(filename, encoding='utf-8') as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader
        header_row = next(reader)  # 返回文件中的下一行
        dates, CPUs, lows = [], [], []  # 声明存储日期，最值的列表
        loop_cnt = 60
        cpus_cnt = 0.0
        c = 1
        for row in reader:
            cpus_cnt += float(row[6])
            if c % loop_cnt == 0:
                # current_date = datetime.strptime(row[1], '%H-%M-%S')  # 将日期数据转换为datetime对象
                current_date = row[3] #获取时间
                dates.append(current_date)  # 存储日期
                CPU = cpus_cnt / loop_cnt  #  获取cpu数据， 并将字符串转换为数字
                cpus_cnt = 0.0
                CPUs.append(CPU)  # 存储CPU
                # low = int(row[3])
                # lows.append(low)  # 存储温度最小值
            c += 1

    # 根据数据绘制图形
    # fig = plt.figure(dpi=128, figsize=(10, 6))
    # plt.plot(dates, CPUs, c='red', alpha=0.5)  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    # # plt.plot(dates, lows, c='blue', alpha=0.5)
    # # plt.fill_between(dates, CPUs, lows, facecolor='blue', alpha=0.1)  # 给图表区域填充颜色
    # plt.title("")
    # plt.xlabel('', fontsize=16)
    # plt.ylabel('Total CPU', fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=16)
    # fig.autofmt_xdate(bottom=0.2, rotation=70)  # 绘制斜的日期标签
    # plt.savefig(png_file)
    # plt.show()

#对服务器的 IO 的数据绘图
def io_csv_2_png(csv_file, png_file):
    # 读取CSV文件数据
    filename = csv_file
    with open(filename, encoding='utf-8') as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader
        header_row = next(reader)  # 返回文件中的下一行
        dates, CPUs, lows = [], [], []  # 声明存储日期，最值的列表
        o = 1
        loop_cnt = 60
        io_cnt = 0.0
        for row in reader:
            io_cnt += float(row[5])
            if o % loop_cnt == 0:
                # current_date = datetime.strptime(row[1], '%H-%M-%S')  # 将日期数据转换为datetime对象
                current_date = row[3] #获取时间
                dates.append(current_date)  # 存储日期
                CPU = io_cnt / loop_cnt  #  获取io数据， 并将字符串转换为数字
                io_cnt = 0.0
                CPUs.append(CPU)  # 存储CPU
                # low = int(row[3])
                # lows.append(low)  # 存储温度最小值
            o += 1

    # 根据数据绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(dates, CPUs, c='red', alpha=0.5)  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    # plt.plot(dates, lows, c='blue', alpha=0.5)
    # plt.fill_between(dates, CPUs, lows, facecolor='blue', alpha=0.1)  # 给图表区域填充颜色
    # plt.title("%s IO "%(str(row[2][:]), ), fontsize=24, )
    plt.title("")
    plt.xlabel('', fontsize=16)
    plt.ylabel('IO used', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    fig.autofmt_xdate(bottom=0.2, rotation=70)  # 绘制斜的日期标签
    plt.savefig(png_file)
    plt.show()


def mem_csv_2_png(csv_file, png_file):
    # 读取CSV文件数据
    filename = csv_file
    with open(filename, encoding='utf-8') as f:  # 打开这个文件，并将结果文件对象存储在f中
        reader = csv.reader(f)  # 创建一个阅读器reader
        header_row = next(reader)  # 返回文件中的下一行
        dates, CPUs, lows = [], [], []  # 声明存储日期，最值的列表
        m = 1
        loop_cnt = 60
        mem_cnt = 0.0
        for row in reader:
            mem_cnt += float(row[7])
            if m  % loop_cnt == 0:
                # current_date = datetime.strptime(row[1], '%H-%M-%S')  # 将日期数据转换为datetime对象
                current_date = row[3] #获取时间
                dates.append(current_date)  # 存储日期
                CPU = mem_cnt / loop_cnt  #  获取cpu数据， 并将字符串转换为数字
                mem_cnt = 0.0
                CPUs.append(CPU)  # 存储CPU
                # low = int(row[3])
                # lows.append(low)  # 存储温度最小值
            m += 1

    # 根据数据绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(dates, CPUs, c='red', alpha=0.5)  # 实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
    # plt.plot(dates, lows, c='blue', alpha=0.5)
    # plt.fill_between(dates, CPUs, lows, facecolor='blue', alpha=0.1)  # 给图表区域填充颜色
    # plt.title("%s MEM "%(str(row[2][:]), ), fontsize=24, )
    plt.title("")
    plt.xlabel('', fontsize=16)
    plt.ylabel('Memory used %', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    fig.autofmt_xdate(bottom=0.2, rotation=70)  # 绘制斜的日期标签
    plt.savefig(png_file)
    plt.show()

# excel 转成 csv
def exl_2_csv(exl_file, csv_file):
    data = pd.read_excel(exl_file, 'sheet1', index_col=0)
    data.to_csv(csv_file, encoding='utf-8')

#txt 转换成 csv
def txt_2_csv(txt_file, csv_file):
    txt = np.loadtxt(txt_file)
    txtDF = pd.DataFrame(txt)
    txtDF.to_csv(csv_file, index=False)

#txt 转换成 exl
def txt_2_exl(txt_file, exl_file):
    data = pd.read_csv(txt_file)
    df = pd.DataFrame(data)
    df.head()
    writer = pd.ExcelWriter(exl_file)
    df.to_excel(writer, 'sheet1')

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
            for i in range(len(line.split(','))):   #\t即tab健分隔
                item = line.split(',')[i]
                sheet.write(x,i,item)      #x单元格经度，i单元格纬度
            x += 1  #另起一行
        f.close()
        xls.save(xlsname)        #保存为xls文件
    except:
        raise

def main():
    while(True):
        print("1) 服务占用cpu                       2) mem 使用情况 ")
        print("3) 总 cpu 使用情况                   4) IO 使用情况  ")
        print("99) 退出 ")
        choice_id = input("请选择你要图形化的数据：")

        if choice_id == '99':
            break
        if choice_id == '1':
            # 获取要分析文件的路径
            path_file = askopenfilename()
            FILE_NAME = path_file.split('/')[-1].replace('.txt', '')
            data_txt_file = "data\%s.txt" % (FILE_NAME,)
            data_csv_file = "data\%s.csv" % (FILE_NAME,)
            data_exl_file = "data\%s.xlsx" % (FILE_NAME,)
            del_tab_txt_file = "data\%s_tab.txt" % (FILE_NAME,)
            png_file = "png\%s.png" % (FILE_NAME,)
            getMainData(path_file, data_txt_file)
            delMainData(data_txt_file, del_tab_txt_file)
            txt_xls(del_tab_txt_file, data_exl_file)
            exl_2_csv(data_exl_file, data_csv_file)
            # 将服务绘制成图片
            svr_csv_2_png(data_csv_file, 10)
        elif choice_id == '2':
            # 获取要分析文件的路径
            path_file = askopenfilename()
            FILE_NAME = path_file.split('/')[-1].replace('.txt', '')
            data_txt_file = "data\%s.txt" % (FILE_NAME,)
            data_csv_file = "data\%s.csv" % (FILE_NAME,)
            data_exl_file = "data\%s.xlsx" % (FILE_NAME,)
            del_tab_txt_file = "data\%s_tab.txt" % (FILE_NAME,)
            png_file = "png\%s.png" % (FILE_NAME,)
            getMainData(path_file, data_txt_file)
            delMainData(data_txt_file, del_tab_txt_file)
            txt_xls(del_tab_txt_file, data_exl_file)
            exl_2_csv(data_exl_file, data_csv_file)
            # 将服务绘制成图片
            # mem_csv_2_png(data_csv_file, png_file)
            svr_csv_2_png(data_csv_file, 7)
        elif choice_id == '3':
            # 获取要分析文件的路径
            path_file = askopenfilename()
            FILE_NAME = path_file.split('/')[-1].replace('.txt', '')
            data_txt_file = "data\%s.txt" % (FILE_NAME,)
            data_csv_file = "data\%s.csv" % (FILE_NAME,)
            data_exl_file = "data\%s.xlsx" % (FILE_NAME,)
            del_tab_txt_file = "data\%s_tab.txt" % (FILE_NAME,)
            png_file = "png\%s.png" % (FILE_NAME,)
            getMainData(path_file, data_txt_file)
            delMainData(data_txt_file, del_tab_txt_file)
            txt_xls(del_tab_txt_file, data_exl_file)
            exl_2_csv(data_exl_file, data_csv_file)
            # 将服务绘制成图片
            # cpu_csv_2_png(data_csv_file, png_file)
            svr_csv_2_png(data_csv_file, 6, 3)
        elif choice_id == '4':
            # 获取要分析文件的路径
            path_file = askopenfilename()
            FILE_NAME = path_file.split('/')[-1].replace('.txt', '')
            data_txt_file = "data\%s.txt" % (FILE_NAME,)
            data_csv_file = "data\%s.csv" % (FILE_NAME,)
            data_exl_file = "data\%s.xlsx" % (FILE_NAME,)
            del_tab_txt_file = "data\%s_tab.txt" % (FILE_NAME,)
            png_file = "png\%s.png" % (FILE_NAME,)
            getMainData(path_file, data_txt_file)
            delMainData(data_txt_file, del_tab_txt_file)
            txt_xls(del_tab_txt_file, data_exl_file)
            exl_2_csv(data_exl_file, data_csv_file)
            # 将服务绘制成图片
            # io_csv_2_png(data_csv_file, png_file)
            svr_csv_2_png(data_csv_file, 5)


if __name__ == "__main__":
    main()
    #将服务绘制成图片
    # svr_csv_2_png(data_csv_file, png_file)
    # txt_2_csv(del_tab_txt_file, data_csv_file) #该方式是有bug