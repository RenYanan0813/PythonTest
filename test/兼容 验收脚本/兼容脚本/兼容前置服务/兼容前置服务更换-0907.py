# -*- coding:utf-8 -*-

import paramiko
import re
import xlrd
import config
import datetime
import os
import shutil

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

#获取全部数据
def get_all_data(filename):
    table = xlrd.open_workbook(filename)
    data = table.sheet_by_name('Sheet1')
    row1 = data.row_values(0)
    data_list = []
    for r in xrange(1, data.nrows):
        sername = data.row_values(r)[0]  # 获取服务名
        each = data.row_values(r)  # 每一个服务对应的信息列表
        temp_dict = dict(zip(row1, each))
        temp = {sername : temp_dict}
        data_list.append(temp)
    return data_list


# 根据提供的服务名列表获取到服务器信息
def get_need_hostinfo(data_list, search_list):
    res = list(filter(lambda data: data if str(data.keys()[0]) in search_list else False, data_list))
    need_list = []
    for host in res:
        need_list.append(host.values()[0])
    return need_list


#更改交易前置acsvrA
def change_tra_acsvrA(target_txt, target_txt1):
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
                        lenght[i] = '        "name" : "/ssd/log/acsvrA",\n'
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


#更改交易前置acsvrB
def change_tra_acsvrB(target_txt, target_txt1):
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
                        lenght[i] = '        "name" : "/ssd/log/acsvrB",\n'
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
                        lenght[i] = '        "grp_cfg" : "/home/sge/group.cfg",\n'
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
                        lenght[i] = '        "grp_cfg" : "/home/sge/group.cfg",\n'
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
        com_txt = '/home/reg2/install/acsvr_acct/conf/acsvr_acct.cfg'
        target_txt = 'd:\\svrconfig\\acsvr_acct.cfg'
        target_txt1 = 'd:\\svrconfig\\acsvr_acct1.cfg'
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
                        lenght[i] = '        "name" : "/ssd/reg2/log/acsvr_acct",\n'
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
    # if target_txt1 == '' and target_txt == '':
    #     com_txt = '/home/reg1/install/acsvr_bank/conf/acsvr_bank.cfg'
    #     target_txt = 'd:\\sshclient\\acsvr_bank.cfg'
    #     target_txt1 = 'd:\\sshclient\\acsvr_bank1.cfg'
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
                    if '"bank_servers"' in lenght[i]:
                        for j in range(1, 103):
                            if '],' in lenght[i+j]:
                                break
                            else:
                                lenght[i+j] = '#' + lenght[i+j]
                                # fp2.write(lenght[i])
                        print "添加注释完成！"
                    if '北京银行' in lenght[i]:
                        lenght[i + 1] = '        {\n'
                        lenght[i + 2] = '                "end_id" : "01170000",\n'
                        lenght[i + 3] = '                "ip" : "180.2.31.299",\n'
                        lenght[i + 4] = '                "port" :18888\n'
                        lenght[i + 5] = '        },\n'

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
        com_txt = '/home/reg2/install/acsvr_wm/conf/acsvr_wm.cfg'
        target_txt = 'd:\\svrconfig\\acsvr_wm.cfg'
        target_txt1 = 'd:\\svrconfig\\acsvr_wm1.cfg'
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
                        lenght[i] = '        "name" : "/ssd/reg2/log/acsvr_wm",\n'
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
def change_etf_etfsvr(target_txt, target_txt1):
    # if target_txt1 == '' and target_txt == '':
    #     com_txt = '/home/reg1/install/acsvr_wm/conf/etfsvr.cfg'
    #     target_txt = 'd:\\sshclient\\etfsvr.cfg'
    #     target_txt1 = 'd:\\sshclient\\etfsvr.cfg'
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
                        lenght[i] = '        "name" : "/ssd/log/etfacsvr",\n'
                        # fp2.write(s)
                        print "更改 name 成功 %s" % (lenght[i])
                    if '"grp_cfg"' in lenght[i]:
                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                        # fp2.write(str(s1))
                        lenght[i] = ''
                        lenght[i] = '        "grp_cfg" :"../group.cfg",\n'
                        print "更改 grp_cfg 成功 %s" % (lenght[i])

                    fp2.write(lenght[i])
        print 'etfsvr配置文件更改完成，存储为%s' % (target_txt1)
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()


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

