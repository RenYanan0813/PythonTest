# c:/Python36/
# -*- coding:utf-8 -*-
"""
目的： 实时监控特定服务器的cpu使用率，磁盘空间使用率、IO使用率
日期：20181112
py: python3.6


更新： 20181113
1. 增加GUI界面，未完成！

更新： 20181114
1. 完成增加GUI界面，未做到实时监控！
2. 使用PyInstaller -F 打包成exe文件

更新： 20181115
1. 不需要GUI界面
2. 增加将结果输出到txt文件中

"""


import paramiko
import config
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import Scrollbar
from time import sleep
import os

def listener_cpu(hsn, usn, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    # sys.stdout = open("listener_cpu.txt", 'w+')
    try:
        date = datetime.now().strftime('%Y%m%d %H:%M:%S')
        print("--------- %s 正在输出到 listener_cpu.txt 文件中... "%(date,))
        print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn), file=open("listener_cpu.txt", 'a'))
        # stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")
        stdin, stdout, stderr = ssh.exec_command("sar -P 0 -u 1 2")

        for line in stdout:
            print('... ' + line.strip('\n'), file=open("listener_cpu.txt", 'a'))
        print("\n\n", file=open("listener_cpu.txt", 'a'))

        print("*********************%s --- %s 服务器的---- 各服务使用 cpu 情况 **********************" % (date, hsn), file=open("listener_cpu.txt", 'a'))
        stdin3, stdout3, stderr3 = ssh.exec_command("top -bi -n 1 -d 0.02")
        # stdin3, stdout3, stderr3 = ssh.exec_command("sar -P 0 -u 1 2")
        i = 0
        for line in stdout3:
            i += 1
            if i < 10:
                print('... ' + line.strip('\n'), file=open("listener_cpu.txt", 'a'))
        print("\n\n", file=open("listener_cpu.txt", 'a'))

        print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn), file=open("listener_cpu.txt", 'a'))
        stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
        for line in stdout1:
            print('... ' + line.strip('\n'), file=open("listener_cpu.txt", 'a'))
        print("\n\n", file=open("listener_cpu.txt", 'a'))

        print("*********************%s --- %s 服务器的----  磁盘 使用情况 **********************"%(date, hsn), file=open("listener_cpu.txt", 'a'))
        stdin2, stdout2, stderr2 = ssh.exec_command("df -h")
        for line in stdout2:
            print('... ' + line.strip('\n'), file=open("listener_cpu.txt", 'a'))
        print("\n\n", file=open("listener_cpu.txt", 'a'))
        print("--------- 输出到 listener_cpu.txt 文件中, 完成 100%  ------------")
    except Exception as e:
        print("-------")
    finally:
        ssh.close()

# def listener_cpu1(hsn, usn, psw):
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=hsn, username=usn, password=psw)
#
#     ssh1 = paramiko.SSHClient()
#     ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh1.connect(hostname=hsn, username=usn, password=psw)
#
#     try:
#         # while(True):
#         out = []
#         out1 = []
#         out2 = []
#         date = datetime.now().strftime('%Y%m%d %H:%M:%S')
#         # print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************" % (date, hsn))
#         stdin, stdout, stderr = ssh.exec_command("sar -P 0 -u 1 2")
#         out = list(stdout)
#
#         # print("*********************%s --- %s 服务器的---- 各服务使用 cpu 情况 **********************" % (date, hsn))
#         stdin3, stdout3, stderr3 = ssh.exec_command("top -bi -n 1 -d 0.02")
#         out3 = list(stdout3)
#
#         # print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn))
#         stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
#         out1 = list(stdout1)
#
#         # print("*********************%s --- %s 服务器的----  磁盘 使用情况 **********************"%(date, hsn))
#         stdin2, stdout2, stderr2 = ssh.exec_command("df -h")
#         out2 = list(stdout2)
#
#         return out, out1, out2, out3
#     except Exception as e:
#         print("-------")
#     finally:
#         ssh.close()

