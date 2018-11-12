# -*- coding:utf-8 -*-


"""
目的： 实时监控特定服务器的cpu使用率，磁盘空间使用率、IO使用率

日期：20181112

py: python2.7

"""


import paramiko
import config
from datetime import datetime

def listener_cpu(hsn, usn, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hsn, username=usn, password=psw)
    date = datetime.now().strftime('%Y%m%d %H:%M:%S')
    try:

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
    except Exception as e:
        print("-------")
    finally:
        ssh.close()


if __name__ == "__main__":
    # listener_cpu(config.qtesvr_a["hostname"], config.qtesvr_a["username"], config.qtesvr_a["psw"])
    listener_cpu('47.105.140.34', 'root', 'ryn812373?')