# 通用，重命名文件,加日期
def renameFile(file_local, target_file, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    date = datetime.datetime.now().strftime('%Y%m%d')
    target_file_date = target_file + date
    com = 'cd %s; mv %s %s' % (file_local, target_file, target_file_date)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print("重命名完成!")
    except Exception as e:
        print("重命名失败!")
    finally:
        ssh.close()

# 通用，重命名文件
def mvFile(file_local, target_file, target_file2, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    # date = datetime.datetime.now().strftime('%Y%m%d')
    # target_file_date = target_file + date
    com = 'cd %s; mv %s %s' % (file_local, target_file, target_file2)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print("重命名完成!")
    except Exception as e:
        print("重命名失败!")
    finally:
        ssh.close()

# 将服务器上的tar压缩包解压
# tar_add 文件路径, tarTxt 文件名
def tarFile(tar_add, tarTxt, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    com = 'cd %s; tar -xf %s' % (tar_add, tarTxt)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print stdout.read()
        print '解压成功!'
    except Exception as e:
        print '解压失败!'
    finally:
        ssh.close()

# 删除文件
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

#更换前置服务acsvrA
def acsvrA():
    new_acsvrA_add = config.new_acsvrA['new_acsvrA_address'] + config.new_acsvrA['new_acsvrA_file']
    local_add_file = '%sacsvrA%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvrA['new_acsvrA_file'] = 'acsvrA%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvrA_add, local_add_file, config.new_acsvrA['hostname'], config.new_acsvrA['username'],
                   config.new_acsvrA['password'])
    print "最新版acsvrA压缩包下载本地完成！"

    old_acsvrA_add = '%sacsvrA%s.tar.gz' % (
    config.old_acsvrA['old_acsvrA_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvrA_add, config.old_acsvrA['hostname'], config.old_acsvrA['username'],
                    config.old_acsvrA['password'])
    print "将新版本acsvrA压缩包上传至acsvrA服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvrA['old_acsvrA_address'], 'acsvrA', config.old_acsvrA['hostname'],
               config.old_acsvrA['username'], config.old_acsvrA['password'])
    print "acsvrA旧版本文件重命名完成！"

    tarFile(config.old_acsvrA['old_acsvrA_address'], config.old_acsvrA['new_acsvrA_file'],
            config.old_acsvrA['hostname'], config.old_acsvrA['username'], config.old_acsvrA['password'])
    print '解压 acsvrA{date}.tar.gz 完成！'

    delFile(old_acsvrA_add, config.old_acsvrA['hostname'], config.old_acsvrA['username'],
            config.old_acsvrA['password'])
    print "删除 acsvrA{date}.tar.gz 压缩包完成！"

    mvFile(config.old_acsvrA['old_acsvrA_address'], 'acsvr', 'acsvrA', config.old_acsvrA['hostname'],
           config.old_acsvrA['username'], config.old_acsvrA['password'])
    print "acsvrA新版本文件重命名完成！"

    new_cfg = config.old_acsvrA['old_acsvrA_conf_add'] + config.old_acsvrA['acsvrA_conf_file']
    local_acsvrA_conf_file = '%s%s' % (config.local_svr['local_address'], config.old_acsvrA['acsvrA_conf_file'])
    getFileToLocal(new_cfg, local_acsvrA_conf_file, config.old_acsvrA['hostname'],
                   config.old_acsvrA['username'], config.old_acsvrA['password'])
    print "下载acsvrA需要更改的配置文件完成！"

    local_acsvrA_conf_file1 = '%s%s1' % (config.local_svr['local_address'], config.old_acsvrA['acsvrA_conf_file'])
    change_tra_acsvrA(local_acsvrA_conf_file, local_acsvrA_conf_file1)
    print "更改acsvrA配置文件完成！"

    # 上传到服务器上的文件
    old_acsvrA_conf_file = '%s%s' % (config.old_acsvrA['old_acsvrA_conf_add'], config.old_acsvrA['acsvrA_conf_file'])

    # 删除服务器上的原文件
    delFile(old_acsvrA_conf_file, config.old_acsvrA['hostname'], config.old_acsvrA['username'],
            config.old_acsvrA['password'])
    print "删除原acsvrA配置文件完成！"

    # 上传到服务器上的文件
    old_acsvrA_conf_file = '%s%s' % (config.old_acsvrA['old_acsvrA_conf_add'], config.old_acsvrA['acsvrA_conf_file'])
    putFileToServer(local_acsvrA_conf_file1, old_acsvrA_conf_file, config.old_acsvrA['hostname'],
                    config.old_acsvrA['username'], config.old_acsvrA['password'])
    print "上传更改后的acsvrA配置文件至服务器完成"

#更换前置服务acsvrB
def acsvrB():
    new_acsvrB_add = config.new_acsvrB['new_acsvrB_address'] + config.new_acsvrB['new_acsvrB_file']
    local_add_file = '%sacsvrB%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvrB['new_acsvrB_file'] = 'acsvrB%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvrB_add, local_add_file, config.new_acsvrB['hostname'], config.new_acsvrB['username'],
                   config.new_acsvrB['password'])
    print "最新版acsvrB压缩包下载本地完成！"

    old_acsvrB_add = '%sacsvrB%s.tar.gz' % (
    config.old_acsvrB['old_acsvrB_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvrB_add, config.old_acsvrB['hostname'], config.old_acsvrB['username'],
                    config.old_acsvrB['password'])
    print "将新版本acsvrB压缩包上传至acsvrB服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvrB['old_acsvrB_address'], 'acsvrB', config.old_acsvrB['hostname'],
               config.old_acsvrB['username'], config.old_acsvrB['password'])
    print "acsvrB旧版本文件重命名完成！"

    tarFile(config.old_acsvrB['old_acsvrB_address'], config.old_acsvrB['new_acsvrB_file'],
            config.old_acsvrB['hostname'], config.old_acsvrB['username'], config.old_acsvrB['password'])
    print '解压 acsvrB{date}.tar.gz 完成！'

    delFile(old_acsvrB_add, config.old_acsvrB['hostname'], config.old_acsvrB['username'],
                    config.old_acsvrB['password'])
    print "删除 acsvrB{date}.tar.gz 压缩包完成！"

    mvFile(config.old_acsvrB['old_acsvrB_address'], 'acsvr', 'acsvrB', config.old_acsvrB['hostname'],
               config.old_acsvrB['username'], config.old_acsvrB['password'])
    print "acsvrB新版本文件重命名完成！"

    new_cfg = config.old_acsvrB['old_acsvrB_conf_add'] + config.old_acsvrB['acsvrB_conf_file']
    local_acsvrB_conf_file = '%s%s' % (config.local_svr['local_address'], config.old_acsvrB['acsvrB_conf_file'])
    getFileToLocal(new_cfg, local_acsvrB_conf_file, config.old_acsvrB['hostname'],
                   config.old_acsvrB['username'], config.old_acsvrB['password'])
    print "下载acsvrB需要更改的配置文件完成！"

    local_acsvrB_conf_file1 = '%s%s1' % (config.local_svr['local_address'], config.old_acsvrB['acsvrB_conf_file'])
    change_tra_acsvrB(local_acsvrB_conf_file, local_acsvrB_conf_file1)
    print "更改acsvrB配置文件完成！"

    # 上传到服务器上的文件
    old_acsvrB_conf_file = '%s%s' % (config.old_acsvrB['old_acsvrB_conf_add'], config.old_acsvrB['acsvrB_conf_file'])

    # 删除服务器上的原文件
    delFile(old_acsvrB_conf_file, config.old_acsvrB['hostname'], config.old_acsvrB['username'],
            config.old_acsvrB['password'])
    print "删除原acsvrB配置文件完成！"

    # 上传到服务器上的文件
    old_acsvrB_conf_file = '%s%s' % (config.old_acsvrB['old_acsvrB_conf_add'], config.old_acsvrB['acsvrB_conf_file'])
    putFileToServer(local_acsvrB_conf_file1, old_acsvrB_conf_file, config.old_acsvrB['hostname'],
                    config.old_acsvrB['username'], config.old_acsvrB['password'])
    print "上传更改后的acsvrB配置文件至服务器完成"

#更换前置服务quotaacsvr
def quotaacsvr():
    new_quotaacsvr_add = config.new_quotaacsvr['new_quotaacsvr_address'] + config.new_quotaacsvr['new_quotaacsvr_file']
    local_add_file = '%squotaacsvr%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_quotaacsvr['new_quotaacsvr_file'] = 'quotaacsvr%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_quotaacsvr_add, local_add_file, config.new_quotaacsvr['hostname'],
                   config.new_quotaacsvr['username'], config.new_quotaacsvr['password'])
    print "最新版quotaacsvr压缩包下载本地完成！"

    old_quotaacsvr_add = '%squotaacsvr%s.tar.gz' % (
    config.old_quotaacsvr['old_quotaacsvr_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_quotaacsvr_add, config.old_quotaacsvr['hostname'],
                    config.old_quotaacsvr['username'], config.old_quotaacsvr['password'])
    print "将新版本quotaacsvr压缩包上传至quotaacsvr服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_quotaacsvr['old_quotaacsvr_address'], 'quotaacsvr', config.old_quotaacsvr['hostname'],
               config.old_quotaacsvr['username'], config.old_quotaacsvr['password'])
    print "quotaacsvr旧版本文件重命名完成！"

    tarFile(config.old_quotaacsvr['old_quotaacsvr_address'], config.old_quotaacsvr['new_quotaacsvr_file'],
            config.old_quotaacsvr['hostname'], config.old_quotaacsvr['username'], config.old_quotaacsvr['password'])
    print '解压 quotaacsvr{date}.tar.gz 完成！'

    delFile(old_quotaacsvr_add, config.old_quotaacsvr['hostname'], config.old_quotaacsvr['username'],
            config.old_quotaacsvr['password'])
    print "删除 quotaacsvr{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_quotaacsvr['old_quotaacsvr_conf_add'] + config.old_quotaacsvr['quotaacsvr_conf_file']
    local_quotaacsvr_conf_file = '%s%s' % (
    config.local_svr['local_address'], config.old_quotaacsvr['quotaacsvr_conf_file'])
    getFileToLocal(new_cfg, local_quotaacsvr_conf_file,
                   config.old_quotaacsvr['hostname'], config.old_quotaacsvr['username'],
                   config.old_quotaacsvr['password'])
    print "下载quotaacsvr需要更改的配置文件完成！"

    local_quotaacsvr_conf_file1 = '%s%s1' % (
    config.local_svr['local_address'], config.old_quotaacsvr['quotaacsvr_conf_file'])
    change_tra_quotaacsvr(local_quotaacsvr_conf_file, local_quotaacsvr_conf_file1)
    print "更改quotaacsvr配置文件完成！"

    # 上传到服务器上的文件
    old_quotaacsvr_conf_file = '%s%s' % (
    config.old_quotaacsvr['old_quotaacsvr_conf_add'], config.old_quotaacsvr['quotaacsvr_conf_file'])

    # 删除服务器上的原文件
    delFile(old_quotaacsvr_conf_file, config.old_quotaacsvr['hostname'], config.old_quotaacsvr['username'],
            config.old_quotaacsvr['password'])
    print "删除原quotaacsvr配置文件完成！"

    # 上传到服务器上的文件
    old_quotaacsvr_conf_file = '%s%s' % (
    config.old_quotaacsvr['old_quotaacsvr_conf_add'], config.old_quotaacsvr['quotaacsvr_conf_file'])
    putFileToServer(local_quotaacsvr_conf_file1, old_quotaacsvr_conf_file, config.old_quotaacsvr['hostname'],
                    config.old_quotaacsvr['username'], config.old_quotaacsvr['password'])
    print "上传更改后的quotaacsvr配置文件至服务器完成"


