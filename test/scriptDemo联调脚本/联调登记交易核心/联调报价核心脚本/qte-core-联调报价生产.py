#! usr/bin/env python
# -*- coding:utf-8 -*-
import re,paramiko
import os,datetime,time,xlrd,sys

#将新版本包里的文件分别命名为A或B
def coppy_server(version_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[1])
    tar_path = os.path.split(version_ip[3])[0]
    print(tar_path)
    # stdin, stdout, stderr = ssh.exec_command('cd %s; mkdir tmp; tar -xf install.tar.gz -C tmp;'%tar_path)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mkdir tmp; cd install; cp -r * ../tmp; cd %s; rm -rf install'%(tar_path,tar_path))
    time.sleep(10)
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # # stdin, stdout, stderr = ssh.exec_command('cd %s/tmp/keepsvr; mkdir data'%tar_path)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r bridgesvr_tra bridgesvr_traA; mv bridgesvr_tra bridgesvr_traB; cp -r bussvr bussvrA; mv bussvr bussvrB; cp -r keepsvr keepsvrA; mv keepsvr keepsvrB; cp -r matchsvr matchsvrA; mv matchsvr matchsvrB'%tar_path)
    time.sleep(8)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin, stdout, stderr = ssh.exec_command('cd %s/tmp; cp -r qrysvr qrysvrA; mv qrysvr qrysvrB; cp -r qsvr qsvrA; mv qsvr qsvrB'%tar_path)
    time.sleep(6)
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
##上传新版本,并解压。
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


