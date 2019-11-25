# -*- coding:utf-8 -*-
"""
    author: rony
"""

import os
import config
import shutil
import paramiko
from datetime import datetime
import datetime


#创建本地公用文件夹
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        # return TrueF
    else:
        print(path + ' 目录已存在')
        # return False

#验证文件是否存在
def modify_file_exist(file_mame):
    file_mame1 = "%s%s"%(config.common_local_path["local_address"], file_mame)
    isExist = os.path.isfile(file_mame1)
    return isExist

#下载新版到本地
def pull_new_version_to_local():
    t = paramiko.Transport((config.version_svr["hostname"], 22))
    t.connect(username=config.version_svr["username"], password=config.version_svr["password"])
    sftp = paramiko.SFTPClient.from_transport(t)
    if config.version_svr["new_version_path"] == "" or config.version_svr["new_version_file"] == "":
        print("新版本地址出错，请重新检查....")
    else:
        try:
            new_ver_com = "%s/%s"%(config.version_svr["new_version_path"], config.version_svr["new_version_file"])
            local_ver_com = "%s%s"%(config.common_local_path["local_address"], 'install.tar.gz')
            sftp.get(new_ver_com, local_ver_com)
            print("新版下载成功，存储在 %s 路径下, 名称为 %s"%(config.common_local_path["local_address"], config.version_svr["new_version_file"]))
        except:
            print("下载新版本到本地出错，请检查新版本地址及本地路径是否有误！")
        finally:
            sftp.close()
            t.close()


#上传新版本到服务器,
def push_new_ver_2_svr(svr_info):
    svr_num = len(svr_info)
    print("共有.... %d 台 .... 服务器，需要上传！"%(svr_num, ))
    for i in range(svr_num):
        t = paramiko.Transport((svr_info[i]["hostname"], 22))
        t.connect(username=svr_info[i]["username"], password=svr_info[i]["password"])
        sftp = paramiko.SFTPClient.from_transport(t)
        try:
            local_ver_com = "%s%s" % (config.common_local_path["local_address"], 'install.tar.gz')
            remote_svr_com = "%s%s" % (svr_info[i]["server_path"], 'install.tar.gz')
            sftp.put(local_ver_com, remote_svr_com)
        except:
            print("上传有错误，请检查！")
        finally:
            sftp.close()
            t.close()


##备份旧服务
def mv_old_file(old_file_info):
    old_svr_num = len(old_file_info)
    old_qte_svr_num = len(old_file_info[0]["svr_cfgs"])
    print("共有 %d 台服务器的 %d 个服务备份..."%(old_svr_num, old_qte_svr_num))
    for svr_num in range(old_svr_num):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=old_file_info[svr_num]["hostname"], username=old_file_info[svr_num]["username"], password=old_file_info[svr_num]["password"])
        try:
            for qte_svr_num in range(old_qte_svr_num):
                date = datetime.datetime.now().strftime('%Y%m%d_%S')
                old_file_date = old_file_info[svr_num]["svr_cfgs"][qte_svr_num] + date
                mv_com = 'cd %s; mv %s %s' % (old_file_info[svr_num]["server_path"], old_file_info[svr_num]["svr_cfgs"][qte_svr_num], old_file_date)
                stdin, stdout, stderr = ssh.exec_command(mv_com)
                stdin1, stdout1, stderr1 = ssh.exec_command('cd %s; ll'%(old_file_info[svr_num]["server_path"], ))
                if old_file_date in stdout1:
                    print("备份 %s 服务器上的 %s 服务完成!"%(old_file_info[svr_num]["hostname"], old_file_info[svr_num]["svr_cfgs"][qte_svr_num]))
                else:
                    print("备份 %s 原文件出错，请手动检查....."%(old_file_info[svr_num]["svr_cfgs"][qte_svr_num]))
        except Exception as e:
            print("ssh连接有问题，备份原文件失败!")
        finally:
            ssh.close()

