#c:/python36/
#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('180.2.35.186', username='zhiban', password='zhiban')
stdin, stdout, stderr = client.exec_command('ls')

for line in stdout:
    print('...' + line.strip('\n'))

client.close()