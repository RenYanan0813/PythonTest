#! usr/bin/env python
# -*- coding:utf-8 -*-
import re,paramiko
import os,datetime,time,xlrd,sys
def coppy_server(version_ip,install_tar,install_name,tar_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[1])
    stdin1, stdout1, stderr1 = ssh.exec_command('cd %s; tar -xf %s; mv %s install' %(tar_path,install_tar,install_name))
    time.sleep(10)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mkdir tmp; cd install; cp -r * ../tmp'%tar_path)
    time.sleep(3)
    stdin, stdout, stderr = ssh.exec_command('cd %s; rm -rf install'%tar_path)
    time.sleep(10)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r authsvr authsvrA; mv authsvr authsvrB; cp -r bridgesvr_qte bridgesvr_qteA; mv bridgesvr_qte bridgesvr_qteB; cp -r corpsvr corpsvrA; mv corpsvr corpsvrB; cp -r dealsvr dealsvrA; mv dealsvr dealsvrB'%tar_path)
    time.sleep(8)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r infosvr infosvrA; mv infosvr infosvrB; cp -r loginsvr loginsvrA; mv loginsvr loginsvrB'%tar_path)
    time.sleep(6)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # stdin, stdout, stderr = ssh.exec_command('cd %s; tar -czf install.tar.gz *; cp install.tar.gz ../'%tar_path)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mv tmp install; tar -czf install.tar.gz install'%tar_path)
    time.sleep(5)
    print('newinstall.tar.gz creat ok !')
    ssh.close()
def inner(version_ip,tar_path):                 ##下载新版本。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[2])
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    tar_path = tar_path +'/install.tar.gz'
    sftp.get(tar_path,'install.tar.gz')
    ssh.close()
    print('download install.tar.gz ok')
    time.sleep(5)
def rename_isntall(ipp,unm,passd,old_version_path):   ###重命名。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    print(old_version_path)
    print(back_dir)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mv install %s'%(back_dir,old_install_name))
    print('备份 install 成功。文件名: %s'%old_install_name)
    ssh.close()
def outer(ipp,unm,passd,old_version_path):     ##上传新版本,并解压。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put('install.tar.gz',old_version_path)
    print('upload install.tar.gz finish')
    time.sleep(5)
    back_dir = os.path.split(old_version_path)[0]
    stdin, stdout, stderr = ssh.exec_command('cd %s; tar -xvf install.tar.gz'%back_dir)
    time.sleep(5)
    stdin, stdout, stderr = ssh.exec_command('cd %s; ls'%back_dir)
    stout_str = str(stdout.read())
    if 'install' in stout_str:
        print('新版本文件安置成功！')
    ssh.close()

def mk_qte_data(ipp,unm,passd,conf_name):
    if 'authsvr-A.cfg' in conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        ssh.exec_command('cd /home/qte/install/authsvrA; mkdir data')
        time.sleep(2)
        ssh.close()
    if 'authsvr-B.cfg' in conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        ssh.exec_command('cd /home/qte/install/authsvrB; mkdir data')
        time.sleep(2)
        ssh.close()

def coppy_ac(ipp,unm,passd,old_version_path,ser_list,conf_name):  ##复制结算行挡板等文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    if 'qte-acsvr' in ser_list:
        print('qte-acsvr in')
        ssh.exec_command('cd %s/%s; cp -r qte-acsvr ../install'%(back_dir,old_install_name))
        print('qte-acsvr 复制成功 。')
    else:
        print('not found qte-acsvr')
    if 'qte_quotaacsvr' in ser_list:
        print('qte_quotaacsvr in')
        ssh.exec_command('cd %s/%s; cp -r qte_quotaacsvr ../install'%(back_dir,old_install_name))
        print('qte_quotaacsvr 复制成功 。')
    else:
        print('not found qte_quotaacsvr')
    if 'qte_qy_acsvr' in ser_list:
        print('qte_qy_acsvr in')
        ssh.exec_command('cd %s/%s; cp -r qte_qy_acsvr ../install' % (back_dir, old_install_name))
        print('qte_qy_acsvr 复制成功 。')
    else:
        print('not found qte_qy_acsvr')
    ssh.close()

