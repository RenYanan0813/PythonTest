#! usr/bin/env python
# -*- coding:utf-8 -*-
import re,paramiko
import os,datetime,time,xlrd,sys
def coppy_server(version_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[1])
    tar_path = os.path.split(version_ip[3])[0]
    print(tar_path)
    # stdin, stdout, stderr = ssh.exec_command('cd %s; mkdir tmp; tar -xf install.tar.gz -C tmp;'%tar_path)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mkdir tmp; cd install; cp -r * ../tmp; cd %s; rm -rf install'%(tar_path,tar_path))
    time.sleep(5)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r bridgesvr_tra bridgesvr_traA; mv bridgesvr_tra bridgesvr_traB; cp -r bussvr bussvrA; mv bussvr bussvrB; cp -r keepsvr keepsvrA; mv keepsvr keepsvrB; cp -r matchsvr matchsvrA; mv matchsvr matchsvrB'%tar_path)
    time.sleep(5)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r qrysvr qrysvrA; mv qrysvr qrysvrB; cp -r qsvr qsvrA; mv qsvr qsvrB'%tar_path)
    time.sleep(5)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # stdin, stdout, stderr = ssh.exec_command('cd %s; tar -czf install.tar.gz *; cp install.tar.gz ../'%tar_path)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mv tmp install; tar -czf install.tar.gz install'%tar_path)
    time.sleep(5)
    print('newinstall.tar.gz creat ok !')
    ssh.close()
def inner(version_ip):                 ##下载新版本。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[2])
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    # tem_path =os.path.split(version_ip[3])[0] + '/tmp' + '/install.tar.gz'
    sftp.get(version_ip[3],'install.tar.gz')
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
    if 'install' in stdout.read():
        print('新版本文件安置成功！')
    ssh.close()

############## 以下为老 ############# old 1 ####
'''
def modefy_tra_conf(ipp,unm,passd,ser_list,conf_name,back_dir):  ##修改 conf文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    i = 0
    for ser in ser_list:
        cfg = conf_name[i]
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        print('开始下载 %s'%cfg)
        print(back_dir)
        print(ser)
        print(cfg)
        strr= '%s/install/%s/conf/%s'%(back_dir,ser,cfg)
        print(strr)
        time.sleep(1)
        sftp.get('%s/install/%s/conf/%s'%(back_dir,ser,cfg),'%s'%cfg)
        print('get %s done !'%cfg)
        i += 1
        time.sleep(1)
    ssh.close()
    print('总共有 %s 个服务，共有 %s 个配置cfg文件'%(len(ser_list),len(conf_name)))
    # for cfg in conf_name:
    #     if cfg == 'initsvr.cfg' or cfg == 'tips_init.cfg':
    #         pass
    #     else:
    #         print('开始修改 %s 文件'%cfg)
    #         num = conf_name.index(cfg)
    #         nstr = ser_list[num]
    #         with open('%s'%cfg,'r+') as f:
    #             data = f.readlines()
    #             mark1 = False
    #             mark2 = False
    #             # mark3 = False
    #             for line in data:
    #                 if '"name"' in line and mark1 == False:
    #                     line_rownum = data.index(line)
    #                     # nstr = cfg[:-4]
    #
    #                     new_line = '    "name" : "/ssd/log/%s",\n'%nstr
    #                     data[line_rownum] = new_line
    #                     print('更新 %s 文件log参数 成功 。'%cfg)
    #                     mark1 = True
    #                 if '"grp_cfg"' in line and mark2 == False:
    #                     line_rownum = data.index(line)
    #                     new_line = '    "grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
    #                     data[line_rownum] = new_line
    #                     print('更新 %s 文件 grp 成功 。'%cfg)
    #                     mark2 = True
    #                     break
    #             if mark1 == True and mark2 == True:
    #                 with open('%s'%cfg,'w+') as f2:
    #                     for lines in data:
    #                         f2.write(lines)
    #                 print('更新 %s 文件 2 个配置成功。' % cfg)
# print('all log_path and grp_cfg have been modified sucessfully !')
'''
############## 以下为新加入，以上为老############# old 1 ### new1 #


