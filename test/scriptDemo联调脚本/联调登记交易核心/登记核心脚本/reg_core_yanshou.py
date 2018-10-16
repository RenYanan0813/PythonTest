#! usr/bin/env python
# -*- coding:utf-8 -*-
import re,paramiko
import os,datetime,time,xlrd,sys

def inner(version_ip):                 ##下载新版本。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=version_ip[0], username=version_ip[1], password=version_ip[1])
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.get(version_ip[3], 'install.tar.gz')
    ssh.close()
    print('download install.tar.gz ok')
def outer(ipp,unm,passd,old_version_path):     ##上传新版本,并解压。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put('install.tar.gz', old_version_path)
    print('upload install.tar.gz finish')
    back_dir = os.path.split(old_version_path)[0]
    stdin, stdout, stderr = ssh.exec_command('cd %s; tar -xvf install.tar.gz'%back_dir)
    time.sleep(20)
    stdin, stdout, stderr = ssh.exec_command('cd %s; ls'%back_dir)
    if 'install' in stdout.read():
        print('新版本文件安置成功！')
    ssh.close()

def rename_isntall(ipp,unm,passd,old_version_path):   ###重命名。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    print(back_dir)
    stdin, stdout, stderr = ssh.exec_command('cd %s; mv install %s' % (back_dir,old_install_name))
    print('备份 install 成功。文件名: %s' % old_install_name)
    ssh.close()

def coppy_3_directories(ipp,unm,passd,old_version_path):  ##复制结算行挡板等文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    date_str = str(datetime.datetime.now())[:10]
    old_install_name = 'install_%s' % date_str
    back_dir = os.path.split(old_version_path)[0]
    ssh.exec_command('cd %s/%s; cp -r monsvr ../install'%(back_dir,old_install_name))
    print('monsvr files ok')
    stdin, stdout, stderr = ssh.exec_command('cd %s/%s; ls'%(back_dir,old_install_name))
    tem = stdout.read()
    if 'acsvr_wm' in tem:
        print('acsvr_wm in')
        ssh.exec_command('cd %s/%s; cp -r acsvr_wm ../install'%(back_dir,old_install_name))
        print('acsvr_wm 复制成功 。')
    else:
        print('not found acsvr_wm')
    if 'acsvr_acct' in tem:
        print('acsvr_acct in')
        ssh.exec_command('cd %s/%s; cp -r acsvr_acct ../install'%(back_dir,old_install_name))
        print('acsvr_acct 复制成功 。')
    else:
        print('not found acsvr_acct')
    ssh.close()

def modefy_reg_conf(ipp,unm,passd,ser_list,conf_name,back_dir):  ##修改 conf文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    i = 0
    for ser in ser_list:
        cfg = conf_name[i]
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        print('开始下载 %s'%cfg)
        sftp.get('%s/install/%s/conf/%s'%(back_dir,ser,cfg), '%s'%cfg)
        print('get %s done !'%cfg)
        i += 1
        time.sleep(1)
    ssh.close()
    print('总共有 %s 个服务，共有 %s 个配置cfg文件'%(len(ser_list),len(conf_name)))
    for cfg in conf_name:
        print('开始修改 %s 文件'%cfg)
        with open('%s'%cfg,'r+') as f:
            data = f.readlines()
            mark1 = False
            mark2 = False
            # mark3 = False
            for line in data:
                if '"name"' in line and mark1 == False:
                    line_rownum = data.index(line)
                    nstr = cfg[:-4]
                    new_line = '    "name" : "/ssd/log/%s",\n'%nstr
                    data[line_rownum] = new_line
                    print('更新 %s 文件log参数 成功 。'%cfg)
                    mark1 = True
                if '"grp_cfg"' in line and mark2 == False:
                    line_rownum = data.index(line)
                    new_line = '    "grp_cfg" : "/nfs/conf/reg_group.cfg",\n'
                    data[line_rownum] = new_line
                    print('更新 %s 文件 grp 成功 。'%cfg)
                    mark2 = True
                    break
            if mark1 == True and mark2 == True:
                with open('%s'%cfg,'w+') as f2:
                    for lines in data:
                        f2.write(lines)
                print('更新 %s 文件 2 个配置成功。' % cfg)