#更改服务文件夹名称
def mv_svrs_name(svr_info):
    svr_num = len(svr_info[0]["svr_cfgs"])
    app_svr_num = len(svr_info[0]["svr_cfgs"])
    print("共有 %d 台服务器的 %d 个服务更改名称..." % (svr_num, app_svr_num))
    for svr_num in range(svr_num):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=svr_info[svr_num]["hostname"], username=svr_info[svr_num]["username"], password=svr_info[svr_num]["password"])
        try:
            for qte_svr_num in range(app_svr_num):
                app_file_flag = "%s%s"%(svr_info[svr_num]["svr_cfgs"][qte_svr_num], svr_info[svr_num]["flag"])
                mv_com = 'cd %s; mv %s %s' % (svr_info[svr_num]["server_path"], svr_info[svr_num]["svr_cfgs"][qte_svr_num], app_file_flag)
                stdin, stdout, stderr = ssh.exec_command(mv_com)
                stdin1, stdout1, stderr1 = ssh.exec_command('cd %s; ll'%(svr_info[svr_num]["server_path"], ))
                if app_file_flag in stdout1:
                    print("flag命名 %s 服务器上的 %s 服务完成!"%(svr_info[svr_num]["hostname"], svr_info[svr_num]["svr_cfgs"][qte_svr_num]))
                else:
                    print("flag命名 %s 原文件出错，请手动检查....."%(svr_info[svr_num]["svr_cfgs"][qte_svr_num]))
        except Exception as e:
            print("ssh连接有问题，flag命名原文件失败!")
        finally:
            ssh.close()

#解压新版本
def tar_xf_new_version(file_info):
    old_svr_num = len(file_info)
    print("共有 %d 台服务器需要解压..." % (old_svr_num, ))
    for svr_num in range(old_svr_num):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=file_info[svr_num]["hostname"], username=file_info[svr_num]["username"], password=file_info[svr_num]["password"])
        try:
            tar_com = 'cd ~; tar -xf install.tar.gz'
            stdin, stdout, stderr = ssh.exec_command(tar_com)
            if stdout != "":
                print("解压 %s 服务器上的 install.tar.gz 完成!"%(file_info[svr_num]["hostname"]))
        except Exception as e:
            print("解压 %s 服务器上的 install.tar.gz 失败........." % (file_info[svr_num]["hostname"]))
        finally:
            ssh.close()

#下载需要更改配置的文件
def pull_all_cfg_to_local():
    svr_cfgs = ['qte_acsvr.cfg', 'guomi_safe.cfg', 'version.cfg', 'qte_quotaacsvr.cfg', 'qte_qy_acsvr.cfg']
    t = paramiko.Transport((config.qte_acsvr[0]["hostname"], 22))
    t.connect(username=config.qte_acsvr[0]["username"], password=config.qte_acsvr[0]["password"])
    sftp = paramiko.SFTPClient.from_transport(t)

    try:
        for i in range(len(svr_cfgs)):
            if i < 3:
                    cfg_file = "%s%s%s"%(config.qte_acsvr[0]["server_path"], 'qte_acsvr', svr_cfgs[i])
                    save_path = "%s%s"%(config.common_local_path["local_address"], svr_cfgs[i])
                    sftp.get(cfg_file, save_path)
            if 'qte_quotaacsvr' in svr_cfgs[i]:
                cfg_file = "%s%s%s" % (config.qte_acsvr[0]["server_path"], 'qte_quotaacsvr', svr_cfgs[i])
                save_path = "%s%s" % (config.common_local_path["local_address"], svr_cfgs[i])
                sftp.get(cfg_file, save_path)
            if 'qte_qy_acsvr' in svr_cfgs[i]:
                cfg_file = "%s%s%s" % (config.qte_acsvr[0]["server_path"], 'qte_qy_acsvr', svr_cfgs[i])
                save_path = "%s%s" % (config.common_local_path["local_address"], svr_cfgs[i])
                sftp.get(cfg_file, save_path)
        for i in range(len(svr_cfgs)):
            if modify_file_exist(svr_cfgs[i]) == True:
                print('下载 %s 完成[=========================] 100%  ', "文件上传至:%s" % (svr_cfgs[i], save_path))
            else:
                print('下载 %s 失败 ........ 0% , 请检查配置！ ' % (svr_cfgs[i], ))
    except:
        print('服务器未找到该 cfg 文件! ')
    finally:
        t.close()
        sftp.close()