#按钮点击出信息
# def get_info(hsn, usn, pwd):
#     # text1.edit_reset()
#     date = datetime.now().strftime('%Y%m%d %H:%M:%S')
#     a, b, c, d = listener_cpu1(hsn, usn, pwd)
#     # cpu 使用情况
#     text1.insert(INSERT, "--------------时间 %s ***** 服务器 %s cpu 使用情况 -------------------------\n"%(date,hsn))
#     for j in range(len(a)):
#         if a[j] != "" or a[j] != None:
#             text1.insert(INSERT, a[j])
#
#     text1.insert(INSERT,'\n\n')
#     #各服务使用 cpu 情况
#     text1.insert(INSERT, "--------------时间 %s ***** 服务器 %s 各服务使用 cpu 情况 -------------------------\n"%(date,hsn))
#     i = 0
#     num = 1
#     for j in range(len(d)):
#         if d[j] != "" or d[j] != None:
#             i += 1
#             if i < 6:
#                 text1.insert(INSERT, d[j])
#
#     text1.insert(INSERT, '\n\n')
#     # mem 使用情况
#     text1.insert(INSERT, "---------------时间 %s ***** 服务器 %s mem 使用情况 -------------------------\n"%(date,hsn))
#     for j in range(len(b)):
#         if b[j] != "" or b[j] != None:
#             text1.insert(INSERT, b[j])
#
#     text1.insert(INSERT, '\n\n')
#     # 磁盘 使用情况
#     text1.insert(INSERT, "---------------时间 %s ***** 服务器 %s 磁盘 使用情况 -------------------------\n"%(date,hsn))
#     for j in range(len(c)):
#         if c[j] != "" or c[j] != None:
#             text1.insert(INSERT, c[j])
#
# def get_listener(num):
#
#     # text2.destory()
#     text1.delete('1.0', '100.0')
#     get_info('180.2.34.23', 'qte', 'qte')
#     # get_info1('180.2.34.24', 'qte', 'qte')
#     at1 = text1.after(5, get_listener, 1)
#
# def get_listener_b(num):
#
#     # text1.destory()
#     text1.delete('1.0', '100.0')
#     # get_info('180.2.34.23', 'qte', 'qte')
#     get_info('180.2.34.24', 'qte', 'qte')
#     at2 = text1.after(5, get_listener_b, 1)
#
# def get_pause():
#     os.system('pause')
#
#
# def tkinkerDemo():
#     window = tk.Tk()
#     window.title("服务器监控")
#     # window.resizable(800, 500)
#     window.geometry('800x550')
#
#     fm = tk.Frame(window)
#     fm.pack()
#     fm1 = tk.Frame(window, bg='lightgreen')
#     text1 = Text(fm1, width=300, height=110, bg='lightpink')
#
#
#     btn_qte_a = tk.Button(fm,
#                   text='23服务',  # 显示在按钮上的文
#                   )  # 点击按钮式执行的命令
#     btn_qte_a.pack(side='left', padx=30, pady=20)  # 按钮位置
#
#     btn_qte_b = tk.Button(fm,
#                           text='24服务',  # 显示在按钮上的文字
#
#                           )  # 点击按钮式执行的命令
#     btn_qte_b.pack(side='left', padx=30, pady=20)  # 按钮位置
#     btn_qte_pause = tk.Button(fm,
#                           text='暂停',  # 显示在按钮上的文字
#
#                           command='hit_me')  # 点击按钮式执行的命令
#     btn_qte_pause.pack(side='left', padx=30, pady=20)  # 按钮位置
#
#     set_sec_txt = tk.Entry(fm, textvariable ='输入秒数...').pack(side='left')
#
#     text1.pack()
#     fm1.pack()
#     btn_qte_a.bind("<Button-1>", get_listener)
#     btn_qte_b.bind("<Button-1>", get_listener_b)
#     # text1.after(5, get_listener_b, 1)
#     btn_qte_pause.bind("<Button-1>", get_pause)
#     fm.pack(padx=0, pady=10)
#
#     window.update()
#     window.mainloop()



if __name__ == "__main__":

    while(True):
        listener_cpu(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"])
        listener_cpu(config.qtesvr_b["hostname"], config.qtesvr_b["username"], config.qtesvr_b["psw"])
        # sleep(1)

    # listener_cpu('47.105.140.34', 'root', '________')
    # tkinkerDemo()