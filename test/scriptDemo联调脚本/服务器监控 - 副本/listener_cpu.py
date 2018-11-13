# -*- coding:utf-8 -*-
"""
目的： 实时监控特定服务器的cpu使用率，磁盘空间使用率、IO使用率
日期：20181112
py: python2.7


更新： 20181113
增加GUI界面，未完成！
"""


import paramiko
import config
from datetime import datetime
import Tkinter as tk
from Tkinter import Scrollbar
from time import sleep

def listener_cpu(hsn, usn, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)

    try:
        date = datetime.now().strftime('%Y%m%d %H:%M:%S')
        print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn))
        stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")
        for line in stdout:
            print('... ' + line.strip('\n'))
        print("\n\n")
        print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn))
        stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
        for line in stdout1:
            print('... ' + line.strip('\n'))
        print("\n\n")
        print("*********************%s --- %s 服务器的----  IO 使用情况 **********************"%(date, hsn))
        stdin2, stdout2, stderr2 = ssh.exec_command("iostat")
        for line in stdout2:
            print('... ' + line.strip('\n'))
        # sleep(3)
    except Exception as e:
        print("-------")
    finally:
        ssh.close()

def listener_cpu1(hsn, usn, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)

    try:
        out = []
        out1 = []
        out2 = []
        date = datetime.now().strftime('%Y%m%d %H:%M:%S')
        print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn))
        stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")
        out = list(stdout)
        print("\n\n")
        print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn))
        stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
        out1 = list(stdout1)

        print("\n\n")
        print("*********************%s --- %s 服务器的----  IO 使用情况 **********************"%(date, hsn))
        stdin2, stdout2, stderr2 = ssh.exec_command("iostat")
        out2 = list(stdout2)
        # sleep(3)
        return out, out1, out2
    except Exception as e:
        print("-------")
    finally:
        ssh.close()

def tkinkerDemo():
    window = tk.Tk()
    window.title("服务器监控")
    # window.resizable(800, 500)
    window.geometry('800x500')

    fm = tk.Frame(window)
    btn_qte_a = tk.Button(fm,
                  text='23服务',  # 显示在按钮上的文字

                  command='hit_me')  # 点击按钮式执行的命令
    btn_qte_a.pack(side='left', padx=30, pady=20)  # 按钮位置

    btn_qte_b = tk.Button(fm,
                          text='24服务',  # 显示在按钮上的文字

                          command='hit_me')  # 点击按钮式执行的命令
    btn_qte_b.pack(side='left', padx=30, pady=20)  # 按钮位置
    btn_qte_pause = tk.Button(fm,
                          text='暂停',  # 显示在按钮上的文字

                          command='hit_me')  # 点击按钮式执行的命令
    btn_qte_pause.pack(side='left', padx=30, pady=20)  # 按钮位置

    set_sec_txt = tk.Entry(fm, textvariable ='输入秒数...').pack(side='left')
    fm.pack(padx=0, pady=10)

    a, b, c = listener_cpu1('47.105.140.34', 'root', 'ryn812373?')

    cpu_mess = str(a)
    print(cpu_mess)
    mem_mess = []
    io_mess = []


    fm1 = tk.Frame(window, bg='lightgreen')


    cpu_mes = tk.Label(fm1,
                 text=cpu_mess,
                 bg='green',  # 背景颜色
                 font=('Arial', 12),  # 字体和字体大小
                 # width=300, height=30  # 标签长宽
                 )
    cpu_mes.pack()  # 固定窗口位置

    mem_mes = tk.Label(fm1,
                       text=b,
                       # text='OMG! this is mem!',  # 标签的文字
                       bg='green',  # 背景颜色
                       font=('Arial', 12),  # 字体和字体大小
                       # width=300, height=30  # 标签长宽
                       )
    mem_mes.pack()  # 固定窗口位置

    io_mes = tk.Label(fm1,
                       text=c,
                       # text='OMG! this is io!',  # 标签的文字
                       bg='green',  # 背景颜色
                       font=('Arial', 12),  # 字体和字体大小
                       # width=300, height=30  # 标签长宽
                       )
    io_mes.pack()  # 固定窗口位置
    fm1.pack()
    window.mainloop()



if __name__ == "__main__":
    while(True):
        listener_cpu(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"])
        listener_cpu(config.qtesvr_b["hostname"], config.qtesvr_b["username"], config.qtesvr_b["psw"])
        sleep(30)  #30秒刷新一次
    # listener_cpu('47.105.140.34', 'root', '________')
    # tkinkerDemo()