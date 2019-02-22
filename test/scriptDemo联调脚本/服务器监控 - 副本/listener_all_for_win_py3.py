#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

"""
    1. 服务监控命令：top -bi -n 1 -d 0.02
    2. CPU 监控命令： sar -u 1 3
    3. IO 监控命令： sar -b 1 3
    4. disk 监控命令： df -h
    5. mem 监控命令：  sar -r 1 3
"""

import config
from time import sleep
import paramiko
from datetime import datetime
import time
import threading

#监控 cpu ,
def listener_cpu(hsn, usn, psw, out_txt, sleep_tm, listener_tm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d')
    cpu_out = "%s_cpu_%s.txt"%(out_txt, date_out)
    stop_time = float(sleep_tm)
    listener_time = int(listener_tm) * 60
    flag = True
    # sys.stdout = open(out, 'w+')
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn), file=open(cpu_out, 'a'))
            command1 = "sar -u %s %s" %(sleep_tm, listener_time)
            stdin, stdout, stderr = ssh.exec_command(command1)
            print("正在监控 %s 的 cpu 中..."%(hsn))
            for line in stdout:
                print('... ' + line.strip('\n'), file=open(cpu_out, 'a'))
            print("\n\n", file=open(cpu_out, 'a'))

            #间隔几秒打印一次
            sleep(stop_time)

            #设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > listener_time:
                flag = False

    except Exception as e:
        print("cpu 监控有异常！")
    finally:
        ssh.close()
        print("监控 %s 的 cpu 情况完成"%(hsn))


#监控 mem ,
def listener_mem(hsn, usn, psw, out_txt, sleep_tm, listener_tm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d')
    mem_out = "%s_mem_%s.txt"%(out_txt, date_out)
    stop_time = float(sleep_tm)
    listener_time = int(listener_tm) * 60
    # server_name = svr_name.split(",")
    flag = True
    # sys.stdout = open(out, 'w+')
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn), file=open(mem_out, 'a'))
            # stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
            command = "sar -r %s %s" %(sleep_tm, listener_time)
            stdin1, stdout1, stderr1 = ssh.exec_command(command)
            print("正在监控 %s 的 mem 中..." % (hsn))
            for line in stdout1:
                print('... ' + line.strip('\n'), file=open(mem_out, 'a'))
            print("\n\n", file=open(mem_out, 'a'))
            #间隔几秒打印一次
            sleep(stop_time)

            #设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > listener_time:
                flag = False

    except Exception as e:
        print("mem 监控有异常！")
    finally:
        ssh.close()
        print("监控 %s 的 mem 情况完成" % (hsn))