#删除qte的cfg文件
def rm_qte_cfgs():
    for svr_num in range(len(config.qte_acsvr)):
        rm_ac_cfgs = "%s%s" % (config.qte_acsvr[svr_num]["server_path"], 'qte_acsvr/conf/')
        rm_quo_cfgs = "%s%s" % (config.qte_acsvr[svr_num]["server_path"], 'qte_quotaacsvr/conf/')
        rm_qy_cfgs = "%s%s" % (config.qte_acsvr[svr_num]["server_path"], 'qte_qy_acsvr/conf/')

        # 删除要替换的cfg文件
        for i in ['qte_acsvr.cfg', 'guomi_safe.cfg', 'version.cfg']:
            rm_ac = "%s%s" % (rm_ac_cfgs, i)
            delFile(rm_ac, config.qte_acsvr[svr_num]["hostname"], config.qte_acsvr[svr_num]["username"],
                    config.qte_acsvr[svr_num]["password"])
        for i in ['qte_quotaacsvr.cfg', 'version.cfg']:
            rm_quo = "%s%s" % (rm_quo_cfgs, i)
            delFile(rm_quo, config.qte_acsvr[svr_num]["hostname"], config.qte_acsvr[svr_num]["username"],
                    config.qte_acsvr[svr_num]["password"])
        for i in ['qte_qy_acsvr.cfg', 'guomi_safe.cfg', 'version.cfg']:
            rm_qy = "%s%s" % (rm_qy_cfgs, i)
            delFile(rm_qy, config.qte_acsvr[svr_num]["hostname"], config.qte_acsvr[svr_num]["username"],
                    config.qte_acsvr[svr_num]["password"])


