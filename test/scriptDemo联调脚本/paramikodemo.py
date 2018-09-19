#c:/python36/
#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import paramiko

t = paramiko.Transport(('180.2.34.203', 22))
t.connect(username='cln', password='cln')

sftp = paramiko.SFTPClient.from_transport(t)
sftp.get('/home/cln/ryn/ryn1.tar','d:\\sshclient1')

sftp.close()