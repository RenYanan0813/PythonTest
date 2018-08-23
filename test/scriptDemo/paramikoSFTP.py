# -*- coding:utf-8 -*-

import paramiko
import re
import datetime

#从服务器上，上传和下载的完整demo，供阅读和更改，未在功能里调用改方法
def getAndPutFile():
    # private_key_path = '/Users/aolens/.ssh/id_rsa'
    # key = paramiko.RSAKey.from_private_key_file(paramiko.AutoAddPolicy)
    t = paramiko.Transport(('180.2.34.203',22))
    t.connect(username='cln',password='cln')
    sftp = paramiko.SFTPClient.from_transport(t)
    flag = True
    while flag:
        con = raw_input('输入要执行的命令: ')
        if con == 'quit':
            # flag = False
            t.close()
            sftp.close()
            break
        elif con == 'put':
            t = paramiko.Transport(('180.2.34.203', 22))
            t.connect(username='cln', password='cln')
            sftp = paramiko.SFTPClient.from_transport(t)
            # com_add = raw_input('输入文件来源地址:')
            # target_add = raw_input('输入文件存放地址:')
            com_add = 'd:\\sshclient\\ryn.tar'
            target_add = '/home/cln/ryn/ryn.tar'
            try:
                    sftp.put(com_add,target_add)
            except:
                    print '本地未找到该文件!'
            print '上传完成[=========================] 100%  ', "文件上传至:%s"% (target_add)
        elif con == 'get':
            # com_add = raw_input('输入文件来源地址:')
            com_add = '/home/cln/ryn.tar'
            # target_add = raw_input('输入文件存放地址:')
            target_add = 'd:\\sshclient\\ryn.tar'
            try:
                    sftp.get(com_add, target_add)
            except:
                    print '服务器没有该文件!'
            print '下载完成[=========================] 100%  ', "文件存放在:%s"% (target_add)
        else:
            print '输入正确的上传下载指令'
            print '上传: put '
            print '下载: get '
            print '========================='


#将本地文件上传到服务器
#com_add为本地文件路径， target_add为服务器文件路径
#svr_add为服务器地址
def putFileToServer(com_add, target_add, svr_add, username, psd):
    # t = paramiko.Transport(('180.2.34.203', 22))
    t = paramiko.Transport((svr_add, 22))
    t.connect(username=username, password=psd)
    sftp = paramiko.SFTPClient.from_transport(t)
    # com_add = raw_input('输入文件来源地址:')
    # target_add = raw_input('输入文件存放地址:')
    # com_add = 'd:\\sshclient\\ryn.tar'
    # target_add = '/home/cln/ryn/ryn.tar'
    try:
        sftp.put(com_add, target_add)
        print '上传至服务器完成[=========================] 100%  ', "文件上传至:%s" % (target_add)
    except:
        print '本地未找到该文件! '

    t.close()


#将服务器下载到本地
#com_add为服务器文件路径， target_add为本地文件路径
#svr_add为服务器地址
def getFileToLocal(com_add, target_add, svr_add, username, psd):
    t = paramiko.Transport((svr_add, 22))
    t.connect(username=username, password=psd)
    sftp = paramiko.SFTPClient.from_transport(t)
    # com_add = '/home/cln/ryn.tar'
    # target_add = raw_input('输入文件存放地址:')
    # target_add = 'd:\\sshclient\\ryn.tar'
    try:
        sftp.get(com_add, target_add)
        print '下载至本地完成[=========================] 100%  \n', "文件存放在:%s" % (target_add)
    except:
        print '服务器没有该文件! \n'

    sftp.close()


