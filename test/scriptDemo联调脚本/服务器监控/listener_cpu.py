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
        # stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")
        stdin, stdout, stderr = ssh.exec_command("sar -P 0 -u 1 2")
        for line in stdout:
            print('... ' + line.strip('\n'))
        print("\n\n")

        print("*********************%s --- %s 服务器的---- 各服务使用 cpu 情况 **********************" % (date, hsn))
        stdin3, stdout3, stderr3 = ssh.exec_command("top -bi -n 1 -d 0.02")
        # stdin3, stdout3, stderr3 = ssh.exec_command("sar -P 0 -u 1 2")
        i = 0
        for line in stdout3:
            i += 1
            if i > 5 or i == 3:
                print('... ' + line.strip('\n'))
        print("\n\n")

        print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn))
        stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
        for line in stdout1:
            print('... ' + line.strip('\n'))
        print("\n\n")
        print("*********************%s --- %s 服务器的----  磁盘 使用情况 **********************"%(date, hsn))
        stdin2, stdout2, stderr2 = ssh.exec_command("df -h")
        for line in stdout2:
            print('... ' + line.strip('\n'))
        print("\n\n")
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
        print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************" % (date, hsn))
        stdin, stdout, stderr = ssh.exec_command("sar -P 0 -u 1 2")
        out = list(stdout)

        print("*********************%s --- %s 服务器的---- 各服务使用 cpu 情况 **********************" % (date, hsn))
        stdin3, stdout3, stderr3 = ssh.exec_command("top -bi -n 1 -d 0.02")
        out3 = list(stdout3)

        print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn))
        stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
        out1 = list(stdout1)

        print("\n\n")
        print("*********************%s --- %s 服务器的----  磁盘 使用情况 **********************"%(date, hsn))
        stdin2, stdout2, stderr2 = ssh.exec_command("df -h")
        out2 = list(stdout2)
        # sleep(3)
        return out, out1, out2, out3
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

    # a, b, c, d= listener_cpu1('47.105.140.34', 'root', 'ryn812373?')
    a, b, c, d = listener_cpu1('180.2.34.24', 'qte', 'qte')
    print(a)
    print(d)
    print(b)
    print(c)

    fm1 = tk.Frame(window, bg='lightgreen')
    text1 = tk.Text(fm1)
    scb = Scrollbar(text1)
    # scb.pack(side='right', fill='y')

    # cpu 使用情况
    for j in range(len(a)):
        if a[j] != "" or a[j] != None:
            text1.insert( a[j], 'a')

    # 各服务使用 cpu 情况
    i = 0
    num = 1
    for j in range(len(d)):
        if d[j] != "" or d[j] != None:
            i += 1
            if i > 5 or i == 3:
                text1.insert('a', d[j], 'd')
    # # cpu 使用情况
    # for j in range(len(a)):
    #     if a[j] != "" or a[j] != None:
    #         tk.Label(fm1,
    #                  text=a[j],
    #                  bg='pink',  # 背景颜色
    #                  font=('Arial', 10),  # 字体和字体大小
    #                  # width=300, height=30  # 标签长宽
    #                  # yscrollcommand=scb.set
    #                  ).pack()
    #
    # # 各服务使用 cpu 情况
    # i = 0
    # num = 1
    # for j in range(len(d)):
    #     if d[j] != "" or d[j] != None:
    #         i += 1
    #         if i > 5 or i == 3:
    #             tk.Label(fm1,
    #                      text=d[j],
    #                      bg='pink',  # 背景颜色
    #                      font=('Arial', 10),  # 字体和字体大小
    #                      # width=300, height=30  # 标签长宽
    #                      # yscrollcommand=scb.set
    #                      ).pack()
    #
    # # mem 使用情况
    # for j in range(len(b)):
    #     if b[j] != "" or b[j] != None:
    #         tk.Label(fm1,
    #                  text=b[j],
    #                  bg='pink',  # 背景颜色
    #                  font=('Arial', 10),  # 字体和字体大小
    #                  # width=300, height=30  # 标签长宽
    #                  # yscrollcommand=scb.set
    #                  ).pack()
    # # 磁盘 使用情况
    # for j in range(len(c)):
    #     if c[j] != "" or c[j] != None:
    #         tk.Label(fm1,
    #                  text=c[j],
    #                  bg='pink',  # 背景颜色
    #                  font=('Arial', 10),  # 字体和字体大小
    #                  # width=300, height=30  # 标签长宽
    #                  # yscrollcommand=scb.set
    #                  ).pack()
    # scb.config(command=lab.yview)
    # bar.config(command=t.yview)
    # lab.config(yscrollcommand=scb.set)
    # scb.pack(side='right', fill='y')
    # fm1.pack(side='left', fill='both', expand=1)
    fm1.pack()
    window.mainloop()



if __name__ == "__main__":
    # while(True):
    #     listener_cpu(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"])
    #     listener_cpu(config.qtesvr_b["hostname"], config.qtesvr_b["username"], config.qtesvr_b["psw"])
    #     sleep(30)  #30秒刷新一次
    # listener_cpu('47.105.140.34', 'root', '________')
    tkinkerDemo()