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

更新：20181120
1. 增设单独某些服务的cpu使用率
2. 增 多少秒 监控一次
3. 设置监控多长时间

更新：20190112

1. cpu单独监控  sar -u 1 60

"""

import paramiko
import config
from datetime import datetime
from time import sleep
import time
import threading

def listener_cpu(hsn, usn, psw, out, sleep_time, listen_time):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d-%H%M%S')
    cpu_out = "%s_cpu_%s.txt"%(out, date_out)
    stop_time = float(sleep_time)
    listener_time = int(listen_time) * 60
    flag = True
    # sys.stdout = open(out, 'w+')
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("--------- %s 正在输出到 %s 文件中... "%(date, out))
            print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn), file=open(cpu_out, 'a'))
            command1 = "sar -u %s %s" %(sleep_time, listener_time)
            stdin, stdout, stderr = ssh.exec_command(command1)
            print("正在监控 %s 的 cpu 中..."%(hsn))
            for line in stdout:
                print('... ' + line.strip('\n'), file=open(cpu_out, 'a'))
            print("\n\n", file=open(cpu_out, 'a'))

            #间隔几秒打印一次
            sleep(stop_time)

            #设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > state_time:
                flag = False

    except Exception as e:
        print("-------")
    finally:
        ssh.close()
        print("监控 %s 的 cpu 情况完成"%(hsn))


if __name__ == "__main__":

    threads = []
    set_time = input("请输入 间隔多少秒 监控一次(秒)：" )
    state_time = input("请输入 监控多少分钟（分）：")

    for i in range(len(config.svr_info)):
        t = threading.Thread(target=listener_cpu, args=(
        config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"], config.svr_info[i]["out_txt"],
        set_time, state_time))
        threads.append(t)


    for j in range(len(config.svr_info)):
        threads[j].start()

    for k in range(len(config.svr_info)):
        threads[k].join()