#上传 cfg 文件 到服务器
def push_qte_cfg_to_svr(qte_info):
    common_cfgs = ['guomi_safe.cfg', 'version.cfg']
    qte_num = len(qte_info)
    print("共有 %d 台服务器需要上传..." % (qte_num,))
    for svr_num in range(qte_num):
        if config.qte_acsvr[svr_num]["flag"] == "A":
            t = paramiko.Transport((qte_info[svr_num]["hostname"], 22))
            t.connect(username=qte_info[svr_num]["username"], password=qte_info[svr_num]["password"])
            sftp = paramiko.SFTPClient.from_transport(t)
            try:
                for i in range(len(qte_info[svr_num]["svr_cfgs"])):
                    if 'qte_acsvr' in qte_info[svr_num]["svr_cfgs"]:
                        local_ac_com = "%s%s-%s.cfg" % (qte_info[svr_num]["local_address"], 'qte_acsvr', qte_info[svr_num]["flag"])
                        ac_cfgs_com = "%s%s/conf/%s-%s.cfg" % (qte_info[svr_num]["server_path"], 'qte_acsvr', 'qte_acsvr', qte_info[svr_num]["flag"])
                        sftp.put(local_ac_com, ac_cfgs_com)
                        for com_num in range(len(common_cfgs)):
                            local_comm_com = "%s%s" % (qte_info[svr_num]["local_address"], common_cfgs[i])
                            comm_cfgs_com = "%s%s/conf/%s" % (
                            qte_info[svr_num]["server_path"], 'qte_acsvr', common_cfgs[i])
                            sftp.put(local_comm_com, comm_cfgs_com)
                    if 'qte_quotaacsvr' in qte_info[svr_num]["svr_cfgs"]:
                        local_ac_com = "%s%s-%s.cfg" % (qte_info[svr_num]["local_address"], 'qte_quotaacsvr', qte_info[svr_num]["flag"])
                        ac_cfgs_com = "%s%s/conf/%s-%s.cfg" % (qte_info[svr_num]["server_path"], 'qte_quotaacsvr', 'qte_quotaacsvr', qte_info[svr_num]["flag"])
                        sftp.put(local_ac_com, ac_cfgs_com)
                        for com_num in range(len(common_cfgs)):
                            if 'version' in common_cfgs:
                                local_comm_com = "%s%s" % (qte_info[svr_num]["local_address"], common_cfgs[i])
                                comm_cfgs_com = "%s%s/conf/%s" % (
                                    qte_info[svr_num]["server_path"], 'qte_quotaacsvr', common_cfgs[i])
                                sftp.put(local_comm_com, comm_cfgs_com)
                    if 'qte_qy_acsvr' in qte_info[svr_num]["svr_cfgs"]:
                        local_ac_com = "%s%s-%s.cfg" % (qte_info[svr_num]["local_address"], 'qte_qy_acsvr', qte_info[svr_num]["flag"])
                        ac_cfgs_com = "%s%s/conf/%s-%s.cfg" % (
                        qte_info[svr_num]["server_path"], 'qte_qy_acsvr', 'qte_qy_acsvr', qte_info[svr_num]["flag"])
                        sftp.put(local_ac_com, ac_cfgs_com)
                        for com_num in range(len(common_cfgs)):
                            local_comm_com = "%s%s" % (qte_info[svr_num]["local_address"], common_cfgs[i])
                            comm_cfgs_com = "%s%s/conf/%s" % (
                            qte_info[svr_num]["server_path"], 'qte_qy_acsvr', common_cfgs[i])
                            sftp.put(local_comm_com, comm_cfgs_com)
                    print("----------- %s ---- 服务器上传---- cfg ----文件 完成！" % (qte_info[svr_num]["hostname"]))
            except:
                pass
            finally:
                t.close()
                sftp.close()


# 删除文件
def delFile(tarTxt, svr_add, username, psd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=svr_add, username=username, password=psd)
    com = 'rm -r %s' % (tarTxt)
    try:
        stdin, stdout, stderr = ssh.exec_command(com)
        print("删除 %s 服务器上的 %s ----------------------- 完成!"%(svr_add, tarTxt.split('/')[-1]))
    except Exception as e:
        print("删除 %s 服务器上的 %s xxxxxxxxxxxxxxxxxxxxxxx 失败!" % (svr_add, tarTxt.split('/')[-1]))
    finally:
        ssh.close()