#更换前置服务intacsvr
def intacsvr():
    new_intacsvr_add = config.new_intacsvr['new_intacsvr_address'] + config.new_intacsvr['new_intacsvr_file']
    local_add_file = '%sintacsvr%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_intacsvr['new_intacsvr_file'] = 'intacsvr%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_intacsvr_add, local_add_file, config.new_intacsvr['hostname'], config.new_intacsvr['username'],
                   config.new_intacsvr['password'])
    print "最新版intacsvr压缩包下载本地完成！"

    old_intacsvr_add = '%sintacsvr%s.tar.gz' % (
    config.old_intacsvr['old_intacsvr_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_intacsvr_add, config.old_intacsvr['hostname'], config.old_intacsvr['username'],
                    config.old_intacsvr['password'])
    print "将新版本intacsvr压缩包上传至intacsvr服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_intacsvr['old_intacsvr_address'], 'intacsvr', config.old_intacsvr['hostname'],
               config.old_intacsvr['username'], config.old_intacsvr['password'])
    print "intacsvr旧版本文件重命名完成！"

    tarFile(config.old_intacsvr['old_intacsvr_address'], config.old_intacsvr['new_intacsvr_file'],
            config.old_intacsvr['hostname'], config.old_intacsvr['username'], config.old_intacsvr['password'])
    print '解压 intacsvr{date}.tar.gz 完成！'

    delFile(old_intacsvr_add, config.old_intacsvr['hostname'], config.old_intacsvr['username'],
            config.old_intacsvr['password'])
    print "删除 intacsvr{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_intacsvr['old_intacsvr_conf_add'] + config.old_intacsvr['intacsvr_conf_file']
    local_intacsvr_conf_file = '%s%s' % (config.local_svr['local_address'], config.old_intacsvr['intacsvr_conf_file'])
    getFileToLocal(new_cfg, local_intacsvr_conf_file, config.old_intacsvr['hostname'],
                   config.old_intacsvr['username'], config.old_intacsvr['password'])
    print "下载intacsvr需要更改的配置文件完成！"

    local_intacsvr_conf_file1 = '%s%s1' % (config.local_svr['local_address'], config.old_intacsvr['intacsvr_conf_file'])
    change_tra_intacsvr(local_intacsvr_conf_file, local_intacsvr_conf_file1)
    print "更改intacsvr配置文件完成！"

    # 上传到服务器上的文件
    old_intacsvr_conf_file = '%s%s' % (
    config.old_intacsvr['old_intacsvr_conf_add'], config.old_intacsvr['intacsvr_conf_file'])

    # 删除服务器上的原文件
    delFile(old_intacsvr_conf_file, config.old_intacsvr['hostname'], config.old_intacsvr['username'],
            config.old_intacsvr['password'])
    print "删除原intacsvr配置文件完成！"

    # 上传到服务器上的文件
    old_intacsvr_conf_file = '%s%s' % (
    config.old_intacsvr['old_intacsvr_conf_add'], config.old_intacsvr['intacsvr_conf_file'])
    putFileToServer(local_intacsvr_conf_file1, old_intacsvr_conf_file, config.old_intacsvr['hostname'],
                    config.old_intacsvr['username'], config.old_intacsvr['password'])
    print "上传更改后的intacsvr配置文件至服务器完成"