#监控 IO ,
def listener_io(hsn, usn, psw, out_txt, sleep_tm, listener_tm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d')
    io_out = "%s_io_%s.txt"%(out_txt, date_out)
    stop_time = float(sleep_tm)
    listener_time = int(listener_tm) * 60
    flag = True
    # sys.stdout = open(out, 'w+')
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("*********************%s --- %s 服务器的---- IO 使用情况 **********************"%(date, hsn), file=open(io_out, 'a'))
            command1 = "sar -b %s %s" %(sleep_tm, listener_time)
            stdin, stdout, stderr = ssh.exec_command(command1)
            print("正在监控 %s 的 IO 中..."%(hsn))
            for line in stdout:
                print('... ' + line.strip('\n'), file=open(io_out, 'a'))
            print("\n\n", file=open(io_out, 'a'))

            #间隔几秒打印一次
            sleep(stop_time)

            #设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > listener_time:
                flag = False

    except Exception as e:
        print(" io 监控有异常！")
    finally:
        ssh.close()
        print("监控 %s 的 IO 情况完成"%(hsn))

#监控 disk ,
def listener_disk(hsn, usn, psw, out_txt, sleep_tm, listener_tm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d')
    disk_out = "%s_disk_%s.txt"%(out_txt, date_out)
    stop_time = float(sleep_tm)
    listener_time = int(listener_tm) * 60

    flag = True
    print("正在监控 %s 的 disk 中..." % (hsn))
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')
            print("*********************%s --- %s 服务器的----  disk 使用情况 **********************"%(date, hsn), file=open(disk_out, 'a'))

            stdin2, stdout2, stderr2 = ssh.exec_command("df -h")

            for line in stdout2:
                print('... ' + line.strip('\n'), file=open(disk_out, 'a'))
            print("\n\n", file=open(disk_out, 'a'))

            #间隔几秒打印一次
            sleep(stop_time)

            #设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > listener_time:
                flag = False

    except Exception as e:
        print("disk 监控有异常！")
    finally:
        ssh.close()
        print("监控 %s 的 disk 情况完成" % (hsn))

#监控 服务 ,
def listener_svrs(hsn, usn, psw, out_txt, svr_name, sleep_tm, listener_tm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d')
    svr_out = "%s_%s_%s.txt" % (out_txt, svr_name, date_out)
    stop_time = float(sleep_tm)
    listener_time = int(listener_tm) * 60
    server_name = svr_name.split(",")
    flag = True
    # sys.stdout = open(out, 'w+')
    print("正在监控 %s 的 服务 中..." % (hsn))
    try:
        # 设置起始时间
        start_time = time.time()
        while (flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("*********************%s --- %s 服务器的---- 某些服务使用 cpu 情况 **********************" % (date, hsn),
                  file=open(svr_out, 'a'))
            print("...   USER  PID  %CPU  %MEM   VSZ   RSS   TTY   STAT START TIME COMMAND \n",
                  file=open(svr_out, 'a'))

            for svr in range(len(server_name)):
                comd = "ps -aux | grep %s" % (server_name[svr])
                stdin3, stdout3, stderr3 = ssh.exec_command(comd)
                for line in stdout3:
                    print('... ' + line.strip('\n'), file=open(svr_out, 'a'))
                print(stderr3)
            print("\n\n", file=open(svr_out, 'a'))

            # 间隔几秒打印一次
            sleep(stop_time)

            # 设置统计时间段
            end_time = time.time()
            if int(int(end_time) - int(start_time)) > listener_time:
                flag = False

    except Exception as e:
        print("服务 的 监控有异常！")
    finally:
        ssh.close()
        print("监控 %s 的 服务 情况完成" % (hsn))



if __name__ == "__main__":

    svrs_threads = []
    cpu_threads = []
    mem_threads = []
    disk_threads = []
    io_threads = []
    svrnames = []
    for m in range(len(config.svr_info)):
        svrnames.append( input("请输入 %s 服务器的某些服务的服务名(以逗号分隔)："%(config.svr_info[m]["hostname"],)))
    sleep_time = input("请输入 间隔多少秒 监控一次(秒)：" )
    listener_time = input("请输入 监控多长分钟（分）：")

    for i in range(len(config.svr_info)):
        #为 服务s 添加线程
        svrs_threads.append(threading.Thread(target=listener_svrs, args=(
            config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"],
            config.svr_info[i]["out_txt"],
            svrnames[i], sleep_time, listener_time)))

        # 为 cpu 添加线程
        cpu_threads.append(threading.Thread(target=listener_cpu, args=(
            config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"],
            config.svr_info[i]["out_txt"],
            sleep_time, listener_time)))

        # 为 disk 添加线程
        disk_threads.append(threading.Thread(target=listener_disk, args=(
            config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"],
            config.svr_info[i]["out_txt"],
            sleep_time, listener_time)))

        # 为 IO 添加线程
        io_threads.append(threading.Thread(target=listener_io, args=(
            config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"],
            config.svr_info[i]["out_txt"],
            sleep_time, listener_time)))

        # 为 mem 添加线程
        mem_threads.append(threading.Thread(target=listener_mem, args=(
            config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"],
            config.svr_info[i]["out_txt"],
            sleep_time, listener_time)))

    for j in range(len(config.svr_info)):
        svrs_threads[j].start()
        cpu_threads[j].start()
        mem_threads[j].start()
        disk_threads[j].start()
        io_threads[j].start()

    for k in range(len(config.svr_info)):
        svrs_threads[k].start()
        cpu_threads[k].start()
        mem_threads[k].start()
        disk_threads[k].start()
        io_threads[k].start()