def coppy_ac(ipp,unm,passd,old_version_path,ser_list,conf_name):  ##复制结算行挡板等文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    # ssh.exec_command('cd %s/%s; cp acct.sh ../install'%(back_dir,old_install_name))   ########联调mosnvr不在install。
    # print('coppy acct.sh files ok')
    # stdin, stdout, stderr = ssh.exec_command('cd %s/%s; ls'%(back_dir,old_install_name))
    # tem = stdout.read()
    if 'acsvrA' in ser_list:
        print('acsvrA in')
        ssh.exec_command('cd %s/%s; cp -r acsvrA ../install'%(back_dir,old_install_name))
        print('acsvrA 复制成功 。')
    else:
        print('not found acsvrA')
    if 'acsvrB' in ser_list:
        print('acsvrB in')
        ssh.exec_command('cd %s/%s; cp -r acsvrB ../install'%(back_dir,old_install_name))
        print('acsvrB 复制成功 。')
    else:
        print('not found acsvrB')
    if 'intacsvr' in ser_list:
        print('intacsvr in')
        ssh.exec_command('cd %s/%s; cp -r intacsvr ../install' % (back_dir, old_install_name))
        print('intacsvr 复制成功 。')
    else:
        print('not found intacsvr')
    if 'quotaacsvr' in ser_list:
        print('quotaacsvr in')
        ssh.exec_command('cd %s/%s; cp -r quotaacsvr ../install' % (back_dir, old_install_name))
        print('quotaacsvr 复制成功 。')
    else:
        print('not found quotaacsvr')
    ssh.close()

def modefy_tra_conf(ipp,unm,passd,ser_list,conf_name,back_dir):  ##修改 conf文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    i = 0
    spit = ['acsvrA','acsvrB','intacsvr','quotaacsvr']
    for ser in ser_list:
        if ser in spit:
            i += 1
            pass
        else:
            cfg = conf_name[i]
            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname=ipp, username=unm, password=passd)
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            print('开始下载 %s'%cfg)
            # print(back_dir)
            # print(ser)
            # print(cfg)
            strr= '%s/install/%s/conf/%s'%(back_dir,ser,cfg)
            # print(strr)
            time.sleep(1)
            sftp.get('%s/install/%s/conf/%s'%(back_dir,ser,cfg),'%s'%cfg)
            print('get %s done !'%cfg)
            i += 1
            time.sleep(1)
    ssh.close()
    print('总共有 %s 个服务，共有 %s 个配置cfg文件'%(len(ser_list),len(conf_name)))




############## 以上为新加入############### new1 #


###############################################
def modefy_qsvr(ser_list,conf_name):
    if 'qsvrB' in ser_list:
        os.rename('qsvr.cfg','qsvr-B.cfg')
        with open('qsvr-B.cfg','r+') as fk:
            data = fk.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/qsvr-B",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9502,\n'
                if '"dev"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"dev": 502,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                if '"init_data_path"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"init_data_path" : "/nfs/data_tip",\n'
                    data[line_num + 1] = '"init_file" : "/nfs/data_tip/tips_init_file.cfg",\n'
                    break
        with open('qsvr-B.cfg','w+') as fqn:
            for new_line in data:
                fqn.write(new_line)
        print('***************** qsv-B.cfg hase been modified sucessfuly! *********************')

    if 'qsvrA' in ser_list:
        os.rename('qsvr.cfg','qsvr-A.cfg')
        with open('qsvr-A.cfg','r+') as fk:
            data = fk.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/qsvr-A",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9501,\n'
                if '"dev"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"dev": 501,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                if '"init_data_path"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"init_data_path" : "/nfs/data_tip",\n'
                    data[line_num + 1] = '"init_file" : "/nfs/data_tip/tips_init_file.cfg",\n'
                    break
        with open('qsvr-A.cfg','w+') as fqn:
            for new_line in data:
                fqn.write(new_line)
        print('***************** qsv-A.cfg hase been modified sucessfuly! **********************')