##复制结算行挡板等文件。
def coppy_ac(ipp,unm,passd,old_version_path,ser_list,conf_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    if 'qte_acsvr' in ser_list:
        print('qte_acsvr in')
        ssh.exec_command('cd %s/%s; cp -r qte_acsvr ../install'%(back_dir,old_install_name))
        print('qte_acsvr 复制成功 。')
    else:
        print('not found qte_acsvr')
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

##修改 conf文件。
def modefy_qte_conf(ipp,unm,passd,ser_list,conf_name,back_dir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    i = 0
    spit = ['qte_acsvr','qte_quotaacsvr','qte_qy_acsvr']
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
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                if '"init_data_path"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"init_data_path" : "/nfs/tip_data",\n'
                    data[line_num + 1] = '"init_file" : "/nfs/tip_data/tips_init_file.cfg",\n'
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
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
                if '"init_data_path"' in line:
                    line_num = data.index(line)
                    data[line_num] = '"init_data_path" : "/nfs/tip_data",\n'
                    data[line_num + 1] = '"init_file" : "/nfs/tip_data/tips_init_file.cfg",\n'
                    break
        with open('qsvr-A.cfg','w+') as fqn:
            for new_line in data:
                fqn.write(new_line)
        print('***************** qsv-A.cfg hase been modified sucessfuly! **********************')


def modefy_rescur(ser_list, conf_name, old_version_path,new_conf_name):
    if 'tra_syncsvr-A.cfg' in new_conf_name:
        with open('tra_syncsvr-A.cfg','r+') as fr:
            data = fr.readlines()
            for line in data:
                if '"grp_cfg"' in line :
                    num = data.index(line)
                    data[num] = '"grp_cfg" : "./conf/group.cfg",\n'
                if '"name"' in line:
                    num = data.index(line)
                    data[num] = '"name" : "/ssd/log/tra_syncsvr-A",\n'
                if '"dev"' in line:
                    num = data.index(line)
                    data[num] = '"dev" : 203,\n'
                if '"listen_port"' in line:
                    num = data.index(line)
                    data[num] = '"listen_port" : 9203,\n'
                if '"idx"' in line:
                    num = data.index(line)
                    data[num] = '"idx" : "/home/sge/install/keepsvrB/data/flowA.idx",\n'
                    data[num +1 ] = '"con" : "/home/sge/install/keepsvrB/data/flowA.con",\n'
            with open('tra_syncsvr-A.cfg','w+') as fr2:
                for line in data:
                    fr2.write(line)
                print('*********tra_syncsvr-A.cfg ok ! *******')
    if 'tra_syncsvr-B.cfg' in new_conf_name:
        with open('tra_syncsvr-B.cfg', 'r+') as fr:
            data = fr.readlines()
            for line in data:
                if '"grp_cfg"' in line:
                    num = data.index(line)
                    data[num] = '"grp_cfg" : "./conf/group.cfg",\n'
                if '"dev"' in line:
                    num = data.index(line)
                    data[num] = '"dev" : 204,\n'
                if '"listen_port"' in line:
                    num = data.index(line)
                    data[num] = '"listen_port" : 9204,\n'
                if '"name"' in line:
                    num = data.index(line)
                    data[num] = '"name" : "/ssd/log/tra_syncsvr-B",\n'
                if '"idx"' in line:
                    num = data.index(line)
                    data[num] = '"idx" : "/home/sge/install/keepsvrB/data/flowB.idx",\n'
                    data[num +1 ] = '"con" : "/home/sge/install/keepsvrB/data/flowB.con",\n'
            with open('tra_syncsvr-B.cfg', 'w+') as fr2:
                for line in data:
                    fr2.write(line)
                print('*********tra_syncsvr-B.cfg ok ! *******')


def sync_com(ipp,unm,passd,ser_list,conf_name,old_version_path,new_conf_name):
    if 'tra_syncsvr-A.cfg' in new_conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        date_str = str(datetime.datetime.now())[:10]
        old_install_name = 'install_%s' % date_str
        back_dir = os.path.split(old_version_path)[0]
        ssh.exec_command('cd %s/%s/tra_syncsvrA/conf; cp group_sync.cfg /home/sge/install/tra_syncsvrA/conf' % (back_dir, old_install_name))
        print('tra_syncsvrA group ok')
    if 'tra_syncsvr-B.cfg' in new_conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        date_str = str(datetime.datetime.now())[:10]
        old_install_name = 'install_%s' % date_str
        back_dir = os.path.split(old_version_path)[0]
        ssh.exec_command('cd %s/%s/tra_syncsvrB/conf; cp group_sync.cfg /home/sge/install/tra_syncsvrB/conf' % (back_dir, old_install_name))
        print('tra_syncsvrB group ok')


def mk_keep_data(ipp,unm,passd,conf_name):
    if 'keepsvr-A.cfg' in conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        ssh.exec_command('cd /home/sge/install/keepsvrA; mkdir data')
        time.sleep(2)
    if 'keepsvr-B.cfg' in conf_name:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        ssh.exec_command('cd /home/sge/install/keepsvrB; mkdir data')
        time.sleep(2)


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
                    data[line_num + 2] = '"password":"Oracle123!",\n'
                    data[line_num + 3] = '"dbname":"REG"\n'
                if '"nfs_dir"' in line :
                    line_num = data.index(line)
                    data[line_num] = '"nfs_dir": "/nfs/data"\n'
                if '"db_cfg"' in line:
                    line_num = data.index(line)
                    data[line_num + 1] = '"username":"tra_user",\n'
                    data[line_num + 2] = '"password":"Oracle123!",\n'
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
                data[line_num + 2] = '"password":"Oracle123!",\n'
                data[line_num + 3] = '"dbname":"REG"\n'
            if '"nfs_dir"' in line:
                line_num = data.index(line)
                data[line_num] = '"nfs_dir":"/nfs/tip_data"\n'
            if '"tbl_cfg": "conf/tips_init_tra_tbl.cfg",' in line:
                line_num = data.index(line)
                data[line_num + 2] = '"username":"HIS",\n'
                data[line_num + 3] = '"password":"Oracle123!",\n'
                data[line_num + 4] = '"dbname":"his"\n'
            if '"tbl_cfg": "conf/tips_init_ppr_tbl.cfg",' in line:
                line_num = data.index(line)
                data[line_num + 2] = '"username":"ppr_user",\n'
                data[line_num + 3] = '"password":"Oracle123!",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                            data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                        data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                        data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
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
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
        with open('quot_mem2dbsvr.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('quot_mem2dbsvr ok!')
    if 'quot_mem2dbsvr_thread.cfg' in conf_name:
        with open('quot_mem2dbsvr_thread.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "TRA",\n'
                if '"proc_id"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"proc_id": "quot",\n'
                if '"user_nm"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "tra_user",\n'
                if '"user_pwd"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "Oracle123!"\n'
        with open('quot_mem2dbsvr_thread.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('quot_mem2dbsvr_thread.cfg ok!')
    if 'trans_mem2dbsvr.cfg' in conf_name:
        with open('trans_mem2dbsvr.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"name"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"name":"/ssd/log/trans_mem2dbsvr",\n'
                if '"grp_cfg" :' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"grp_cfg" : "/nfs/tra_conf/group.cfg",\n'
        with open('trans_mem2dbsvr.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('trans_mem2dbsvr ok!')
    if 'trans_mem2dbsvr_thread.cfg' in conf_name:
        with open('trans_mem2dbsvr_thread.cfg', 'r+') as fm:
            data = fm.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"orc_inst": "TRA",\n'
                if '"proc_id"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"proc_id": "trans",\n'
                if '"user_nm"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_nm": "tra_user",\n'
                if '"user_pwd"' in line:
                    lin_num = data.index(line)
                    data[lin_num] = '"user_pwd": "Oracle123!"\n'
        with open('trans_mem2dbsvr_thread.cfg', 'w+')as fm:
            for line in data:
                fm.write(line)
        print('trans_mem2dbsvr_thread.cfg ok!')


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
    ac_group = ['acsvrB','acsvrA','intacsvr','quotaacsvr']
    ser_list =ser_list + ac_group
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
        # 将新版本包里的文件分别命名为A或B
        coppy_server(version_ip)
        print(ipp,old_version_path)

        ###重命名老版本install文件夹
        rename_isntall(ipp,unm,passd,old_version_path)
        ##下载新版本。
        inner(version_ip)
        ##上传新版本,并解压。
        outer(ipp, unm, passd, old_version_path)
        os.remove('install.tar.gz')

        # 拷贝前置服务
        coppy_ac(ipp, unm, passd, old_version_path, ser_list, conf_name)

        # 下载所有需要修改的cfg配置文件
        modefy_qte_conf(ipp,unm,passd,ser_list,conf_name,back_dir)

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
        modefy_rescur(ser_list, conf_name, old_version_path, new_conf_name)
        upload_confed_files(ipp,unm,passd,ser_list,new_conf_name,old_version_path)
        sync_com(ipp,unm,passd,ser_list,conf_name,old_version_path,new_conf_name)
        rm_noserver(ipp,unm,passd,ser_list,conf_name,old_version_path)
        mk_keep_data(ipp,unm,passd,conf_name)
        print('############################# 处理 %s 服务器 完成 。###############################' % ipp)
        time.sleep(2)
if __name__ == '__main__':
    big_list = read_excel('tra_conf-0801-liantiao.xls')
    main(big_list)
