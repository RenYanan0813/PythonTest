# -*- coding:utf-8 -*-

'''py: 2.7'''

import paramiko
import wh_config
import os
import datetime
import re



#创建本地文件夹
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

        print path + ' 创建成功'
        # return TrueF
    else:
        print path + ' 目录已存在'
        # return False


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


#通用，重命名文件
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
    finally:
        sftp.close()
        t.close()


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
    finally:
        t.close()
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


#将仓储的三个配置文件下载到本地
def getAllFile( svr_conf_add, local_add, svr_add, username, psd):
    filename = ['server_conf.py', 'db_conf.py', 'ip_conf.py']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    # com = 'cd /home/cln/ryn/; tar -xf %s' % ('ryn.tar')
    # stdin, stdout, stderr = ssh.exec_command(com)
    for i in range(len(filename)):
        tarTxt = '%s%s' % (local_add, filename[i])
        # tarTxt = '/home/cln/wh/wh/config/'
        comTxt = '%s%s' % (svr_conf_add, filename[i])
        getFileToLocal(comTxt, tarTxt, svr_add, username, psd)


# 更改仓储的server_conf.py配置文件
def changeServer_confFile(target_txt, target_txt1):
    # if target_txt1 == '' and target_txt == '':
    #     com_txt = '/home/cln/wh/config/server_conf.py'
    #     target_txt = 'd:\\sshclient\\server_conf.py'
    #     target_txt1 = 'd:\\sshclient\\server_conf1.py'
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
                        lenght[i] = 'server_port = 12350'
                        # fp2.write(s)
                        print "更改 server——port 成功 %s" % (lenght[i])
                    if "server_ip" in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = "server_ip = '180.2.35.233'"
                        print "更改 server——ip 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'server_conf配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        # fp2.close()
    # putFileToServer('d:\\sshclient\\text\\text.py', '/home/cln/ryn/')
    # delFile(com_txt)
    # putFileToServer(target_txt, '/home/cln/wh/wh/config/')
    # renameFile(com_txt, '/home/cln/ryn/config.txt')


# 更改仓储的ip_conf.py配置文件
def changeIpconfFile(target_txt, target_txt1):
    # if target_txt1 == '' and target_txt == '':
    #     com_txt = '/home/cln/wh/config/server_conf.py'
    #     target_txt = 'd:\\sshclient\\ip_conf.py'
    #     target_txt1 = 'd:\\sshclient\\ip_conf1.py'
    # com_txt = '/home/cln/wh/config/ip_conf.py'
    # target_txt = 'd:\\sshclient\\text\\ip_conf.py'
    # getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    ip_white_lst = '''ip_white_lst = [
    ('180.2.35.189','1'),  # '1' member server
    ('180.2.35.234','2'),  # '2' acsvr_wh
    ('180.2.35.188','3'),  # '3' business server
    ('180.2.35.233','5'),  # '5' watch server

'''
    try:
        with open(target_txt, 'r') as fp1:
            lenght = fp1.read()
            print("正在读取原数据...")
            # for i in range(len(lenght)):
            with open(target_txt1, 'w') as fp2:
                # if
                # s = re.sub(r'server_ip = \'(\w+, )+', '180.2.32.20', lenght)
                s = re.sub(r'ip_white_lst = (.*)', '%s' % (ip_white_lst), lenght)
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


# 更改仓储的db_conf.py配置文件
def changeDBconfFile(target_txt, target_txt1):
    # if target_txt1 == '' and target_txt == '':
    #     com_txt = '/home/cln/wh/config/db_conf.py'
    #     target_txt = 'd:\\sshclient\\db_conf.py'
    #     target_txt1 = 'd:\\sshclient\\db_conf1.py'
    # com_txt = '/home/cln/wh/config/db_conf.py'
    # target_txt = 'd:\\sshclient\\text\\db_conf.py'
    # getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    db_conf = '''#!/usr/bin/python
#coding:utf-8