#更换前置服务etfsvr
def etfsvr():
    new_etfsvr_add = config.new_etfsvr['new_etfsvr_address'] + config.new_etfsvr['new_etfsvr_file']
    local_add_file = '%setfsvr%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_etfsvr['new_etfsvr_file'] = 'etfsvr%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_etfsvr_add, local_add_file, config.new_etfsvr['hostname'], config.new_etfsvr['username'],
                   config.new_etfsvr['password'])
    print "最新版etfsvr压缩包下载本地完成！"

    old_etfsvr_add = '%setfsvr%s.tar.gz' % (
    config.old_etfsvr['old_etfsvr_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_etfsvr_add, config.old_etfsvr['hostname'], config.old_etfsvr['username'],
                    config.old_etfsvr['password'])
    print "将新版本etfsvr压缩包上传至etfsvr服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_etfsvr['old_etfsvr_address'], 'etfsvr', config.old_etfsvr['hostname'],
               config.old_etfsvr['username'], config.old_etfsvr['password'])
    print "etfsvr旧版本文件重命名完成！"

    tarFile(config.old_etfsvr['old_etfsvr_address'], config.old_etfsvr['new_etfsvr_file'],
            config.old_etfsvr['hostname'], config.old_etfsvr['username'], config.old_etfsvr['password'])
    print '解压 etfsvr{date}.tar.gz 完成！'

    delFile(old_etfsvr_add, config.old_etfsvr['hostname'], config.old_etfsvr['username'],
            config.old_etfsvr['password'])
    print "删除 etfsvr{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_etfsvr['old_etfsvr_conf_add'] + config.old_etfsvr['etfsvr_conf_file']
    local_etfsvr_conf_file = '%s%s' % (config.local_svr['local_address'], config.old_etfsvr['etfsvr_conf_file'])
    getFileToLocal(new_cfg, local_etfsvr_conf_file, config.old_etfsvr['hostname'],
                   config.old_etfsvr['username'], config.old_etfsvr['password'])
    print "下载etfsvr需要更改的配置文件完成！"

    local_etfsvr_conf_file1 = '%s%s1' % (config.local_svr['local_address'], config.old_etfsvr['etfsvr_conf_file'])
    change_etf_etfsvr(local_etfsvr_conf_file, local_etfsvr_conf_file1)
    print "更改etfsvr配置文件完成！"

    # 上传到服务器上的文件
    old_etfsvr_conf_file = '%s%s' % (config.old_etfsvr['old_etfsvr_conf_add'], config.old_etfsvr['etfsvr_conf_file'])

    # 删除服务器上的原文件
    delFile(old_etfsvr_conf_file, config.old_etfsvr['hostname'], config.old_etfsvr['username'],
            config.old_etfsvr['password'])
    print "删除原etfsvr配置文件完成！"

    # 上传到服务器上的文件
    old_etfsvr_conf_file = '%s%s' % (config.old_etfsvr['old_etfsvr_conf_add'], config.old_etfsvr['etfsvr_conf_file'])
    putFileToServer(local_etfsvr_conf_file1, old_etfsvr_conf_file, config.old_etfsvr['hostname'],
                    config.old_etfsvr['username'], config.old_etfsvr['password'])
    print "上传更改后的etfsvr配置文件至服务器完成"