def modefy_initsvr_tra(ser_list,conf_name):
    if 'initsvr_tra' in ser_list:
        with open('initsvr.cfg','r+')as finit:
            data = finit.readlines()
            for line in data:
                if '"name"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"name":"/ssd/log/initsvr",\n'
                if '"comm_db_cfg":' in line:
                    line_num = data.index(line)
                    data[line_num + 1] = '"username":"par_user",\n'
                    data[line_num + 2] = '"password":"oracle123!",\n'
                    data[line_num + 3] = '"dbname":"REG"\n'
                if '"nfs_dir"' in line :
                    line_num = data.index(line)
                    data[line_num] = '"nfs_dir": "/nfs/data"\n'
                if '"db_cfg"' in line:
                    line_num = data.index(line)
                    data[line_num + 1] = '"username":"tra_user",\n'
                    data[line_num + 2] = '"password":"oracle123!",\n'
                    data[line_num + 3] = '"dbname":"TRA"\n'
            with open('initsvr.cfg','w+') as fw:
                for line in data:
                    fw.write(line)
            print('**************initsvr_tra ok ! *****************')
    else:
        print('该服务器上不存在initsvr服务')

def modefy_tips_initsvr_tra(ser_list,conf_name):
    if 'tips_initsvr_tra' in ser_list:
        with open('tips_init.cfg','r+') as f:
            data = f.readlines()
        for line in data:
            if '"name":' in line:
                line_num = data.index(line)
                data[line_num] = '"name":"/ssd/log/tips_init",\n'
            if '"comm_db_cfg":' in line:
                line_num = data.index(line)
                data[line_num + 1] = '"username":"par_user",\n'
                data[line_num + 2] = '"password":"oracle123!",\n'
                data[line_num + 3] = '"dbname":"REG"\n'
            if '"nfs_dir"' in line:
                line_num = data.index(line)
                data[line_num] = '"nfs_dir":"/nfs/data_tip"\n'
            if '"tbl_cfg": "conf/tips_init_tra_tbl.cfg",' in line:
                line_num = data.index(line)
                data[line_num + 2] = '"username":"his",\n'
                data[line_num + 3] = '"password":"oracle123!",\n'
                data[line_num + 4] = '"dbname":"HIS"\n'
            if '"tbl_cfg": "conf/tips_init_ppr_tbl.cfg",' in line:
                line_num = data.index(line)
                data[line_num + 2] = '"username":"ppr_user",\n'
                data[line_num + 3] = '"password":"oracle123!",\n'
                data[line_num + 4] = '"dbname":"CLN"\n'
        with open('tips_init.cfg','w+') as fn:
            for line in data:
                fn.write(line)
        print('***************** initscr_tra ok ! *********************')
    else:
        print('该服务器上不存在 initsvr_tra !')
def modefy_bussvr(ser_list,conf_name):
    if 'bussvrA' in ser_list:
        os.rename('bussvr.cfg','bussvr-A.cfg')
        with open('bussvr-A.cfg','r+') as fb:
            data = fb.readlines()
            for line in data:
                if '"name":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/bussvr-A",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9201,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 201,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                if '"data_path"' in line :
                    lin_num = data.index(line)
                    data[lin_num] = '"data_path" : "/nfs/data",\n'
                    data[lin_num + 1] = '"init_cfg_file" : "/nfs/data/init_file.cfg",\n'
                    data[lin_num + 2] = '"startwork_cfg" : "/nfs/data/startwork.inf",\n'
        with open('bussvr-A.cfg','w+') as fa:
            for line in data:
                fa.write(line)
        print('bussvr-A.cfg ok !' )
    if 'bussvrB' in ser_list:
        os.rename('bussvr.cfg','bussvr-B.cfg')
        with open('bussvr-B.cfg','r+') as fb:
            data = fb.readlines()
            for line in data:
                if '"name":' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/bussvr-B",\n'
                if '"listen_port"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"listen_port":9202,\n'
                if '"dev"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"dev" : 202,\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                if '"data_path"' in line :
                    lin_num = data.index(line)
                    data[lin_num] = '"data_path" : "/nfs/data",\n'
                    data[lin_num + 1] = '"init_cfg_file" : "/nfs/data/init_file.cfg",\n'
                    data[lin_num + 2] = '"startwork_cfg" : "/nfs/data/startwork.inf",\n'
        with open('bussvr-B.cfg','w+') as fa:
            for line in data:
                fa.write(line)
        print('bussvr-B.cfg ok !' )