def modefy_tra_conf(ipp,unm,passd,ser_list,conf_name,back_dir):  ##修改 conf文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    i = 0
    #spit = ['qte_qy_acsvr','qte_quotaacsvr','qte_acsvr','qte_monsvr','group_qte.cfg','monsvr']
    spit = ['qte_qy_acsvr','qte_quotaacsvr','qte_acsvr']

    for ser in ser_list:
        if ser in spit:
            i += 1
            pass
        else:
            cfg = conf_name[i]
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            print('开始下载 %s'%cfg)
            strr= '%s/install/%s/conf/%s'%(back_dir,ser,cfg)
            time.sleep(1)
            sftp.get('%s/install/%s/conf/%s'%(back_dir,ser,cfg),'%s'%cfg)
            print('get %s done !'%cfg)
            i += 1
            time.sleep(1)
    ssh.close()
    print('总共有 %s 个服务，共有 %s 个配置cfg文件'%(len(ser_list),len(conf_name)))

def modefy_initsvr_qte(ser_list,conf_name):
    if 'qte_initsvr.cfg' in conf_name:
        with open('qte_initsvr.cfg','r+')as finit:
            data = finit.readlines()
            for line in data:
                if '"name"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"name":"/home/qte/log/qte_initsvr",\n'
                if '"comm_db_cfg":' in line:
                    line_num = data.index(line)
                    data[line_num + 1] = '"username":"par_user",\n'
                    data[line_num + 2] = '"password":"Oracle123!",\n'
                    data[line_num + 3] = '"dbname":"reg"\n'
                if '"nfs_dir"' in line :
                    line_num = data.index(line)
                    data[line_num] = '"nfs_dir": "/nfs/data"\n'
                if '"db_cfg"' in line:
                    line_num = data.index(line)
                    data[line_num + 1] = '"username":"qte_user",\n'
                    data[line_num + 2] = '"password":"oracle123!",\n'
                    data[line_num + 3] = '"dbname":"tra"\n'
            with open('qte_initsvr.cfg','w+') as fw:
                for line in data:
                    fw.write(line)
            print('**************qte_initsvr ok ! *****************')
    else:
        print('该服务器上不存在qte_initsvr服务')

def modefy_corpsvr(ser_list,conf_name):
    if 'corpsvrA' in ser_list:
        os.rename('corpsvr.cfg','corpsvr-A.cfg')
        with open('corpsvr-A.cfg','r+') as fb:
            data = fb.readlines()
            for line in data:
                if '"name":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/corpsvrA",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9201,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 201,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                if '"data_path"' in line :
                    lin_num = data.index(line)
                    data[lin_num] = '"data_path" : "/nfs/data",\n'
                    data[lin_num + 1] = '"init_cfg_file" : "/nfs/data/init_file_qte.cfg",\n'
                    data[lin_num + 2] = '"startwork_cfg" : "/nfs/data/startwork_qte.inf",\n'
        with open('corpsvr-A.cfg','w+') as fa:
            for line in data:
                fa.write(line)
        print('corpsvr-A.cfg ok !' )
    if 'corpsvrB' in ser_list:
        os.rename('corpsvr.cfg','corpsvr-B.cfg')
        with open('corpsvr-B.cfg','r+') as fb:
            data = fb.readlines()
            for line in data:
                if '"name":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/corpsvrB",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9202,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 202,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                if '"data_path"' in line :
                    lin_num = data.index(line)
                    data[lin_num] = '"data_path" : "/nfs/data",\n'
                    data[lin_num + 1] = '"init_cfg_file" : "/nfs/data/init_file_qte.cfg",\n'
                    data[lin_num + 2] = '"startwork_cfg" : "/nfs/data/startwork_qte.inf",\n'
        with open('corpsvr-B.cfg','w+') as fa:
            for line in data:
                fa.write(line)
        print('corpsvrB.cfg ok !' )