#更换前置服务acsvr_acct
def acsvr_acct():
    new_acsvr_acct_add = config.new_acsvr_acct['new_acsvr_acct_address'] + config.new_acsvr_acct['new_acsvr_acct_file']
    local_add_file = '%sacsvr_acct%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvr_acct['new_acsvr_acct_file'] = 'acsvr_acct%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvr_acct_add, local_add_file, config.new_acsvr_acct['hostname'],
                   config.new_acsvr_acct['username'], config.new_acsvr_acct['password'])
    print "最新版acsvr_acct压缩包下载本地完成！"

    old_acsvr_acct_add = '%sacsvr_acct%s.tar.gz' % (
    config.old_acsvr_acct['old_acsvr_acct_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvr_acct_add, config.old_acsvr_acct['hostname'],
                    config.old_acsvr_acct['username'], config.old_acsvr_acct['password'])
    print "将新版本acsvr_acct压缩包上传至acsvr_acct服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvr_acct['old_acsvr_acct_address'], 'acsvr_acct', config.old_acsvr_acct['hostname'],
               config.old_acsvr_acct['username'], config.old_acsvr_acct['password'])
    print "acsvr_acct旧版本文件重命名完成！"

    tarFile(config.old_acsvr_acct['old_acsvr_acct_address'], config.old_acsvr_acct['new_acsvr_acct_file'],
            config.old_acsvr_acct['hostname'], config.old_acsvr_acct['username'], config.old_acsvr_acct['password'])
    print '解压 acsvr_acct{date}.tar.gz 完成！'

    delFile(old_acsvr_acct_add, config.old_acsvr_acct['hostname'], config.old_acsvr_acct['username'],
            config.old_acsvr_acct['password'])
    print "删除 acsvr_acct{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_acsvr_acct['old_acsvr_acct_conf_add'] + config.old_acsvr_acct['acsvr_acct_conf_file']
    local_acsvr_acct_conf_file = '%s%s' % (
    config.local_svr['local_address'], config.old_acsvr_acct['acsvr_acct_conf_file'])
    getFileToLocal(new_cfg, local_acsvr_acct_conf_file,
                   config.old_acsvr_acct['hostname'], config.old_acsvr_acct['username'],
                   config.old_acsvr_acct['password'])
    print "下载acsvr_acct需要更改的配置文件完成！"

    local_acsvr_acct_conf_file1 = '%s%s1' % (
    config.local_svr['local_address'], config.old_acsvr_acct['acsvr_acct_conf_file'])
    change_reg_acct(local_acsvr_acct_conf_file, local_acsvr_acct_conf_file1)
    print "更改acsvr_acct配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_acct_conf_file = '%s%s' % (
    config.old_acsvr_acct['old_acsvr_acct_conf_add'], config.old_acsvr_acct['acsvr_acct_conf_file'])

    # 删除服务器上的原文件
    delFile(old_acsvr_acct_conf_file, config.old_acsvr_acct['hostname'], config.old_acsvr_acct['username'],
            config.old_acsvr_acct['password'])
    print "删除原acsvr_acct配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_acct_conf_file = '%s%s' % (
    config.old_acsvr_acct['old_acsvr_acct_conf_add'], config.old_acsvr_acct['acsvr_acct_conf_file'])
    putFileToServer(local_acsvr_acct_conf_file1, old_acsvr_acct_conf_file, config.old_acsvr_acct['hostname'],
                    config.old_acsvr_acct['username'], config.old_acsvr_acct['password'])
    print "上传更改后的acsvr_acct配置文件至服务器完成"