print('all log and grp have been modified sucessfully !')

def complex_init(ipp,unm,passd,ser_list,conf_name,back_dir):
    if 'initsvr' in ser_list:
        with open ('initsvr_reg.cfg','r+') as f:
            data = f.readlines()
            for line in data:
                if '"name"' in line:
                    print('find name')
                    num = data.index(line) - 1
                    if '"log" : {' in data[num]:
                        data[num+1] = '        "name":"/ssd/log/initsvr",\n'
                if '"nfs_dir"' in line:
                    num = data.index(line)
                    data[num] = '        "nfs_dir":"/nfs/data"\n'
                if '"comm_db_cfg":{'in line:
                    num = data.index(line) + 1
                    data[num] = '        "username":"PAR_USER",\n'
                    data[num+1] = '        "password":"oracle123!",\n'
                    data[num+2] = '        "dbname":"REG"\n'
                if '"conf/initsvr_ppr_tbl.cfg"' in line:
                    num = data.index(line) + 2
                    data[num] = '        "dbname": "PPR",\n'
                    data[num+1] = '        "password": "oracle123!",\n'
                    data[num+2] = '        "username": "PPR_USER"\n'
                if '"conf/initsvr_par_tbl.cfg"' in line:
                    num = data.index(line) + 2
                    data[num] = '        "dbname": "REG",\n'
                    data[num+1] = '        "password": "oracle123!",\n'
                    data[num+2] = '        "username": "PAR_USER"\n'
                if '"conf/initsvr_reg_tbl.cfg"' in line:
                    num = data.index(line) + 2
                    data[num] = '        "dbname": "REG",\n'
                    data[num+1] = '        "password": "oracle123!",\n'
                    data[num+2] = '        "username": "REG_USER"\n'
                if '"conf/initsvr_par_tra_tbl.cfg"' in line:
                    num = data.index(line) + 2
                    data[num] = '        "dbname": "REG",\n'
                    data[num+1] = '        "password": "oracle123!",\n'
                    data[num+2] = '        "username": "PAR_USER"\n'
        print(data)
        with open('initsvr_reg.cfg','w+') as fw:
            for line in data:
                line.strip()
                print(line)
                fw.write(line)
        print('initsvr_reg.cfg db-connection ok ! ')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put('initsvr_reg.cfg','%s/install/initsvr/conf/initsvr_reg.cfg'%(back_dir))
        print('up init pk')

def manul_acctsvr(ipp,unm,passd,ser_list,conf_name):
    for i in conf_name:
        if 'acctsvr-' in i:
            print('开始处理 %s'%i)
            with open(i,'r+') as fa:
                data = fa.readlines()
                for line in data:
                    if '"data_path"' in line:
                        nu = data.index(line)
                        data[nu] = '"data_path" : "/nfs/data",\n'
                        d2 = nu + 1
                        data[d2] = '"reload_path" : "/nfs/clean",\n'
                        d3 =d2 + 1
                        data[d3] = '"init_cfg_file" : "/nfs/data/init_file_reg.cfg",\n'
                        d4 = d3 + 1
                        data[d4] = '"startwork_cfg" : "/nfs/data/startwork_reg.inf",\n'
                        print('%s 的 nfs 修改完成'%i)
            with open('%s'%i, 'w+') as f2:
                for lines in data:
                    f2.write(lines)

def manul_acsvr_wh(ipp,unm,passd,ser_list,conf_name):
        if 'acsvr_wh' in ser_list:
            with open('acsvr_wh.cfg','r+') as fw:
                data = fw.readlines()
                for line in data:
                    if '"server_ip"' in line:
                        nu = data.index(line)
                        data[nu] = '        "server_ip" : "180.2.35.233",\n'
            with open('acsvr_wh.cfg', 'w+') as f2:
                for lines in data:
                    f2.write(lines)
            print('acsvr_wh 修改 ip 成功')
        else:
            print('服务器 %s  上不存在 acsvr_wh.cfg'%ipp)
