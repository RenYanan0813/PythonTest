# -*- coding:utf-8 -*-

"""
目的：更改服务器时间 20181030
py: python3
"""

import xlrd
import paramiko
import datetime

def readExcel(exl):
    #打开excel
    data = xlrd.open_workbook(exl)
    table = data.sheet_by_index(0)
    #多少行，可知多少台服务器需要修改
    num = table.nrows
    print("---------总共有---  %s  ---台服务器需要更改时间！"%(num-1,))
    get_svr_info(num, table)
    print("总共有%s台服务器需要更改时间！")
    # get_beijin_date()

#获取每个服务器的详细信息
def get_svr_info(num, svr_nfo):
    for i in range(1, 4):
        hostname = str(svr_nfo.row_values(i)[0])
        username = str(svr_nfo.row_values(i)[1])
        password = str(svr_nfo.row_values(i)[2])
        # run_script = str(svr_nfo.row_values(i)[3])
        change_svr_date(hostname, username, password)

#更改服务器时间
def change_svr_date(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    date = get_beijin_date()
    cmd = 'sudo date -s "%s"'%(date,)

    try:
        print("---------更改服务器时间------ %s ------开始-----------"%(hostname,))
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        print("*********更改服务器时间****** %s ******完成***********"%(hostname,))
    except Exception as e:
        print("################更改 %s 时间出了问题！#########################"%(hostname,))
    finally:
        ssh.close()


#获取北京时间
def get_beijin_date():
    date = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    return date


if __name__ == "__main__":
    readExcel("change_svr_date.xls")