#更换前置服务acsvr_bank
def acsvr_bank():
    new_acsvr_bank_add = config.new_acsvr_bank['new_acsvr_bank_address'] + config.new_acsvr_bank['new_acsvr_bank_file']
    local_add_file = '%sacsvr_bank%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvr_bank['new_acsvr_bank_file'] = 'acsvr_bank%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvr_bank_add, local_add_file, config.new_acsvr_bank['hostname'],
                   config.new_acsvr_bank['username'], config.new_acsvr_bank['password'])
    print "最新版acsvr_bank压缩包下载本地完成！"

    old_acsvr_bank_add = '%sacsvr_bank%s.tar.gz' % (
    config.old_acsvr_bank['old_acsvr_bank_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvr_bank_add, config.old_acsvr_bank['hostname'],
                    config.old_acsvr_bank['username'], config.old_acsvr_bank['password'])
    print "将新版本acsvr_bank压缩包上传至acsvr_bank服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvr_bank['old_acsvr_bank_address'], 'acsvr_bank', config.old_acsvr_bank['hostname'],
               config.old_acsvr_bank['username'], config.old_acsvr_bank['password'])
    print "acsvr_bank旧版本文件重命名完成！"

    tarFile(config.old_acsvr_bank['old_acsvr_bank_address'], config.old_acsvr_bank['new_acsvr_bank_file'],
            config.old_acsvr_bank['hostname'], config.old_acsvr_bank['username'], config.old_acsvr_bank['password'])
    print '解压 acsvr_bank{date}.tar.gz 完成！'

    delFile(old_acsvr_bank_add, config.old_acsvr_bank['hostname'], config.old_acsvr_bank['username'],
            config.old_acsvr_bank['password'])
    print "删除 acsvr_bank{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_acsvr_bank['old_acsvr_bank_conf_add'] + config.old_acsvr_bank['acsvr_bank_conf_file']
    local_acsvr_bank_conf_file = '%s%s' % (
    config.local_svr['local_address'], config.old_acsvr_bank['acsvr_bank_conf_file'])
    getFileToLocal(new_cfg, local_acsvr_bank_conf_file,
                   config.old_acsvr_bank['hostname'], config.old_acsvr_bank['username'],
                   config.old_acsvr_bank['password'])
    print "下载acsvr_bank需要更改的配置文件完成！"

    local_acsvr_bank_conf_file1 = '%s%s1' % (
    config.local_svr['local_address'], config.old_acsvr_bank['acsvr_bank_conf_file'])
    change_reg_bank(local_acsvr_bank_conf_file, local_acsvr_bank_conf_file1)
    print "更改acsvr_bank配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_bank_conf_file = '%s%s' % (
    config.old_acsvr_bank['old_acsvr_bank_conf_add'], config.old_acsvr_bank['acsvr_bank_conf_file'])

    # 删除服务器上的原文件
    delFile(old_acsvr_bank_conf_file, config.old_acsvr_bank['hostname'], config.old_acsvr_bank['username'],
            config.old_acsvr_bank['password'])
    print "删除原acsvr_bank配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_bank_conf_file = '%s%s' % (
    config.old_acsvr_bank['old_acsvr_bank_conf_add'], config.old_acsvr_bank['acsvr_bank_conf_file'])
    putFileToServer(local_acsvr_bank_conf_file1, old_acsvr_bank_conf_file, config.old_acsvr_bank['hostname'],
                    config.old_acsvr_bank['username'], config.old_acsvr_bank['password'])
    print "上传更改后的acsvr_bank配置文件至服务器完成"


