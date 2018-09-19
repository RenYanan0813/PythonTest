#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import paramiko
def scpdemo(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostinfo[0]['host'], username=hostinfo[0]['username'], password=hostinfo[0]['password'])
    # stdin, stdout, stderr = ssh.exec_command(hostinfo[0]['command1'])
    # stdin, stdout, stderr = ssh.exec_command(hostinfo[0]['command2'])
    stdin, stdout, stderr = ssh.exec_command("cd /home/zhiban/guoqing/20180725/reg/; scp wh0725_r2886.tar.gz cln@180.2.34.203:/home/cln/wh")
    # stdin, stdout, stderr = ssh.exec_command("ls")
    if stdout == "'cln@180.2.34.203's password:":
        stdin.write('cln')

    for line in stdout:
        print("结果！")
        print('...' + line.strip('\n'))
    for line in stderr:
        print("出错！")
        print('...' + line.strip('\n'))
    ssh.close()


def changeServerConf(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostinfo[1]['host'], username=hostinfo[1]['username'], password=hostinfo[1]['password'])
    stdin, stdout, stderr = ssh.exec_command(hostinfo[0]['command1'])
    stdin, stdout, stderr = ssh.exec_command(hostinfo[0]['command2'])
    for line in stdout:
        print('...' + line.strip('\n'))

    ssh.close()


def main():
    hostinfo = (
        {
            'id': 1,
            'scpwhto203': 1,
            'host': '180.2.35.130',
            'username': 'zhiban',
            'password': 'zhiban',
            'command1': 'cd /home/zhiban/guoqing/20180725/reg/; ls',
            'command2': 'scp wh0725_r2886.tar.gz cln@180.2.34.203:/home/cln/wh; yes; cln'
        },
        {
            'id': 2,
            'host': '180.2.34.203',
            'username': 'cln',
            'password': 'cln'
        }
    )
    scpdemo(hostinfo)

import datetime
if __name__ == '__main__':
    main()

    # print(str(datetime.date.today()).split('-'))