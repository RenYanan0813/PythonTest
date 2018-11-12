#c:/python36/
# -*- coding:utf-8 -*-
"""
目的： 实时监控特定服务器的cpu使用率，磁盘空间使用率、IO使用率

日期：20181112

py: python2.7

"""


import paramiko
import config
from datetime import datetime
import Tkinter as tk
from time import sleep

def listener_cpu(hsn, usn, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)

    try:
        while(True):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')
            print("*********************%s cpu 使用情况 **********************"%(date,))
            stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")
            for line in stdout:
                print('... ' + line.strip('\n'))
            print("\n\n")
            print("*********************%s 内存使用情况 **********************"%(date,))
            stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
            for line in stdout1:
                print('... ' + line.strip('\n'))
            print("\n\n")
            print("*********************%s IO 使用情况 **********************"%(date,))
            stdin2, stdout2, stderr2 = ssh.exec_command("iostat")
            for line in stdout2:
                print('... ' + line.strip('\n'))
            sleep(3)
    except Exception as e:
        print("-------")
    finally:
        ssh.close()

def tkinkerDemo():
    window = tk.Tk()
    window.title("服务器监控")
    window.geometry('800x500')

    b = tk.Button(window,
                  text='hit me',  # 显示在按钮上的文字
                  width=15, height=2,
                  command='hit_me')  # 点击按钮式执行的命令
    b.pack()  # 按钮位置

    cpu_lab = tk.Label(window,
                 text='OMG! this is cpu!',  # 标签的文字
                 bg='green',  # 背景颜色
                 font=('Arial', 12),  # 字体和字体大小
                       width=300, height=30  # 标签长宽
                 )
    cpu_lab.pack()  # 固定窗口位置

    mem_lab = tk.Label(window,
                       text='OMG! this is mem!',  # 标签的文字
                       bg='green',  # 背景颜色
                       font=('Arial', 12),  # 字体和字体大小
                       width=300, height=30  # 标签长宽
                       )
    mem_lab.pack()  # 固定窗口位置

    io_lab = tk.Label(window,
                       text='OMG! this is io!',  # 标签的文字
                       bg='green',  # 背景颜色
                       font=('Arial', 12),  # 字体和字体大小
                       width=300, height=30  # 标签长宽
                       )
    io_lab.pack()  # 固定窗口位置

    window.mainloop()



if __name__ == "__main__":
    # listener_cpu(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"])
    listener_cpu('47.105.140.34', 'root', '________')
    # tkinkerDemo()