def modefy_match(ser_list,conf_name):
    for ser in ser_list:
        if 'matchsvr' in ser:
            if 'matchsvrA' in ser_list:
                os.rename('matchsvr.cfg','matchsvr-A.cfg')
                with open('matchsvr-A.cfg','r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line :
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/matchsvr-A",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":9401,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 401,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('matchsvr-A.cfg','w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* matchsvr-A.cfg modefy ok ! **************')
            if 'matchsvrB' in ser_list:
                os.rename('matchsvr.cfg','matchsvr-B.cfg')
                with open('matchsvr-B.cfg','r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line :
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/matchsvr-B",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":9402,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 402,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('matchsvr-B.cfg','w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* matchsvr-B.cfg modefy ok ! **************')
def modefy_qrysvr(ser_list,conf_name):
    for ser in ser_list:
        if 'qrysvr' in ser:
            if 'qrysvrA' in ser_list:
                os.rename('qrysvr.cfg', 'qrysvr-A.cfg')
                with open('qrysvr-A.cfg', 'r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/qrysvr-A",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":91101,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev": 1101,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('qrysvr-A.cfg', 'w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* qrysvr-A.cfg modefy ok ! **************')
            if 'qrysvrB' in ser_list:
                os.rename('qrysvr.cfg', 'qrysvr-B.cfg')
                with open('qrysvr-B.cfg', 'r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/qrysvr-B",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port":91102,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 1102,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('qrysvr-B.cfg', 'w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* qrysvr-B.cfg modefy ok ! **************')
            else:
                print('no qrysvr !')

def modrfy_bridge(ser_list,conf_name):
    for ser in ser_list:
        if 'bridgesvr_tra' in ser:
            if 'bridgesvr_traA' in ser_list:
                os.rename('bridgesvr.cfg', 'bridgesvr_tra-A.cfg')
                with open('bridgesvr_tra-A.cfg', 'r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/bridgesvr_tra-A",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port" : 93001,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev": 3001,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('bridgesvr_tra-A.cfg', 'w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* bridgesvr_tra-A.cfg modefy ok ! **************')
            if 'bridgesvr_traB' in ser_list:
                os.rename('bridgesvr.cfg', 'bridgesvr_tra-B.cfg')
                with open('bridgesvr_tra-B.cfg', 'r+') as fm:
                    data = fm.readlines()
                    for line in data:
                        if '"name"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"name":"/ssd/log/bridgesvr_tra-B",\n'
                        if '"listen_port"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"listen_port" : 93002,\n'
                        if '"dev"' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"dev" : 3002,\n'
                        if '"grp_cfg" :' in line:
                            lin_num = data.index(line)
                            data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
                with open('bridgesvr_tra-B.cfg', 'w+')as fm:
                    for line in data:
                        fm.write(line)
                print('************* bridgesvr_tra-B.cfg modefy ok ! **************')

def modefy_acsvr(ser_list,conf_name):
    for ser in ser_list:
        if 'acsvrA' in ser:
            os.rename('acsvr.cfg', 'acsvr-A.cfg')
            with open('acsvr-A.cfg', 'r+') as fm:
                data = fm.readlines()
                for line in data:
                    if '"name"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"name":"/ssd/log/acsvr-A",\n'
                    if '"listen_port"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"listen_port" : 9311,\n'
                    if '"listen_ports"' in line:
                        lin_num = data.index(line)
                        data[lin_num + 1]  = '7777:1,\n'
                        data[lin_num + 2] = '16999:2\n'
                    if '"dev"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"dev": 101,\n'
                    if '"grp_cfg" :' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
            with open('acsvr-A.cfg', 'w+')as fm:
                for line in data:
                    fm.write(line)
            print('************* acsvr-A.cfg modefy ok ! **************')
        if 'acsvrB' in ser_list:
            os.rename('acsvr.cfg', 'acsvr-B.cfg')
            with open('acsvr-B.cfg', 'r+') as fm:
                data = fm.readlines()
                for line in data:
                    if '"name"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"name":"/ssd/log/acsvr-B",\n'
                    if '"listen_port"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"listen_port" : 9311,\n'
                    if '"listen_ports"' in line:
                        lin_num = data.index(line)
                        data[lin_num + 1]  = '7777:1,\n'
                        data[lin_num + 2] = '16999:2\n'
                    if '"dev"' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"dev" : 102,\n'
                    if '"grp_cfg" :' in line:
                        lin_num = data.index(line)
                        data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
            with open('acsvr-B.cfg', 'w+')as fm:
                for line in data:
                    fm.write(line)
            print('************* acsvr-B.cfg modefy ok ! **************')


def modefy_keepsvr(ser_list,conf_name):
    if 'keepsvr-A.cfg' in conf_name:
        with open('keepsvr-A.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/keepsvr-A",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
        with open('keepsvr-A.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* keepsvr-A.cfg modefy ok ! **************')
    if 'keepsvr-B.cfg' in conf_name:
        with open('keepsvr-B.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/keepsvr-B",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
        with open('keepsvr-B.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('************* keepsvr-A.cfg modefy ok ! **************')

def modefy_mem2db(ser_list,conf_name):
    if 'quot_mem2dbsvr.cfg' in conf_name:
        with open('quot_mem2dbsvr.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/quot_mem2dbsvr",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
        with open('quot_mem2dbsvr.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('quot_mem2dbsvr ok!')
    if 'trans_mem2dbsvr.cfg' in conf_name:
        with open('trans_mem2dbsvr.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/trans_mem2dbsvr",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/conf/group.cfg",\n'
        with open('trans_mem2dbsvr.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('trans_mem2dbsvr ok!')















#########################################

def upload_confed_files(ipp,unm,passd,ser_list,conf_name,old_version_path):       ##上传修改完的文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    back_dir = os.path.split(old_version_path)[0]
    i = 0
    spit = ['acsvrA', 'acsvrB', 'intacsvr', 'quotaacsvr']
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
    for ser in temp1:
        if ser in ser_list:
            pass
        else:
            stdin_2, stdout_2, stderr_2 = ssh.exec_command('cd %s/install; rm -rf %s' % (back_dir,ser))
            time.sleep(1)



def read_excel(file):
    data = xlrd.open_workbook(file)
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
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
        coppy_server(version_ip)
        print(ipp,old_version_path)
        rename_isntall(ipp,unm,passd,old_version_path)
        inner(version_ip)
        outer(ipp, unm, passd, old_version_path)
        os.remove('install.tar.gz')
        coppy_ac(ipp, unm, passd, old_version_path, ser_list, conf_name)
        modefy_tra_conf(ipp,unm,passd,ser_list,conf_name,back_dir)
        modefy_qsvr(ser_list, conf_name)
        modefy_initsvr_tra(ser_list, conf_name)
        modefy_tips_initsvr_tra(ser_list, conf_name)
        modefy_bussvr(ser_list, conf_name)
        modefy_match(ser_list, conf_name)
        modefy_qrysvr(ser_list, conf_name)
        modrfy_bridge(ser_list, conf_name)
        #modefy_acsvr(ser_list, conf_name)
        modefy_keepsvr(ser_list, conf_name)
        modefy_mem2db(ser_list, conf_name)

        # upload_confed_files(ipp,unm,passd,ser_list,conf_name,old_version_path)
        upload_confed_files(ipp,unm,passd,ser_list,new_conf_name,old_version_path)
        rm_noserver(ipp, unm, passd, ser_list, conf_name, old_version_path)
        print('############################# 处理 %s 服务器 完成 。###############################' % ipp)
        time.sleep(2)
if __name__ == '__main__':
    big_list = read_excel('tra_conf-229230-realinfo.xls')
    main(big_list)
