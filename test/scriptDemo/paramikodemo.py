#c:/python36/
#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
transport = client.connect('180.2.34.203', username='cln', password='cln')
ssh = paramiko.SSHClient.f(client)
# ssh = paramiko.SFTPClient.ge
ssh.get('/home/cln/ryn/pexpectdemo.py','e:/sshclient/')

client.close()