#更换前置服务acsvr_wm
def acsvr_wm():
    new_acsvr_wm_add = config.new_acsvr_wm['new_acsvr_wm_address'] + config.new_acsvr_wm['new_acsvr_wm_file']
    local_add_file = '%sacsvr_wm%s.tar.gz' % (
    config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvr_wm['new_acsvr_wm_file'] = 'acsvr_wm%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvr_wm_add, local_add_file, config.new_acsvr_wm['hostname'], config.new_acsvr_wm['username'],
                   config.new_acsvr_wm['password'])
    print "最新版acsvr_wm压缩包下载本地完成！"

    old_acsvr_wm_add = '%sacsvr_wm%s.tar.gz' % (
    config.old_acsvr_wm['old_acsvr_wm_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvr_wm_add, config.old_acsvr_wm['hostname'], config.old_acsvr_wm['username'],
                    config.old_acsvr_wm['password'])
    print "将新版本acsvr_wm压缩包上传至acsvr_wm服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvr_wm['old_acsvr_wm_address'], 'acsvr_wm', config.old_acsvr_wm['hostname'],
               config.old_acsvr_wm['username'], config.old_acsvr_wm['password'])
    print "acsvr_wm旧版本文件重命名完成！"

    tarFile(config.old_acsvr_wm['old_acsvr_wm_address'], config.old_acsvr_wm['new_acsvr_wm_file'],
            config.old_acsvr_wm['hostname'], config.old_acsvr_wm['username'], config.old_acsvr_wm['password'])
    print '解压 acsvr_wm{date}.tar.gz 完成！'

    delFile(old_acsvr_wm_add, config.old_acsvr_wm['hostname'], config.old_acsvr_wm['username'],
            config.old_acsvr_wm['password'])
    print "删除 acsvr_wm{date}.tar.gz 压缩包完成！"

    new_cfg = config.old_acsvr_wm['old_acsvr_wm_conf_add'] + config.old_acsvr_wm['acsvr_wm_conf_file']
    local_acsvr_wm_conf_file = '%s%s' % (config.local_svr['local_address'], config.old_acsvr_wm['acsvr_wm_conf_file'])
    getFileToLocal(new_cfg, local_acsvr_wm_conf_file, config.old_acsvr_wm['hostname'],
                   config.old_acsvr_wm['username'], config.old_acsvr_wm['password'])
    print "下载acsvr_wm需要更改的配置文件完成！"

    local_acsvr_wm_conf_file1 = '%s%s1' % (config.local_svr['local_address'], config.old_acsvr_wm['acsvr_wm_conf_file'])
    change_reg_wm(local_acsvr_wm_conf_file, local_acsvr_wm_conf_file1)
    print "更改acsvr_wm配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_wm_conf_file = '%s%s' % (
    config.old_acsvr_wm['old_acsvr_wm_conf_add'], config.old_acsvr_wm['acsvr_wm_conf_file'])

    # 删除服务器上的原文件
    delFile(old_acsvr_wm_conf_file, config.old_acsvr_wm['hostname'], config.old_acsvr_wm['username'],
            config.old_acsvr_wm['password'])
    print "删除原acsvr_wm配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_wm_conf_file = '%s%s' % (
    config.old_acsvr_wm['old_acsvr_wm_conf_add'], config.old_acsvr_wm['acsvr_wm_conf_file'])
    putFileToServer(local_acsvr_wm_conf_file1, old_acsvr_wm_conf_file, config.old_acsvr_wm['hostname'],
                    config.old_acsvr_wm['username'], config.old_acsvr_wm['password'])
    print "上传更改后的acsvr_wm配置文件至服务器完成"


