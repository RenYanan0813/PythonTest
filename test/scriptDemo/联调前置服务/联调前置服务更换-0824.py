# -*- coding:utf-8 -*-

import paramiko
import re
import xlrd
import config
import datetime
import os

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

# 通用，重命名文件
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

#更换前置服务acsvr
def acsvr():
    new_acsvr_add = config.new_acsvr['new_acsvr_address'] + config.new_acsvr['new_acsvr_file']
    local_add_file = '%sacsvr%s.tar.gz' % (config.local_svr['local_address'], datetime.datetime.now().strftime('%Y%m%d'))
    config.old_acsvr['new_acsvr_file'] = 'acsvr%s.tar.gz' % (datetime.datetime.now().strftime('%Y%m%d'),)

    getFileToLocal(new_acsvr_add, local_add_file, config.new_acsvr['hostname'], config.new_acsvr['username'], config.new_acsvr['password'])
    print "最新版acsvr压缩包下载本地完成！"

    old_acsvr_add = '%sacsvr%s.tar.gz' % (config.old_acsvr['old_acsvr_address'], datetime.datetime.now().strftime('%Y%m%d'))
    putFileToServer(local_add_file, old_acsvr_add, config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print "将新版本acsvr压缩包上传至acsvr服务器完成！"

    # 将原来的文件重命名备份
    renameFile(config.old_acsvr['old_acsvr_address'], 'acsvr', config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print "acsvr旧版本文件重命名完成！"

    tarFile(config.old_acsvr['old_acsvr_address'], config.old_acsvr['new_acsvr_file'], config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print '解压 acsvr{date}.tar.gz 完成！'

    local_acsvr_conf_file =  '%s%s'%(config.local_svr['local_address'], config.old_acsvr['acsvr_conf_file'])
    getFileToLocal(config.old_acsvr['acsvr_conf_file'], local_acsvr_conf_file ,config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print "下载acsvr需要更改的配置文件完成！"

    local_acsvr_conf_file1 = '%s%s1'%(config.local_svr['local_address'], config.old_acsvr['acsvr_conf_file'])
    change_tra_acsvr(local_acsvr_conf_file, local_acsvr_conf_file1)
    print "更改acsvr配置文件完成！"

    # 上传到服务器上的文件
    old_acsvr_conf_file = '%s%s' % (config.old_acsvr['old_acsvr_conf_add'], config.old_acsvr['acsvr_conf_file'])

    #删除服务器上的原文件
    delFile(old_acsvr_conf_file, config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print "删除原acsvr配置文件完成！"

    #上传到服务器上的文件
    old_acsvr_conf_file = '%s%s'%(config.old_acsvr['old_acsvr_conf_add'], config.old_acsvr['acsvr_conf_file'])
    putFileToServer(local_acsvr_conf_file1, old_acsvr_conf_file, config.old_acsvr['hostname'], config.old_acsvr['username'], config.old_acsvr['password'])
    print "上传更改后的acsvr配置文件至服务器完成"


#更换前置服务quotaacsvr
def quotaacsvr():
    pass

def main():
    flag = True
    while flag:
        print "\n根据下面提示输入指令:\n"
        com = raw_input(" 1) 更改交易前置acsvr        2) 更改交易前置quotaacsvr \n"
                        " 3) 更改交易前置intacsvr     4) 更改etf前置etfsvr \n"
                        " 5) 更改登记前置acct         6) 更改登记前置bank \n"
                        " 7) 更改登记前置wm           8) 退出 \n"
                        " 请输入指令：")
        if com == '99':
            continue
        elif com == '1':
            print "更改交易前置acsvr"
            config.new_acsvr['new_acsvr_address'] = raw_input("输入最新版acsvr地址 ，(如 /home/zhiban/guoqing/20180822/wh/):")
            config.new_acsvr['new_acsvr_file'] = raw_input("输入最新acsvr核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            acsvr()
            print "---------------完成 更换更改交易前置 acsvr 操作-----------------"
        elif com == '2':
            print "更改交易前置quotaacsvr"
            quotaacsvr_config = raw_input("输入最新版quotaacsvr地址 ，(如 /home/zhiban/guoqing/20180822/wh/):")
            quotaacsvr_file = raw_input("输入最新quotaacsvr核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            quotaacsvr()
            print "---------------完成 更换更改交易前置 quotaacsvr 操作-----------------"
        elif com == '8':
            flag = False
        else:
            print "没有该命令，请重新输入:"


if __name__ == '__main__':
    # data_list = get_all_data('liantiao-0824.xls')  # 全部源数据
    mkdir(config.local_svr['local_address'])
    main()
    print "删除 %s" % (config.local_svr['local_address'],)
    os.removedirs(config.local_svr['local_address'])
    print "已删除 %s 目录" % (config.local_svr['local_address'],)