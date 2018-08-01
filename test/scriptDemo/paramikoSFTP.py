# -*- coding:utf-8 -*-

import paramiko
# private_key_path = '/Users/aolens/.ssh/id_rsa'
# key = paramiko.RSAKey.from_private_key_file(paramiko.AutoAddPolicy)
t = paramiko.Transport(('180.2.34.203',22))
t.connect(username='cln',password='cln')
sftp = paramiko.SFTPClient.from_transport(t)
flag = True
while flag:
        con = raw_input('输入要执行的命令: ')
        if con == 'quit':
                flag = False
                t.close()
        # elif con == 'put':
        #         com_add = raw_input('输入文件来源地址:')
        #         target_add = raw_input('输入文件存放地址:')
        #         sftp.put(com_add,target_add)
        # print '上传完成[=========================] 100%  ', "文件上传至:%s"% (target_add)
        elif con == 'get':
                # com_add = raw_input('输入文件来源地址:')
                com_add = '/home/cln/ryn/pexpectdemo.py'
                # target_add = raw_input('输入文件存放地址:')
                target_add = 'd:\\sshclient'
                sftp.get(com_add, target_add)
                print '下载完成[=========================] 100%  ', "文件存放在:%s"% (target_add)
        else:
                print '输入正确的上传下载指令'
                print '上传: put '
                print '下载: get '
                print '========================='