#将服务器上的tar压缩包解压
#tar_add 文件路径, tarTxt 文件名
def tarFile(tar_add, tarTxt, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    com = 'cd %s; tar -xf %s'% (tar_add, tarTxt)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print stdout.read()
        print '解压成功!'
    except Exception as e:
        print '解压失败!'
    finally:
        ssh.close()

#压缩文件
#tar_add 文件路径, tarTxt 文件名
def tar_zcvf_file(tar_add, tarfile, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    date = datetime.datetime.now().strftime('%Y%m%d')
    tarfile_date = tarfile + date
    com = 'cd %s; tar -zcvf %s %s'% (tar_add, tarfile_date, tarfile)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print stdout.read()
        print '压缩成功!'
    except Exception as e:
        print '压缩失败!'
    finally:
        ssh.close()


#重命名文件
def renameFile(file_local, target_file, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    date = datetime.datetime.now().strftime('%Y%m%d')
    target_file_date = target_file + date
    com = 'cd %s; mv %s %s'% (file_local, target_file, target_file_date)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print("重命名完成!")
    except Exception as e:
        print("重命名失败!")
    finally:
        ssh.close()


#删除文件
def delFile(tarTxt, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    com = 'rm -rf %s' % (tarTxt)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print("删除原文件完成!")
    except Exception as e:
        print("删除原文件失败!")
    finally:
        ssh.close()


#更改仓储的server_conf.py配置文件
def changeServer_confFile(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/cln/wh/config/server_conf.py'
        target_txt = 'd:\\sshclient\\server_conf.py'
        target_txt1 = 'd:\\sshclient\\server_conf1.py'
    # getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if "server_port" in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = 'server_port = 7777'
                        # fp2.write(s)
                        print "更改 server——port 成功 %s"%(lenght[i])
                    if "server_ip" in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = "server_ip = '180.2.32.20'"
                        print "更改 server——ip 成功 %s"%(lenght[i])

                    fp2.write(lenght[i])
        print 'server_conf配置文件更改完成，存储为%s'%(target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
            # fp2.close()
    # putFileToServer('d:\\sshclient\\text\\text.py', '/home/cln/ryn/')
    # delFile(com_txt)
    # putFileToServer(target_txt, '/home/cln/wh/wh/config/')
    # renameFile(com_txt, '/home/cln/ryn/config.txt')


#更改仓储的ip_conf.py配置文件
def changeIpconfFile(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/cln/wh/config/server_conf.py'
        target_txt = 'd:\\sshclient\\ip_conf.py'
        target_txt1 = 'd:\\sshclient\\ip_conf1.py'
    # com_txt = '/home/cln/wh/config/ip_conf.py'
    # target_txt = 'd:\\sshclient\\text\\ip_conf.py'
    # getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    ip_white_lst = '''ip_white_lst = [
    ('180.2.35.63', '1'),  # '1' member server
    ('180.2.31.229', '2'),  # '2' acsvr_wh
    ('180.2.35.36', '3'),  # '3' business server
    ('180.2.35.37', '4'),  # '4' warehouse server
    ('180.2.32.20', '5'),  # '5' watch server
'''
    try:
        with open(target_txt, 'r') as fp1:
            lenght = fp1.read()
            print("正在读取原数据...")
            # for i in range(len(lenght)):
            with open(target_txt1, 'w') as fp2:
                # if
                # s = re.sub(r'server_ip = \'(\w+, )+', '180.2.32.20', lenght)
                s = re.sub(r'ip_white_lst = (.*)', '%s'% (ip_white_lst), lenght)
                print >> fp2, s
                print("更改成功。")
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()
    # putFileToServer('d:\\sshclient\\text\\text.py', '/home/cln/ryn/')
    # renameFile(com_txt, '/home/cln/ryn/config.txt')
    # delFile(com_txt)
    # putFileToServer(target_txt, '/home/cln/wh/wh/config/')


#更改仓储的db_conf.py配置文件
def changeDBconfFile(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/cln/wh/config/db_conf.py'
        target_txt = 'd:\\sshclient\\db_conf.py'
        target_txt1 = 'd:\\sshclient\\db_conf1.py'
    # com_txt = '/home/cln/wh/config/db_conf.py'
    # target_txt = 'd:\\sshclient\\text\\db_conf.py'
    # getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    db_conf = '''#!/usr/bin/python
#coding:utf-8
        
        
db_conf = {
        "main": {
                "pwd": "@enc@dmj/PFlLa04C5Q==",
                "user": "REG_USER",
                "sid": "180.2.35.69:1521/sgeregdb"
        },

        "cln": {
                "pwd": "@enc@dmj/PFlLa04C5Q==",
                "user": "CLN_USER",
                "sid": "180.2.35.146:1521/sgeclndb"
        },

        "his": {
                "pwd": "@enc@dmj/PFlLa04C5Q==",
                "user": "his",
                "sid": "180.2.35.143:1521/sgehisdb"
        },

        "etf": {
                "pwd": "@enc@dmj/PFlLa04C5Q==",
                "user": "ETF_USER",
                "sid": "180.2.35.68:1521/sgetradb"
        }
}'''
    try:
        with open(target_txt, 'r') as fp1:
            lenght = fp1.read()
            print("正在读取原数据...")
            # for i in range(len(lenght)):
            with open(target_txt1, 'w') as fp2:
                # s = re.sub(r'server_ip = \'(\w+, )+', '180.2.32.20', lenght)
                # s = re.sub(r'db_conf = (.*)', '%s'% (db_conf), lenght)
                s = db_conf
                print >> fp2, s
                print("更改成功。")
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()
    # putFileToServer('d:\\sshclient\\text\\text.py', '/home/cln/ryn/')
    # renameFile(com_txt, '/home/cln/ryn/config.txt')
    # delFile(com_txt)
    # putFileToServer(target_txt, '/home/cln/wh/wh/config/')


#更改交易前置acsvr
def change_tra_acsvr(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/sge/install/acsvrA/conf/acsvr.cfg'
        target_txt = 'd:\\sshclient\\acsvr.cfg'
        target_txt1 = 'd:\\sshclient\\acsvr1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/acsvr",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s"%(lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i]=''
                        lenght[i] = '        "grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                        print "更改 grp_cfg 成功 %s"%(lenght[i])

                    fp2.write(lenght[i])
        print 'acsvr配置文件更改完成，存储为%s'%(target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改交易前置quotaacsvr
def change_tra_quotaacsvr(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/reg1/wh/config/quotaacsvr.cfg'
        target_txt = 'd:\\sshclient\\quotaacsvr.cfg'
        target_txt1 = 'd:\\sshclient\\quotaacsvr1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/quotaacsvr",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'quotaacsvr配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改交易前置intacsvr
def change_tra_intacsvr(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/sge/install/intacsvr/conf/intacsvr.cfg'
        target_txt = 'd:\\sshclient\\intacsvr.cfg'
        target_txt1 = 'd:\\sshclient\\intacsvr1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/intacsvr",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'intacsvr配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改登记前置acct
def change_reg_acct(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/reg1/install/acsvr_acct/conf/acsvr_acct.cfg'
        target_txt = 'd:\\sshclient\\acsvr_acct.cfg'
        target_txt1 = 'd:\\sshclient\\acsvr_acct1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/acsvr_acct",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" : "/nfs/conf/reg_group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'acsvr_acct配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改登记前置bank
def change_reg_bank(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/reg1/install/acsvr_bank/conf/acsvr_bank.cfg'
        target_txt = 'd:\\sshclient\\acsvr_bank.cfg'
        target_txt1 = 'd:\\sshclient\\acsvr_bank1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/acsvr_bank_encrypt",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" : "/nfs/conf/reg_group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'acsvr_bank配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改登记前置wm
def change_reg_wm(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/reg1/install/acsvr_wm/conf/acsvr_wm.cfg'
        target_txt = 'd:\\sshclient\\acsvr_wm.cfg'
        target_txt1 = 'd:\\sshclient\\acsvr_wm1.cfg'
    try:
        with open(target_txt, 'r+') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            for i in range(len(lenght)):
                # print 'lenght %s' %(lenght[i])
                with open(target_txt1, 'a') as fp2:
                    if '"name"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                        # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                        lenght[i] = ''
                        lenght[i] = '        "name" : "/ssd/log/acsvr_wm",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" : "/nfs/conf/reg_group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'acsvr_wm配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()

#更改etf前置etfsvr
def change_etf_etfsvr():
    pass

#将仓储的三个配置文件上传到服务器上
def putSomeFile(local_add, svr_conf_add, svr_add, username, psd):
    filename = ['server_conf1.py', 'db_conf1.py', 'ip_conf1.py']
    filename1 = ['server_conf.py', 'db_conf.py', 'ip_conf.py']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    # com = 'cd /home/cln/ryn/; tar -xf %s' % ('ryn.tar')
    # stdin, stdout, stderr = ssh.exec_command(com)
    for i in range(len(filename)):
        comTxt = '%s\\%s'%(local_add, filename[i])
        tarTxt = '%s/%s'%(svr_conf_add, filename1[i])
        delTxt = '%s/%s' %(svr_conf_add, filename1[i])
        delFile(delTxt, svr_add, username, psd)
        putFileToServer(comTxt, tarTxt, svr_add, username, psd)
        # txt = '/home/cln/wh/config/%s' %(filename[i])
        # renameFile(txt, delTxt, svr_add, username, psd)
        print "删除服务器原文件-- %s --完成，上传且重命名本地文件-- %s --完成。\n"%(filename1[i], filename[i])


#将仓储的三个配置文件下载到本地
def getAllFile( svr_conf_add, local_add, svr_add, username, psd):
    filename = ['server_conf.py', 'db_conf.py', 'ip_conf.py']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    # com = 'cd /home/cln/ryn/; tar -xf %s' % ('ryn.tar')
    # stdin, stdout, stderr = ssh.exec_command(com)
    for i in range(len(filename)):
        tarTxt = '%s\\%s' % (local_add, filename[i])
        # tarTxt = '/home/cln/wh/wh/config/'
        comTxt = '%s/%s' % (svr_conf_add, filename[i])
        getFileToLocal(comTxt, tarTxt)


#仓储更换版本
#svr_conf_add1 一般是新版本服务器地址：182.2.35.130
#local_add 是本地文件夹： d:\\sshclient
#svr_conf_add2 一般是仓储服务器：/home/reg1/wh/config/
def cangchu(svr_conf_add1, local_add, svr_conf_add2 ):
    try:
        tar_tar = local_add + '\\wh.tar.gz'
        getFileToLocal(svr_conf_add1, tar_tar, '182.2.35.130', 'zhiban', 'zhiban')
        print "压缩包下载本地完成！"

        tar_svr_add = svr_conf_add2 + 'wh.tar.gz'
        putFileToServer(tar_tar, tar_svr_add, '182.2.32.20', 'reg1', 'reg1')
        print "压缩包上传服务器完成！"

        #将原来的文件重命名备份
        renameFile('/home/reg1','wh', '182.2.32.20', 'reg1', 'reg1')
        print "wh原文件重命名完成！"

        tarFile(svr_conf_add2, 'wh.tar.gz', '182.2.32.20', 'reg1', 'reg1')
        print '解压 wh.tar.gz 完成！'

        getAllFile(svr_conf_add2, local_add, '182.2.32.20', 'reg1', 'reg1')
        print "下载文件完成！"

        tar_svr = local_add + '\\server_conf.py'
        tar_svr2 = local_add + '\\server_conf1.py'
        changeServer_confFile(tar_svr, tar_svr2)

        tar_ip = local_add + '\\ip_conf.py'
        tar_ip2 = local_add + '\\ip_conf1.py'
        changeIpconfFile(tar_ip, tar_ip2)

        tar_db = local_add + '\\db_conf.py'
        tar_db2 = local_add + '\\db_conf1.py'
        changeDBconfFile(tar_db, tar_db2)
        print "更改文件完成！"

        putSomeFile(local_add, svr_conf_add2, '182.2.32.20', 'reg1', 'reg1')
        print "上传文件完成！"
    except Exception as e:
        print "更换失败！"
    except IOError as e:
        print "文件更改出错！"



def main():
    flag = True
    while flag:
        print "\n根据下面提示输入指令:\n"
        com = raw_input("1.先下载，2.再上传，3.再解压，4.再下载文件更改，5.再删除服务器上的后再上传: \n"
                        "输入指令, 退出为 quit，下载为 get， 上传为 put，解压为 tar，\n "
                        "删除服务器文件 为 del， \n"
                        "更改server_conf.py文件 为 server， \n"
                        "更改db_conf.py文件 为 dbconf， \n"
                        "更改ip_conf.py文件 为 ipconf， \n"
                        "将全部改后的配置文件上传到服务器 为 putallfile， \n"
                        "下载全部配置文件 getallfile ,\n" 
                        "换仓储核心 1 ，\n"
                        "请输入指令：")
        if com == 'quit':
            flag = False
        elif com == 'get':
            #输入下载的服务器地址
            print "从服务器下载文件到本地..."
            svr_add = raw_input("输入服务器地址: ")
            username = raw_input("输入服务器用户名: ")
            psd = raw_input("输入服务器密码: ")
            com_add = raw_input('输入服务器上的文件地址(文件名称写清楚，如： /home/cln/ryn.tar): ')
            target_add = raw_input('输入文件存放本地地址(文件名称写清楚且在文件名加 1，如： "d:\\sshclient\\ryn1.tar"): ')
            queren = raw_input("重新检查地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            getFileToLocal(com_add, target_add, svr_add, username, psd)
            print "---------------完成该操作-----------------"
        elif com == 'put':
            # 输入下载的服务器地址
            print "将本地文件上传到服务器..."
            svr_add = raw_input("输入服务器地址: ")
            username = raw_input("输入服务器用户名: ")
            psd = raw_input("输入服务器密码: ")
            com_add = raw_input('输入文件存放的本地地址(文件名称写清楚，如： "d:\\sshclient\\ryn1.tar"): ')
            target_add = raw_input('输入服务器上的文件夹地址(文件名称写清楚，如： /home/cln/ryn.tar): ')
            queren = raw_input("重新检查配置 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            putFileToServer(com_add, target_add, svr_add, username, psd)
            print "---------------完成该操作-----------------"
        elif com == 'del':
            svr_add = raw_input("输入服务器地址: ")
            username = raw_input("输入服务器用户名: ")
            psd = raw_input("输入服务器密码: ")
            print "删除服务器%s上的文件..."%(svr_add)
            target_txt = raw_input("输入要删除的文件的完整路径 如( /home/cln/wh/config/server_conf.py )：")
            queren = raw_input("重新检查地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            delFile(target_txt, svr_add, username, psd)
            print "---------------完成该操作-----------------"
        elif com == 'putallfile':
            svr_add = raw_input("输入服务器地址: ")
            username = raw_input("输入服务器用户名: ")
            psd = raw_input("输入服务器密码: ")
            print "上传的服务器是%s，上传注意检查"%(svr_add)
            local_add = raw_input("输入本地文件地址 如（d:\\sshclient\\server_conf.py）")
            svr_conf_add = raw_input("输入服务器的路径 如（/home/cln/wh/config/server_conf.py）")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            print "上传更改后的全部配置文件，且删除服务器原配置文件.. \n"
            putSomeFile(local_add,svr_conf_add, svr_add, username, psd)
            print "---------------完成该操作-----------------"
        elif com == 'getallfile':
            print "下载全部配置文件... \n"
            svr_add = raw_input("输入服务器地址: ")
            username = raw_input("输入服务器用户名: ")
            psd = raw_input("输入服务器密码: ")
            print "上传的服务器是%s，上传注意检查"%(svr_add)
            local_add = raw_input("输入本地文件地址 如（d:\\sshclient）")
            svr_conf_add = raw_input("输入服务器的路径 如（/home/cln/wh/config）")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            getAllFile(svr_conf_add, local_add, svr_add, username, psd)
            print "---------------完成该操作-----------------"
        elif com == 'server':
            print "更改 Server_conf 配置文件 \n"
            # com_add = raw_input('输入文件存放的本地地址(文件名称写清楚，如： "d:\\sshclient\\server_conf.py"): ')
            target_txt = raw_input('输入文件存放的本地地址(文件名称写清楚，如： d:\\sshclient\\server_conf.py): ')
            target_txt1 = raw_input('输入文件存放的本地地址(文件名称写清楚建议加 1，如： d:\\sshclient\\server_conf1.py): ')
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            changeServer_confFile(target_txt, target_txt1)
            print "---------------完成该操作-----------------"
        elif com == 'ipconf':
            print "更改 ip_conf 配置文件 \n"
            target_txt = raw_input('输入文件存放的本地地址(文件名称写清楚，如： d:\\sshclient\\ip_conf.py): ')
            target_txt1 = raw_input('输入文件存放的本地地址(文件名称写清楚建议加 1，如： d:\\sshclient\\ip_conf1.py): ')
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            changeIpconfFile(target_txt, target_txt1)
            print "---------------完成该操作-----------------"
        elif com == 'dbconf':
            print "更改 db_conf 配置文件 \n"
            target_txt = raw_input('输入文件存放的本地地址(文件名称写清楚，如： d:\\sshclient\\db_conf.py): ')
            target_txt1 = raw_input('输入文件存放的本地地址(文件名称写清楚建议加 1，如： d:\\sshclient\\db_conf1.py): ')
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            changeDBconfFile(target_txt,target_txt1)
            print "---------------完成该操作-----------------"
        elif com == 'tar':
            print "开始解压服务器上的文件... \n"
            tarTxt = raw_input("输入要解压的文件名称，(即put时设置的服务器上传文件名称，如 ryn.tar):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            tarFile(tarTxt)
            print "---------------完成该操作-----------------"

        elif com == '1':
            print "开始更换仓储核心... \n"
            svr_conf_add = raw_input("输入最新仓储核心地址，(如 ryn.tar):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...\n")
            if queren == "99":
                    continue
            cangchu(tarTxt)
            print "---------------完成更换仓储核心操作-----------------"

        else:
            print "没有该命令，请重新输入: \n"

if __name__ == "__main__":
    main()