def modefy_dealsvr(ser_list,conf_name):
    for ser in ser_list:
        if 'dealsvr' in ser:
            if 'dealsvrA' in ser_list:
                os.rename('dealsvr.cfg','dealsvr-A.cfg')
                with open('dealsvr-A.cfg','r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line :
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/home/qte/log/dealsvrA",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":9401,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 401,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                with open('dealsvr-A.cfg','w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* dealsvrA.cfg modefy ok ! **************')
            if 'dealsvrB' in ser_list:
                os.rename('dealsvr.cfg','dealsvr-B.cfg')
                with open('dealsvr-B.cfg','r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line :
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/home/qte/log/dealsvrB",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":9402,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 402,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
                with open('dealsvr-B.cfg','w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* dealsvrB.cfg modefy ok ! **************')
def modefy_infosvr(ser_list,conf_name):
    if 'infosvrA' in ser_list:
        os.rename('infosvr.cfg', 'infosvr-A.cfg')
        with open('infosvr-A.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/infosvrA",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9501,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev": 501,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('infosvr-A.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* infosvrA.cfg modefy ok ! **************')
    if 'infosvrB' in ser_list:
        os.rename('infosvr.cfg', 'infosvr-B.cfg')
        with open('infosvr-B.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/infosvrB",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9502,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 502,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('infosvr-B.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* infosvrB.cfg modefy ok ! **************')
    else:
        print('no infosvr !')

def modrfy_loginsvr(ser_list,conf_name):
    # for ser in ser_list:
    if 'loginsvrA' in ser_list:
        os.rename('loginsvr.cfg', 'loginsvr-A.cfg')
        with open('loginsvr-A.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/loginsvrA",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port" : 14001,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev": 1401,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('loginsvr-A.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* loginsvrA.cfg modefy ok ! **************')
    if 'loginsvrB' in ser_list:
        os.rename('loginsvr.cfg', 'loginsvr-B.cfg')
        with open('loginsvr-B.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/loginsvrB",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port" : 14002,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 1402,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('loginsvr-B.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* loginsvrB.cfg modefy ok ! **************')
    if 'ppr_db_handle.cfg' in conf_name:
        # os.rename('loginsvr.cfg', 'loginsvrB.cfg')
        with open('ppr_db_handle.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "cln",\n'
                if '"user_nm"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "ppr_user",\n'
                if '"user_pwd"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "Oracle123!"'
        with open('ppr_db_handle.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* ppr_db_handle.cfg modefy ok ! **************')
    if 'qte_db_handle.cfg' in conf_name:
        # os.rename('loginsvr.cfg', 'loginsvrB.cfg')
        with open('qte_db_handle.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "tra",\n'
                if '"user_nm"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "qte_user",\n'
                if '"user_pwd"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "oracle123!"'
        with open('qte_db_handle.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* qte_db_handle.cfg ok ! **************')
    if 'reg_db_handle.cfg' in conf_name:
        # os.rename('loginsvr.cfg', 'loginsvrB.cfg')
        with open('reg_db_handle.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "reg",\n'
                if '"user_nm"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "reg_user",\n'
                if '"user_pwd"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "Oracle123!"'
        with open('reg_db_handle.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* reg_db_handle.cfg ok ! **************')


def modefy_authsvr(ser_list,conf_name):
    if 'authsvr-B.cfg' in conf_name:
        with open('authsvr-B.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/authsvr-B",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('authsvr-B.cfg.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* authsvr-B.cfg modefy ok ! **************')
    if 'authsvr-A.cfg' in conf_name:
        with open('authsvr-A.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/authsvrA",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('authsvr-A.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* authsvr-A.cfg modefy ok ! **************')

def modefy_bridgesvr_qte(ser_list,new_conf_name):
    if 'bridgesvr_qte-A.cfg' in new_conf_name:
        os.rename('bridgesvr.cfg', 'bridgesvr_qte-A.cfg')
        with open('bridgesvr_qte-A.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/bridgesvr-qteA",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":91101,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 1101,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('bridgesvr_qte-A.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* authsvr-B.cfg modefy ok ! **************')
    if 'bridgesvr_qte-B.cfg' in new_conf_name:
        os.rename('bridgesvr.cfg', 'bridgesvr_qte-B.cfg')
        with open('bridgesvr_qte-B.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/bridgesvr-qteB",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":91102,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 1102,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('bridgesvr_qte-B.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* bridgesvr-qteB.cfg modefy ok ! **************')

def modefy_qte_mem2dbsvr(ser_list,conf_name):
    if 'qte_mem2dbsvr.cfg' in conf_name:
        with open('qte_mem2dbsvr.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/home/qte/log/qte_mem2dbsvr",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group_qte.cfg",\n'
        with open('qte_mem2dbsvr.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('qte_mem2dbsvr ok!')
    if 'mem2dbsvr_thread.cfg' in conf_name:
        with open('mem2dbsvr_thread.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "tra",\n'
                if '"proc_id"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"proc_id": "qte",\n'
                if '"user_nm":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "qte_user",\n'
                if '"user_pwd":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "oracle123!"\n'
        with open('mem2dbsvr_thread.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('mem2dbsvr_thread.cfg ok!')


#########################################

def upload_confed_files(ipp,unm,passd,ser_list,conf_name,old_version_path):       ##上传修改完的文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    back_dir = os.path.split(old_version_path)[0]
    i = 0
    spit = ['qte_qy_acsvr','qte_quotaacsvr','qte_acsvr','qte_monsvr','group_qte.cfg','monsvr']
    for ser in ser_list:
        if ser in spit:
            i += 1
            pass
        else:
            cfg = conf_name[i]
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            sftp.put('%s'%cfg,'%s/install/%s/conf/%s'%(back_dir,ser,cfg))
            print('put %s done !'%cfg)
            os.remove(cfg)
            i += 1
            time.sleep(1)
    ssh.close()
    print('upload all  files successfully!')

def rm_noserver(ipp,unm,passd,ser_list,conf_name,old_version_path):
    back_dir = os.path.split(old_version_path)[0]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    # stdin, stdout, stderr = ssh.exec_command('cd %s/install; rm -rf %s'%(back_dir,ser)
    stdin, stdout, stderr = ssh.exec_command('cd %s/install; ls'%back_dir)
    temp1 = stdout.read().split()
    ac_group = ['qte_qy_acsvr','qte_quotaacsvr','qte_acsvr','qte_monsvr','group_qte.cfg','monsvr']
    ser_list = ser_list + ac_group

    new_se = []
    for i in ser_list:
        i = str(i)
        new_se.append(i)
    ser_list = new_se
    new2 = []
    for j in temp1:
        readstr = j.decode('utf-8')
        # j = str(readstr)
        new2.append(readstr)
    temp1 = new2

    for ser in temp1:
        if ser in ser_list:
            pass
        else:
            stdin_2, stdout_2, stderr_2 = ssh.exec_command('cd %s/install; rm -rf %s' % (back_dir,ser))
            time.sleep(1)

def read_excel(file):
    data = xlrd.open_workbook(file)
    # if sys.getdefaultencoding() != 'utf-8':
    #     reload(sys)
    #     sys.setdefaultencoding('utf-8')

    import importlib,sys
    if sys.getdefaultencoding() != 'utf-8':
        sys.setdefaultencoding('utf-8')
        importlib.reload(sys)

    table = data.sheets()[0]
    nrows = table.nrows
    version_ip = [table.row_values(1)[0], table.row_values(1)[1], table.row_values(1)[2], table.row_values(1)[3]]
    num = nrows - 2
    print('- - - - - 获取到 %d 台服务器需要更新 ！ - - -  - -'%num)
    big_list = []
    version_ip = [table.row_values(1)[0],table.row_values(1)[1],table.row_values(1)[2],table.row_values(1)[3]]
    if nrows <= 2:
        print('no reg_serverlist')
    else:
        i = 2
        while i <= nrows - 1:
            l = [table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],table.row_values(i)[3],table.row_values(i)[4].split(','),table.row_values(i)[5].split(','),table.row_values(i)[6].split(',')]
            big_list.append(l)
            i += 1
    #print(big_list)
    return [big_list,version_ip]

def main(total):
    big_list = total[0]
    version_ip = total[1]
    install_tar = os.path.split(version_ip[3])[1]
    print(install_tar)
    install_name = install_tar.split('.')[0]
    tar_path = os.path.split(version_ip[3])[0]
    print('00000%s'%tar_path)
    for sercell in big_list:
        ipp = sercell[0]
        unm = sercell[1]
        passd = sercell[2]
        ser_list = sercell[4]
        conf_name = sercell[5]
        new_conf_name = sercell[6]
        old_version_path = sercell[3]
        back_dir = os.path.split(old_version_path)[0]
        print('****************************************** 开始处理 %s 服务器。****************************************'%ipp)
        time.sleep(2)
        coppy_server(version_ip, install_tar, install_name, tar_path)
        print(ipp,old_version_path)
        rename_isntall(ipp,unm,passd,old_version_path)
        inner(version_ip, tar_path)
        outer(ipp, unm, passd, old_version_path)
        os.remove('install.tar.gz')
        coppy_ac(ipp, unm, passd, old_version_path, ser_list, conf_name)
        modefy_tra_conf(ipp,unm,passd,ser_list,conf_name,back_dir)
        modefy_initsvr_qte(ser_list, conf_name)
        modefy_corpsvr(ser_list, conf_name)
        modefy_dealsvr(ser_list, conf_name)
        modefy_infosvr(ser_list, conf_name)
        modrfy_loginsvr(ser_list, conf_name)
        modefy_authsvr(ser_list, conf_name)
        modefy_bridgesvr_qte(ser_list, new_conf_name)
        modefy_qte_mem2dbsvr(ser_list, conf_name)
        upload_confed_files(ipp,unm,passd,ser_list,new_conf_name,old_version_path)
        rm_noserver(ipp, unm, passd, ser_list, conf_name, old_version_path)
        mk_qte_data(ipp, unm, passd, conf_name)
        print('############################# 处理 %s 服务器 完成 。###############################' % ipp)
        time.sleep(2)
if __name__ == '__main__':
    big_list = read_excel('qte_conf-2324-realinfo.xls')
    main(big_list)