def manul_m2d(ipp,unm,passd,ser_list,back_dir,conf_name,old_version_path):
    if 'm2dsvr' in ser_list and 'd2msvr' in ser_list and 'magic_m2dsvr' in ser_list:
        conf_name = ['d2msvr_cmd_tid_map.cfg','reg_m2dsvr_thread.cfg','reg_db_handle.cfg']
        ser_list = ['d2msvr','m2dsvr','magic_m2dsvr']
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipp, username=unm, password=passd)
        i = 0
        for ser in ser_list:
            cfg = conf_name[i]
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            print('准备下载 %s' % cfg)
            sftp.get('%s/install/%s/conf/%s'%(back_dir,ser,cfg),'%s'%cfg)
            print('get digital %s done !' % cfg)
            i += 1
            time.sleep(1)
        ssh.close()
        ls = ['d2msvr_cmd_tid_map.cfg','reg_m2dsvr_thread.cfg']
        for m in ls:
            with open(m,'r+') as fm:
                data= fm.readlines()
                for line in data:
                    if '"orc_inst"' in line:
                        nu = data.index(line)
                        data[nu] = '"orc_inst": "REG",\n'
                        continue
                    if '"user_nm"' in line:
                        nu = data.index(line)
                        data[nu] = '"user_nm": "REG_USER",\n'
                        data[nu+1] = '"user_pwd": "oracle123!"\n'
                        continue
            with open('%s'%m, 'w+') as f2:
                for lines in data:
                    f2.write(lines)
                print('%s connetion oracle cfg ok .'%m)
            mark1 = True

        print('m2d and d2m oracle connetion ok .')
        with open('reg_db_handle.cfg','r+') as fmg:
            data = fmg.readlines()
            for line in data:
                if '"orc_inst"' in line:
                    nu = data.index(line)
                    data[nu] = '"orc_inst": "REG",\n'
                    continue
                if '"user_nm"' in line:
                    nu = data.index(line)
                    data[nu] = '"user_nm": "reg_user",\n'
                    data[nu + 1] = '"user_pwd": "oracle123!"\n'
                    continue
        with open('reg_db_handle.cfg','w+') as f2:
            for lines in data:
                f2.write(lines)
            print('reg_db_handle.cfg 配置修改成功。')
        upload_confed_files(ipp, unm, passd, ser_list, conf_name, old_version_path)
    else:
        print('服务器 %s  上不存在 m2dsvr d2msvr .'%ipp)

def upload_confed_files(ipp,unm,passd,ser_list,conf_name,old_version_path):       ##上传修改完的文件。
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ipp, username=unm, password=passd)
    back_dir = os.path.split(old_version_path)[0]
    i = 0
    for ser in ser_list:
        if ser == 'initsvr':
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
            l = [table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],table.row_values(i)[3],table.row_values(i)[4].split(','),table.row_values(i)[5].split(',')]
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
        old_version_path = sercell[3]
        back_dir = os.path.split(old_version_path)[0]
        print('****************************************** 开始处理 %s 服务器。****************************************'%ipp)
        time.sleep(2)
        rename_isntall(ipp,unm,passd,old_version_path)
        inner(version_ip)
        outer(ipp, unm, passd, old_version_path)
        os.remove('install.tar.gz')
        coppy_3_directories(ipp,unm,passd,old_version_path)
        modefy_reg_conf(ipp,unm,passd,ser_list,conf_name,back_dir)
        complex_init(ipp,unm,passd,ser_list,conf_name,back_dir)
        manul_acctsvr(ipp,unm,passd,ser_list,conf_name)
        manul_acsvr_wh(ipp,unm,passd,ser_list,conf_name)
        manul_m2d(ipp,unm,passd,ser_list,back_dir,conf_name,old_version_path)
        upload_confed_files(ipp,unm,passd,ser_list,conf_name,old_version_path)
        print('############################# 处理 %s 服务器 完成 。###############################' % ipp)
        time.sleep(2)

if __name__ == '__main__':
    big_list = read_excel('reg_conf_233.234.xls')
    main(big_list)