def change_qte_svrs(qte_svr_info):
    if qte_svr_info == None or qte_svr_info == "":
        qte_svr = ['qte_acsvr.cfg', 'qte_quotaacsvr.cfg', 'qte_qy_acsvr.cfg']
    else:
        qte_svr = qte_svr_info
    try:
        for svr_num in range(len(qte_svr)):
            if "qte_acsvr" in qte_svr[svr_num]:
                with open('%s%s'%(config.common_local_path["local_address"], qte_svr[svr_num]), 'r+') as fp1:
                    lenght = fp1.readlines()
                    print("正在读取 qte_acsvr.cfg 原数据...")
                    for num in range(0, 1):
                        if config.qte_acsvr[num]["flag"] == "A":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_acsvr-A.cfg'), 'a') as qte_ac_a:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_acsvrA')
                                        # fp2.write(s)
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    # if '"listen_ports":{' in lenght[i]:
                                    #     # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                                    #     # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                                    #     lenght[i + 1] = ''
                                    #     lenght[i + 2] = ''
                                    #     lenght[i + 1] = '                   7776:1,\n'
                                    #     lenght[i + 2] = '                   16998:2\n'
                                    #     # fp2.write(s)
                                    #     print("更改 listen_ports 成功 %s"%(lenght[i]))
                                    # if '"listen_port"' in lenght[i]:
                                    #     # lenght[i] = re.sub(r'server_port = (\w+)', "server_port = 7777", lenght[i])
                                    #     # s = lenght[i].replace(r'server_port = (\w+)', 'server_port = 7777')
                                    #     lenght[i] = ''
                                    #     lenght[i] = '        "listen_port" : 9312,\n'
                                    #     # fp2.write(s)
                                    #     print("更改 listen_port 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                                        # fp2.write(str(s1))
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        # lenght[i] = re.sub(r'server_ip = (\'\w+\.\w+\.\w+\.\w+\')', "server_ip = '180.2.32.20'", lenght[i])
                                        # fp2.write(str(s1))
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 801,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_ac_a.write(lenght[i])
                        if config.qte_acsvr[num]["flag"] == "B":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_acsvr-B.cfg'), 'a') as qte_ac_b:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_acsvrB')
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 802,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_ac_b.write(lenght[i])
                print('qte_acsvr 配置文件更改完成，存储在%s'%(config.common_local_path["local_address"]))
            if "qte_quotaacsvr" in qte_svr[svr_num]:
                with open('%s%s'%(config.common_local_path["local_address"], qte_svr[svr_num]), 'r+') as fp2:
                    lenght = fp2.readlines()
                    print("正在读取 qte_quotaacsvr.cfg 原数据...")
                    for num in range(0, 1):
                        if config.qte_acsvr[num]["flag"] == "A":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_quotaacsvr-A.cfg'), 'a') as qte_quo_a:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_quotaacsvrA')
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 1501,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_quo_a.write(lenght[i])
                        if config.qte_acsvr[num]["flag"] == "B":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_quotaacsvr-B.cfg'), 'a') as qte_quo_b:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_quotaacsvrB')
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 1502,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_quo_b.write(lenght[i])
                print('qte_quotaacsvr 配置文件更改完成，存储在%s'%(config.common_local_path["local_address"]))
            if "qte_qy_acsvr" in qte_svr[svr_num]:
                with open('%s%s'%(config.common_local_path["local_address"], qte_svr[svr_num]), 'r+') as fp3:
                    lenght = fp3.readlines()
                    print("正在读取 qte_qy_acsvr.cfg 原数据...")
                    for num in range(0, 1):
                        if config.qte_acsvr[num]["flag"] == "A":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_qy_acsvr-A.cfg'), 'a') as qte_qy_a:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_qy_acsvrA')
                                        # fp2.write(s)
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 1001,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_qy_a.write(lenght[i])
                        if config.qte_acsvr[num]["flag"] == "B":
                            for i in range(len(lenght)):
                                with open('%s%s'%(config.common_local_path["local_address"], 'qte_qy_acsvr-B.cfg'), 'a') as qte_qy_b:
                                    if '"name"' in lenght[i]:
                                        lenght[i] = ''
                                        lenght[i] = '        "name" : "/home/qte/log/%s",\n'%('qte_qy_acsvrB')
                                        print("更改 name 成功 %s"%(lenght[i]))
                                    if '"grp_cfg"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                                        print("更改 grp_cfg 成功 %s"%(lenght[i]))
                                    if '"dev"' in lenght[i]:
                                        lenght[i]=''
                                        lenght[i] = '        "dev" : 1002,\n'
                                        print("更改 dev 成功 %s"%(lenght[i]))
                                    qte_qy_b.write(lenght[i])
                print('qte_qy_acsvr 配置文件更改完成，存储在%s'%(config.common_local_path["local_address"]))
    except IOError as e:
        print("qte前置更改出错.....")
    finally:
        fp1.close()
        fp2.close()
        fp3.close()
        qte_ac_a.close()
        qte_ac_b.close()
        qte_quo_a.close()
        qte_quo_b.close()
        qte_qy_a.close()
        qte_qy_b.close()


