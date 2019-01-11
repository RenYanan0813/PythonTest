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


"""

import paramiko
import config
from datetime import datetime
from time import sleep
import time
import threading

def listener_cpu(hsn, usn, psw, out, svr_name, st_time, ste_time):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date_out = datetime.now().strftime('%Y%m%d-%H%M%S')
    cpu_out = "%s_cpu_%s.txt"%(out, date_out)
    svr_out = "%s_%s_%s.txt"%(out, svr_name, date_out)
    mem_out = "%s_mem_%s.txt"%(out, date_out)
    disk_out = "%s_disk_%s.txt"%(out, date_out)
    stop_time = float(st_time)
    state_time = int(ste_time) * 60
    server_name = svr_name.split(",")
    flag = True
    # sys.stdout = open(out, 'w+')
    try:
        #设置起始时间
        start_time = time.time()
        while(flag):
            date = datetime.now().strftime('%Y%m%d %H:%M:%S')

            print("--------- %s 正在输出到 %s 文件中... "%(date, out))
            print("*********************%s --- %s 服务器的---- cpu 使用情况 **********************"%(date, hsn), file=open(cpu_out, 'a'))
            stdin, stdout, stderr = ssh.exec_command("top -bi -n 1 -d 0.02")

            for line in stdout:
                print('... ' + line.strip('\n'), file=open(cpu_out, 'a'))
            print("\n\n", file=open(cpu_out, 'a'))

            print("*********************%s --- %s 服务器的---- 某些服务使用 cpu 情况 **********************" % (date, hsn), file=open(svr_out, 'a'))
            print("...   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND \n", file=open(svr_out, 'a'))
            for svr in range(len(server_name)):
                comd = "top -bi -n 1 -d 0.02 | grep %s"%(server_name[svr])
                stdin3, stdout3, stderr3 = ssh.exec_command(comd)
                for line in stdout3:
                    print('... ' + line.strip('\n'), file=open(svr_out, 'a'))
                print(stderr3)
            print("\n\n", file=open(svr_out, 'a'))

            print("*********************%s --- %s 服务器的----  mem 使用情况 **********************"%(date, hsn), file=open(mem_out, 'a'))
            stdin1, stdout1, stderr1 = ssh.exec_command("free -h")
            print("..........                    total        used        free      shared  buff/cache   available \n", file=open(mem_out, 'a'))
            i = 0
            for line in stdout1:
                i += 1
                if i != 1:
                    print('.......... ' + line.strip('\n'), file=open(mem_out, 'a'))
            print("\n\n", file=open(mem_out, 'a'))

            print("*********************%s --- %s 服务器的----  磁盘 使用情况 **********************"%(date, hsn), file=open(disk_out, 'a'))
            stdin2, stdout2, stderr2 = ssh.exec_command("df -h")
            for line in stdout2:
                print('... ' + line.strip('\n'), file=open(disk_out, 'a'))
            print("\n\n", file=open(disk_out, 'a'))
            print("--------- 输出到 txt 文件中, 完成 100%  ------------" )

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


if __name__ == "__main__":

    threads = []
    svrname = []
    for m in range(len(config.svr_info)):
        svrname.append( input("请输入 %s 服务器的某些服务的服务名(以逗号分隔)："%(config.svr_info[m]["hostname"],)))
    #svrname1 = input("请输入 %s 服务器的某些服务的服务名(以逗号分隔)："%(config.qtesvr_b["hostname"],))
    set_time = input("请输入 间隔多少秒 监控一次(秒)：" )
    state_time = input("请输入 监控多长分钟（分）：")

    for i in range(len(config.svr_info)):
        t = threading.Thread(target=listener_cpu, args=(
        config.svr_info[i]["hostname"], config.svr_info[i]["username"], config.svr_info[i]["psw"], config.svr_info[i]["out_txt"],
        svrname[i], set_time, state_time))
        threads.append(t)


    for j in range(len(config.svr_info)):
        threads[j].start()

    for k in range(len(config.svr_info)):
        threads[k].join()
    #分两个进程，同步运行
    # t = threading.Thread(target=listener_cpu, args=(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"], config.qtesvr_a["out_txt"], svrname, set_time, state_time))
    # t1 = threading.Thread(target=listener_cpu, args=(config.qtesvr_b["hostname"], config.qtesvr_b["username"], config.qtesvr_b["psw"], config.qtesvr_b["out_txt"], svrname1, set_time, state_time))
    #
    # t.start()
    # t1.start()
    #
    # t.join()
    # t1.join()