def main():
    flag = True
    while flag:
        print "\n根据下面提示输入指令:\n"
        com = raw_input(" 1) 更改交易前置acsvrA             2) 更改交易前置quotaacsvr \n"
                        " 3) 更改交易前置intacsvr           4) 更改etf前置etfsvr \n"
                        " 5) 更改登记前置acsvr_acct         6) 更改登记前置acsvr_bank \n"
                        " 7) 更改登记前置acsvr_wm           8) 更改交易前置acsvrB "
                        "9) 退出 \n"
                        " 请输入指令：")
        if com == '99':
            continue
        elif com == '1':
            print "更改交易前置acsvr"
            config.new_acsvrA['new_acsvrA_address'] = raw_input("输入最新版acsvrA地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_acsvrA['new_acsvrA_file'] = raw_input("输入最新acsvrA核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvrA()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 acsvrA 操作-----------------"
        elif com == '2':
            print "更改交易前置quotaacsvr"
            config.new_quotaacsvr['new_quotaacsvr_address'] = raw_input("输入最新版quotaacsvr地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_quotaacsvr['new_quotaacsvr_file'] = raw_input("输入最新quotaacsvr核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            quotaacsvr()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 quotaacsvr 操作-----------------"
        elif com == '3':
            print "更改交易前置intacsvr"
            config.new_intacsvr['new_intacsvr_address'] = raw_input("输入最新版intacsvr地址 ，(如 /home/zhiban/guoqing/20180822/wh/   (最后要加'/')):")
            config.new_intacsvr['new_intacsvr_file'] = raw_input("输入最新intacsvr核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            intacsvr()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 intacsvr 操作-----------------"
        elif com == '4':
            print "更改交易前置etfsvr"
            config.new_etfsvr['new_etfsvr_address'] = raw_input("输入最新版etfsvr地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_etfsvr['new_etfsvr_file'] = raw_input("输入最新etfsvr核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            etfsvr()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 etfsvr 操作-----------------"
        elif com == '5':
            print "更改交易前置acsvr_acct"
            config.new_acsvr_acct['new_acsvr_acct_address'] = raw_input("输入最新版acsvr_acct地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_acsvr_acct['new_acsvr_acct_file'] = raw_input("输入最新acsvr_acct核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvr_acct()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 acsvr_acct 操作-----------------"
        elif com == '6':
            print "更改交易前置acsvr_bank"
            config.new_acsvr_bank['new_acsvr_bank_address'] = raw_input("输入最新版acsvr_bank地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_acsvr_bank['new_acsvr_bank_file'] = raw_input("输入最新acsvr_bank核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvr_bank()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 acsvr_bank 操作-----------------"
        elif com == '7':
            print "更改交易前置acsvr_wm"
            config.new_acsvr_wm['new_acsvr_wm_address'] = raw_input("输入最新版acsvr_wm地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_acsvr_wm['new_acsvr_wm_file'] = raw_input("输入最新acsvr_wm核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvr_wm()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 acsvr_wm 操作-----------------"
        elif com == '8':
            print "更改交易前置acsvrB"
            config.new_acsvrB['new_acsvrB_address'] = raw_input("输入最新版acsvrB地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
            config.new_acsvrB['new_acsvrB_file'] = raw_input("输入最新acsvrB核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvrB()
            print "删除 %s" % (config.local_svr['local_address'],)
            shutil.rmtree(config.local_svr['local_address'])
            print "已删除 %s 目录" % (config.local_svr['local_address'],)
            print "---------------完成 更换更改交易前置 acsvrB 操作-----------------"
        elif com == '9':
            flag = False
        else:
            print "没有该命令，请重新输入:"


if __name__ == '__main__':
    # data_list = get_all_data('liantiao-0824.xls')  # 全部源数据
    # mkdir(config.local_svr['local_address'])
    main()
    # print "删除 %s" % (config.local_svr['local_address'],)
    # shutil.rmtree(config.local_svr['local_address'])
    # print "已删除 %s 目录" % (config.local_svr['local_address'],)