def changeGuoMi(guomi_cfg):
    if guomi_cfg == None or guomi_cfg == "":
        guomi_cfg = "guomi_safe.cfg"
    try:
        with open('%s%s' % (config.common_local_path["local_address"], guomi_cfg), 'r+') as f_guomi:
            lines = f_guomi.readlines()
            for i in range(len(lines)):
                if '"ip"' in lines[i]:
                    lines[i] = '        "ip": "180.2.200.88"\n'
                if '"enc_mode"' in lines[i]:
                    lines[i] = '"enc_mode": 0, #0-hard enc, 1-soft enc, 2-no enc\n'
    except IOError as e:
        print("国密配置更改出错...")
    finally:
        f_guomi.close()


def changeVersion(version_cfg):
    if version_cfg == None or version_cfg == "":
        version_cfg = "version.cfg"
    try:
        with open('%s%s' % (config.common_local_path["local_address"], version_cfg), 'r+') as f_version:
            lines = f_version.readlines()
            for i in range(len(lines)):
                if '"1.3.0' in lines[i]:
                    lines[i] = '        "1.3.0": 1, \n "2.0.1": 1, \n'
    except IOError as e:
        print("版本信息更改出错...")
    finally:
        f_version.close()

def main():
    flag = True
    while flag:
        print("\n根据下面提示输入指令:\n")
        com = input(" 1) 更换 qte 前置 服务...  \n"
                    " 3) 更换 bpt 前置 服务... (为编写)\n"
                    " 88) 退出 \n"
                    " 请输入指令：")
        if com == '99':
            continue
        elif com == '1':
            print("更换 qte 前置 服务")
            print("请检查更换服务器上，是否遗留 install.tar.gz，有则手动移除....")
            if config.version_svr["new_version_path"] == "" or config.version_svr["new_version_file"] == "":
                config.version_svr["new_version_path"] = input("输入最新版 qte 前置地址 ，(如 /home/zhiban/guoqing/20180822/wh :")
                config.version_svr["new_version_file"] = input("输入最新 qte 前置 tar压缩包，(如 wh.tar.gz):")
            queren = input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                continue
            else:
                #检查并创建本地存储目录
                mkdir(config.common_local_path["local_address"])
                #下载新版本到本地
                pull_new_version_to_local()
                #删除服务器上旧的install.tar.gz
                # delFile('')
                #上传新版本tar包到服务器
                push_new_ver_2_svr(config.qte_acsvr)
                #备份旧服务
                mv_old_file(config.qte_acsvr)
                #在服务器上解压新版本tar包
                tar_xf_new_version(config.qte_acsvr)
                #下载 cfg 文件
                pull_all_cfg_to_local()
                #更改 cfg 文件
                change_qte_svrs(config.qte_acsvr[0]["svr_cfgs"])
                changeGuoMi()
                changeVersion()
                #删除 被修改的cfg
                rm_qte_cfgs()
                #上传cfg到服务器
                push_qte_cfg_to_svr(config.qte_acsvr)
                #更改服务文件夹名
                mv_svrs_name(config.qte_acsvr)

                print("删除 %s" % (config.common_local_path["local_address"],))
                shutil.rmtree(config.common_local_path["local_address"])
                print("已删除 %s 目录" % (config.common_local_path["local_address"],))
                print("------------------------------------ 完成 更换 qte 前置 ! ------------------------------------")
        elif com == '3':
            print("更换 qte 前置 qte_acsvrB")
            if config.version_svr["new_version_path"] == "" or config.version_svr["new_version_file"] == "":
                config.version_svr["new_version_path"] = input("输入最新版 qte_acsvrB 地址 ，(如 /home/zhiban/guoqing/20180822/wh/  (最后要加'/')):")
                config.version_svr["new_version_file"] = input("输入最新 qte_acsvrB 核心文件，(如 wh.tar.gz):")
            queren = input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.common_local_path["local_address"])
            # qte_acsvrB()
            print("删除 %s" % (config.common_local_path["local_address"],))
            shutil.rmtree(config.common_local_path["local_address"])
            print("已删除 %s 目录" % (config.common_local_path["local_address"],))
            print("--------------- 完成 更换 qte 前置 qte_acsvrB 操作! -----------------")


if __name__ == "__main__":
    main()