db_conf = {
    "main": {
        "pwd": "@enc@Vmj/PFlLa04C5Q==", 
        "user": "reg_user", 
        "sid": "180.2.35.222:1521/sgeregdb"
    }, 
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
        comTxt = '%s%s'%(local_add, filename[i])
        tarTxt = '%s%s'%(svr_conf_add, filename1[i])
        delTxt = '%s%s' %(svr_conf_add, filename1[i])
        delFile(delTxt, svr_add, username, psd)
        putFileToServer(comTxt, tarTxt, svr_add, username, psd)
        # txt = '/home/cln/wh/config/%s' %(filename[i])
        # renameFile(txt, delTxt, svr_add, username, psd)
        print "删除服务器原文件-- %s --完成，上传且重命名本地文件-- %s --完成。\n"%(filename1[i], filename[i])


def cangchu():
    new_wh_add = wh_config.new_wh['new_wh_address'] + wh_config.new_wh['new_wh_file']
    local_add_file = '%swh%s.tar.gz' % (wh_config.local_wh['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    wh_config.old_wh['new_wh_file'] = 'wh%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_wh_add, local_add_file, wh_config.new_wh['hostname'], wh_config.new_wh['username'], wh_config.new_wh['password'])
    print "最新版wh压缩包下载本地完成！"

    old_wh_add = '%swh%s.tar.gz'%(wh_config.old_wh['old_wh_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file , old_wh_add, wh_config.old_wh['hostname'], wh_config.old_wh['username'], wh_config.old_wh['password'])
    print "将新版本wh压缩包上传至wh服务器完成！"

    #将原来的文件重命名备份
    renameFile(wh_config.old_wh['old_wh_address'],'wh', wh_config.old_wh['hostname'], wh_config.old_wh['username'], wh_config.old_wh['password'])
    print "wh旧版本文件重命名完成！"

    tarFile(wh_config.old_wh['old_wh_address'], wh_config.old_wh['new_wh_file'], wh_config.old_wh['hostname'], wh_config.old_wh['username'], wh_config.old_wh['password'])
    print '解压 wh{date}.tar.gz 完成！'

    getAllFile(wh_config.old_wh['old_wh_conf_add'], wh_config.local_wh['local_address'], wh_config.old_wh['hostname'], wh_config.old_wh['username'], wh_config.old_wh['password'])
    print "下载wh需要更改的配置文件完成！"

    tar_svr = wh_config.local_wh['local_address'] + 'server_conf.py'
    tar_svr2 = wh_config.local_wh['local_address'] + 'server_conf1.py'
    changeServer_confFile(tar_svr, tar_svr2)
    print "server_conf.py 修改完成！"

    tar_ip = wh_config.local_wh['local_address'] + 'ip_conf.py'
    tar_ip2 = wh_config.local_wh['local_address'] + 'ip_conf1.py'
    changeIpconfFile(tar_ip, tar_ip2)
    print "ip_conf.py 修改完成！"

    tar_db = wh_config.local_wh['local_address'] + 'db_conf.py'
    tar_db2 = wh_config.local_wh['local_address'] + 'db_conf1.py'
    changeDBconfFile(tar_db, tar_db2)
    print "db_conf.py 修改完成！"

    putSomeFile(wh_config.local_wh['local_address'], wh_config.old_wh['old_wh_conf_add'], wh_config.old_wh['hostname'], wh_config.old_wh['username'], wh_config.old_wh['password'])
    print "上传文件完成！"


#查看仓储服务状态
def check_wh_state():
    pass
    # ssh = paramiko.SSHClient()
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(hostname=svr_add, username=username, password=psd)


#启动仓储服务
def run_wh_svr():
    pass

#停止仓储服务
def stop_wh_svr():
    pass

def main():
    flag = True
    while flag:
        print "\n根据下面提示输入指令:\n"
        com = raw_input("1) 查看仓储服务状态(没写)       2) 停止仓储服务(没写) \n"
                        "3) 启动换仓储服务 (没写)        4) 更换仓储版本 \n"
                        "5) 退出 \n"
                        " 请输入指令：")
        if com == '99':
            continue
        elif com == '1':
            print "开始查看仓储服务状态..."
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                continue
            check_wh_state()
            print "---------------完成 -- 查看仓储服务状态 -- 操作-----------------"
        elif com == '2':
            print "开始  停止仓储服务..."
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                continue
            stop_wh_svr()
            print "---------------完成 -- 停止仓储服务 -- 操作-----------------"
        elif com == '3':
            print "开始  启动换仓储服务..."
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                continue
            run_wh_svr()
            print "---------------完成 -- 启动换仓储服务 -- 操作-----------------"
        elif com == '4':
            print "开始更换仓储核心... \n"
            wh_config.new_wh['new_wh_address'] = raw_input("输入最新仓储核心地址，(如 /home/zhiban/guoqing/20180822/wh/):")
            wh_config.new_wh['new_wh_file'] = raw_input("输入最新仓储核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            cangchu()
            print "---------------完成 -- 更换仓储核心 -- 操作-----------------"
        elif com == '5':
            flag = False
        else:
            print "没有该命令，请重新输入: \n"

if __name__ == "__main__":
    mkdir(wh_config.local_wh['local_address'])
    main()
    print "删除 %s"%(wh_config.local_wh['local_address'],)
    os.removedirs(wh_config.local_wh['local_address'])
    print "已删除 %s 目录" % (wh_config.local_wh['local_address'],)