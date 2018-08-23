# -*-coding:utf-8-*-

import time
import os
import datetime
import re
import paramiko
import xlrd


ps = 'ps -fu $USER'
ps2 = 'ps -ef | grep java'


# 获取全部数据
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
# data_list = get_all_data('yanshou_environment.xlsx')  # 全部源数据


# 查看系统磁盘空间，存储在每天的日志文件中
def check_mem(data):
    '''
    table = xlrd.open_workbook('./jianrong_envir.xlsx')
    data = table.sheet_by_name('Sheet1')
    check_mem(data)
    '''

    if not os.path.exists('./check_mem_log'):
        os.mkdir('./check_mem_log')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    fp = open('./check_mem_log/' + str(datetime.datetime.now())[:10] + '-info.txt', 'w+')

    print('开始收集各服务器空间的当天使用情况....')
    rows = data.nrows
    for r in xrange(0, rows):
        info = data.row_values(r)

        try:
            ssh.connect(hostname=info[0].encode('raw_unicode_escape'), username=info[1].encode('raw_unicode_escape'), password=info[2].encode('raw_unicode_escape'))
            stdin, stdout, stderr = ssh.exec_command('df -h')

            reslut = stdout.read()
            for line in reslut.splitlines():
                if info[3].encode('raw_unicode_escape') in line:
                    used = re.split(r' *', line)[4]
                    # print(used)
                    # print(info['hostname'] + '的已用空间为：' + used)
                    use_int = int(used[:-1])
                    if use_int >= 70:
                        print(info[0].encode('raw_unicode_escape') + '的可用空间不足30%，请及时清理')
            fp.write(info[0].encode('raw_unicode_escape') + '的空间如下：\n' + reslut + '\n\n')
        except Exception as e:
            print(info[0].encode('raw_unicode_escape') + '连接错误')
        finally:
            ssh.close()
    fp.close()
    print('\n***********服务器空间信息收集完毕，具体使用情况请注意到当天日志文件中查看**********')


# 登记初始化
def init_reg(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(100)
        time_total = 0
        cmd = 'cat /ssd/log/initsvr.log'  # 登记初始化检查的日志名称
        while True:
            if time_total > 1800:
                print(host['hostname'] + '登记初始化，抽数据超时，请手动检查')
                exit(1)
            else:
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(cmd)
                result = stdout_1.read()
                if str(host['check']) in result:
                    print('************************* 登记初始化完成 ! **************************')
                    break
                else:
                    t = time.ctime()
                    nowm = t.split(' ')[3]
                    print('*********** time: %s 正在登记初始化中....'%nowm)
                    time.sleep(8)
                    time_total += 8
    except Exception as e:
        print(host['hostname'], '登记初始化失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 交易初始化
def init_tra(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(10)
        cmd = 'cat /ssd/log/initsvr.log'
        time_total = 0

        while True:
            if time_total > 1800:
                print(host['hostname'], '交易初始化超时，请手动检查')
                exit(1)
            else:
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(cmd)
                result = stdout_1.read()
                if str(host['check']) in result:
                    print('************************ 交易初始化完成 ! ********************')
                    break
                else:
                    print('正在交易初始化中....')
                    time.sleep(3)
                    time_total += 3
    except Exception as e:
        print(host['hostname'], '交易初始化失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 指数初始化
def init_tip(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(host['hostname'], username=host['username'],password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(5)
        time_total = 0
        cmd = 'cat /ssd/log/tips_init.log'
        while True:
            if time_total > 1800:
                print(host['hostname'] + '指数初始化超时，请手动检查')
                exit(1)
            else:
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(cmd)
                result = stdout_1.read()
                if str(host['check']) in result:
                    print('********************* 指数初始化成功 ! ********************')
                    break
                else:
                    print('正在指数初始化中....')
                    time.sleep(3)
                    time_total += 3
    except Exception as e:
        print(host['hostname'], '指数初始化失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 启登记ctrlsvr
def run_reg_ctrlsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            # 暂停3s，防止服务没启动
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '*************** 启登记ctrlsvr成功 ! *****************')
            else:
                print(host['hostname'], '启登记ctrlsvr失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启登记ctrlsvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()


# 启登记acctsvr
def run_reg_acctsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '***************** 启登记acctsvr成功 ! ****************')
            else:
                print(host['hostname'], '启登记失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启登记acctsvr失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()


# 启登记其他服务
def run_reg_other(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 遍历启登记其他服务
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            print(host['script_run'])
            # time.sleep(10)
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(5)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '启登记' + host['sername'] + '服务成功....')
            else:
                print(host['hostname'] + '启登记' + host['sername'] + '服务失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启登记', host['sername'], '服务失败，服务器可能连接失败，请手动检查')
            print(e)
        # finally:
        #     ssh.close()


# 启交易keepsvr
def run_tra_keep(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            # 检查流文件
            stdin, stdout, stderr = ssh.exec_command(host['check_flow_path'])
            result = stdout.read()
            # 如果流文件为空，则执行后续操作
            if 0 == int(result):
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(host['script_run'])
                time.sleep(3)
                stdin_2, stdout_2, stderr_2 = ssh.exec_command(ps)
                result_2 = stdout_2.read()
                if str(host['check']) in result_2:
                    print(host['hostname'] + '启交易keepsvr成功....')
                else:
                    print(host['hostname'], '启交易keepsvr失败，请手动检查')
                    exit(1)
            else:
                print(host['hostname'], '启交易keepsvr失败，请检查流文件是否移走....')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启交易keepsvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启交易keepsvr成功')


# 启交易bussvr
def run_tra_bus(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '启交易bussvr成功....')
            else:
                print(host['hostname'], '启交易bussvr失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启交易bussvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启交易bussvr成功')


# 启交易服务
def run_tra(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    traser_len = len(hostinfo)
    print('servernum %d'%traser_len)
    # print(hostinfo)
    time.sleep(5)
    for host in hostinfo:
        print('ready to start server: %s on %s '%(host['script_run'],host['hostname']))
        # try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(8)
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
        result = stdout_1.read()
        time.sleep(1)
        if str(host['check']) in result:
            print(host['hostname'] + host['sername'] + ' success !')
            time.sleep(5)
        else:
            print(host['hostname'] + ' 启交易 '  + host['sername'] + '服务失败，请手动检查')
            exit(1)
        # except Exception as e:
        #     print(host['hostname'], '启交易', host['sername'], '失败，服务器可能连接失败')
        #     print(e)
        # finally:
        #     ssh.close()
    print('启交易其他服务成功 ！')


# 重启黄马甲审计日志
def restart_yellow_log(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(ps)
        result = stdout.read()

        # 如果进程存在，杀掉后执行后续操作
        if str(host['check']) in result:
            for line in result:
                if str(host['check']) in line:
                    pid = str(re.split(' *', line)[1].decode('raw_unicode_escape'))
                    cmd = 'kill -9 ' + pid + '; ps –fu $USER'
                    stdin_1, stdout_1, stderr_1 = ssh.exec_command(cmd)
                    result_1 = stdout_1.read()
                    if str(host['check']) in result_1:
                        print(host['hostname'], '重启黄马甲，杀进程失败，请手动检查')
                        exit(1)
                    else:
                        print(host['hostname'], '重启黄马甲，杀进程成功，正在重启中....')

        # 重启黄马甲
        # cmd2 = 'cd /home/yellow/ppr_auditlog/interface/shell; nohup ./service.sh &'
        # cmd2 = 'cd /home/yellow/ppr_auditlog/interface/shell; nohup ./service.sh &'
        cmd2 = host['script_run']
        stdin_2, stdout_2, stderr_2 = ssh.exec_command(cmd2)
        time.sleep(10)
        stdin_3, stdout_3, stderr_3 = ssh.exec_command(ps)
        result_3 = stdout_3.read()
        if str(host['check']) in result_3:
            print(host['hostname'], '重启黄马甲审计日志成功')
        else:
            print(host['hostname'], '重启黄马甲审计日志失败，请手动检查')
            exit(1)
    except Exception as e:
        print(host['hostname'], '重启黄马甲失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 启仓储
def run_wh(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(5)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '启仓储' + host['sername'] + '服务成功....')
            else:
                print(host['hostname'], '启仓储', host['sername'], '服务失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启仓储', host['sername'], '服务失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
        # print('启仓储成功')


# 启ETF
def run_etf(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + ' 启ETF ' + host['sername'] + ' 成功....')
            else:
                print(host['hostname'] + '启ETF' + host['sername'] + '失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启ETF', host['sername'], '失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启ETF成功')


# 启风控
def run_risk(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sgw = []  # 获取到sgw服务所在的服务器信息
    engine = []  # 获取engine
    filemanager_riskacsvr = []  # 获取filemanage和riskacsvr
    for host in hostinfo:
        if re.findall('risk_sgw_1', str(host['sername'])):
            sgw.append(host)
        elif re.findall('risk_engine', str(host['sername'])):
            engine.append(host)
        elif re.findall('risk_riskacsvr', str(host['sername'])):
            filemanager_riskacsvr.append(host)
        elif re.findall('risk_fileManage', str(host['sername'])):
            filemanager_riskacsvr.append(host)
    # sgw = sgw.reverse()
    # print(sgw)
    # new_sgw = []
    # new_sgw.append(sgw[1])
    # new_sgw.append(sgw[0])
    # print(new_sgw)
    # time.sleep(3)
    # 启risk和filemanage
    # print(filemanager_riskacsvr)
    time.sleep(20)
    for each in filemanager_riskacsvr:
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_5, stdout_5, stderr_5 = ssh.exec_command(each['script_run'])
        time.sleep(10)
        stdin_6, stdout_6, stderr_6 = ssh.exec_command(ps)
        result_6 = stdout_6.read()
        if str(each['check']) in result_6 and filemanager_riskacsvr.index(each)==0:
            print('*******************启动风控riskacsvr成功 ！*********************')
        elif str(each['check']) in result_6 :
            print('*******************启动风控filemange 成功 ！*********************')
            mark =1
        else:
            print('启动风控filemanage 和 riskac 失败！')
            exit(1)
    # 启风控前置：两个sgw
    if mark == 1:
        print('准备启动sgw')
        for each in sgw:
            # try:
            # print("ready to start follw!")
            # print(each['script_run'])
            ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
            stdin, stdout, stderr = ssh.exec_command(each['script_run'])
            print('启风控前置服务中....')
            time.sleep(15)
            # except Exception as e:
            #     print(each['hostname'], '启风控前置', each['sername'], '失败，服务器可能连接失败')
        # 启完两个风控之后检查
        print(each['hostname'])
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
        result = stdout_1.read()
        if len(re.findall('./sgw start', result)) == 2:
            print('****************** 启风控前置sgw成功 ! ***************')
            ssh.close()
            mark2 =1
        else:
            print(sgw[0]['hostname']+'启风控前置服务失败，请手动检查')
            exit(1)
    # 启风控引擎
    if mark2 == 1:
        print('准备启动引擎')
        each = engine[0]
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_2, stdout_2, stderr_2 = ssh.exec_command(each['script_run'])
        print('..........启风控引擎中.......')
        time.sleep(10)
        stdin_3, stdout_3, stderr_3 = ssh.exec_command(ps2)
        result_3 = stdout_3.read()
        if str(each['check']) in result_3:
            print('************** 启风控引擎成功 !****************')
            ssh.close()
        else:
            print('启风控引擎失败，请手动检查')
            exit(1)
    if mark == 1 and mark2 == 1:
        print('************* 启风控服务成功 ！ ****************')
    else:
        print('启风控服务失败！')



# 重启190运维监控平台
def restart_190_monitor(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
        time.sleep(2)
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(host['script_run'])
        print('重启运维监控服务平台完成')
    except Exception as e:
        print(host['hostname'], '重启运维监控服务平台失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()

# 启动monitor服务
def run_monitor(hostinfo):
    for host in hostinfo:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(5)
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
        result = stdout_1.read()
        time.sleep(10)
        if 'tail -f /nfs/monitor' in result:
            print(host['hostname'] + 'start ok!')
        else:
            print(host['hostname'] + 'start faild!!!!!!!!!!')



# 启数据同步
def run_sync(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(15)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '启数据同步', host['sername'], '成功....')
            else:
                print(host['hostname'], '启数据同步', host['sername'], '失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启数据同步', host['sername'], '失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启数据同步成功')
    # 启完数据同步之后，启监控服务
    # run_monitor()
    # 重启190运维监控平台
    # restart_190_monitor()

# 停交易服务
def stop_tra(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停交易', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停交易', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停交易', host['sername'], '失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('停交易服务成功')

# 清算预导出
def clean_pre(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(60)
        time_total = 0
        today = ''.join(str(datetime.datetime.now())[:10].split('-')) + '.*'  # 获取当前日期，检查预导出日志文件
        while True:
            if time_total > 1800:
                print(host['hostname'], '清算预导出超时，请手动检查')
                exit(1)
            else:
                # 检查预导出日志文件
                stdin_1, stdout_1, stderr_1 = ssh.exec_command('cd /home/clean/code/pre/log; ls')
                result = stdout_1.read()
                need_log = re.findall(today, result)[-1]  # 获取当前交易日最新的日志
                temp = 'cat ' + need_log  # 查看当前交易日最新日志
                stdin_2, stdout_2, stderr_2 = ssh.exec_command('cd /home/clean/code/pre/log; ' + temp)
                result_2 = stdout_2.read()
                if str(host['check']) in result_2:
                    print('清算预导出成功')
                    break
                else:
                    print('正在清算预导出...')
                    time.sleep(3)
                    time_total += 3
    except Exception as e:
        print(host['hostname'], '清算预导出失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 日终登账前预导出
def day_clean_pre(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostinfo[0]
    try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        print('conn ok !')
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        print('cmd run ok!')
        time.sleep(5)
        time_total = 0
        # cmd = 'time=$(date "+%Y%m%d"); cd data/input/$time/; ls | wc -l'
        # cmd = 'time=$(date "+%Y%m%d"); cd data/input/$time/; ls -l|grep "^-"| wc -l'

        # cmd = 'time=$(date "+%Y%m%d"); cd data/input/%s/; ls -l|grep "^-"| wc -l'%($time)

        while True:
            if time_total > 1800:
                print(host['hostname'], '日终登账前预导出超时，请手动检查')
                exit(1)
            else:
                print('ready to check num!')
                stdin_1, stdout_1, stderr_1 = ssh.exec_command('time=$(date "+%Y%m%d"); cd data/input/$time/; ls -l|grep "^-"| wc -l')
                result = stdout_1.read()
                print('check ok')
                print(result)
                time.sleep(20)
                if int(host['check']) == int(result):
                    print('日终登账前预导出完成')
                    break
                else:
                    print('正在进行日终登账前预导出....')
                    time.sleep(5)
                    time_total += 5
    except Exception as e:
        print(host['hostname'], '日终登账前预导出失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


# 停登记
def stop_reg(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停登记服务', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停登记服务', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停登记服务', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()


# 备份日志通用函数
def bak_log(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        if str(host['bak_flag']) == '1.0':
            try:
                ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
                stdin, stdout, stderr = ssh.exec_command('./backup.sh &')  # 指定文件名
                time.sleep(30)
                # 检查普通日志备份
                cmd = str(host['check_bak'])
                time_total = 0
                while True:
                    if time_total > 1800:
                        print(host['hostname'], '备份日志超时，请手动检查')
                        exit(1)
                    else:
                        stdin_1, stdout_1, stderr_1 = ssh.exec_command(cmd)
                        result = stdout_1.read()
                        if 0 == int(result):
                            # 检查流文件备份
                            if str(host['check_flow_file']) == '1.0':
                                cmd2 = str(host['flow_file_path'])
                                time_total2 = 0
                                while True:
                                    if time_total2 > 1800:
                                        print(host['hostname'], '备份流文件超时，请手动检查')
                                        exit(1)
                                    else:
                                        stdin_2, stdout_2, stderr_2 = ssh.exec_command(cmd2)
                                        result2 = stdout_2.read()
                                        if 0 == int(result2):
                                            print(host['hostname'], '备份流文件成功....')
                                            break
                                        else:
                                            print('正在备份流文件中....')
                                            time.sleep(3)
                                            time_total2 += 3
                            print(host['hostname'], '备份日志成功')
                            break
                        else:
                            print('正在备份日志中....')
                            time.sleep(5)
                            time_total + 5
            except Exception as e:
                print(host['hostname'], '备份日志失败，服务器可能连接失败，请手动检查')
                print(e)
            finally:
                ssh.close()


# 停ETF
def stop_etf(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停ETF成功')


# 停风控
def stop_fisk(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sgw = []  # 获取到sgw服务所在的服务器信息
    engine = []  # 获取engine
    redis = []  # 清redis
    filemanager_riskacsvr = []  # 获取filemanage和riskacsvr
    for host in hostinfo:
        if re.findall('risk_sgw_1', str(host['sername'])):
            sgw.append(host)
        elif re.findall('risk_engine', str(host['sername'])):
            engine.append(host)
        elif re.findall('risk_redis', str(host['sername'])):
            redis.append(host)
        elif re.findall('risk_fileManage', str(host['sername'])) or re.findall('risk_riskacsvr', str(host['sername'])):
            filemanager_riskacsvr.append(host)

    # 停risk和filemanage
    for each in filemanager_riskacsvr:
        # try:
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_5, stdout_5, stderr_5 = ssh.exec_command(each['script_stop'])
        time.sleep(3)
        stdin_6, stdout_6, stderr_6 = ssh.exec_command(ps)
        result_6 = stdout_6.read()
        if str(each['check']) in result_6:
            print(each['hostname'], '停', each['sername'], '服务失败，请手动检查')
            exit(1)
        else:
            print(each['hostname'] + "stop riskac successfully!")

    print(each['hostname'] + "stop filemanage successfully!")
    print('******************* 停风控 filemanage 成功 !********************')

    for each in sgw:
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        # print('cmd %s'%each['script_stop'])
        time.sleep(30)
        # stdin, stdout, stderr = ssh.exec_command(each['script_stop'])
        stdin, stdout, stderr = ssh.exec_command(each['script_stop'])
        print('停风控前置服务中....')
        time.sleep(20)
        # 停完两个风控之后检查
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
        result = stdout_1.read()
        # print(result)
        time.sleep(30)
        if './sgw start' in result or './sgw' in result:
            print('停风控前置失败，请手动检查')
            exit(1)
        else:
            print('******************* 停风控前置服务sgw成功 !********************')
            ssh.close()

    # 停风控引擎
    each = engine[0]
    try:
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_2, stdout_2, stderr_2 = ssh.exec_command(each['script_stop'])
        print('停风控引擎中....')
        time.sleep(5)
        stdin_3, stdout_3, stderr_3 = ssh.exec_command(ps2)
        result_3 = stdout_3.read()
        if str(each['check']) in result_3:
            print('停风控引擎失败，请手动检查')
            exit(1)
        else:
            print('***************** 停风控引擎成功 !********************')
            ssh.close()
    except Exception as e:
        print('停风控引擎失败，服务器可能连接失败')
        print(e)


    # 清redis
    each = redis[0]
    try:
        ssh.connect(hostname=each['hostname'], username=each['username'], password=each['password'])
        stdin_4, stdout_4, stderr_4 = ssh.exec_command(each['script_stop'])
        # temp_re = stdout_4.read()
        time.sleep(260)
        if str(each['check']) in stdout_4.read():
            # print(each['hostname'], '清redis成功....')
            print('***************** 清redis成功 !**********************')
        else:
            print('清redis超时，请手动检查')
            exit(1)
    except Exception as e:
        print('清redis失败，服务器可能连接失败')
        print(e)
    finally:
        ssh.close()


#停灾备交易keepsvr
def stop_zaibei_tra_keep(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停灾备交易keepsvr成功')


#停灾备交易bussvr
def stop_zaibei_tra_bus(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停灾备交易bussvr成功')


#停灾备交易其他
def stop_zaibei_tra_other(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停灾备交易其他成功')


# 启灾备交易keepsvr
def run_zaibei_tra_keep(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            # 检查流文件
            stdin, stdout, stderr = ssh.exec_command(host['check_flow_path'])
            result = stdout.read()
            # 如果流文件为空，则执行后续操作
            if 0 == int(result):
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(host['script_run'])
                time.sleep(3)
                stdin_2, stdout_2, stderr_2 = ssh.exec_command(ps)
                result_2 = stdout_2.read()
                if str(host['check']) in result_2:
                    print(host['hostname'] + '启灾备交易keepsvr成功....')
                else:
                    print(host['hostname'], '启灾备交易keepsvr失败，请手动检查')
                    exit(1)
            else:
                print(host['hostname'], '启灾备交易keepsvr失败，请检查流文件是否移走....')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启灾备交易keepsvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启灾备交易keepsvr成功')


# 启灾备交易bussvr
def run_zaibei_tra_bus(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '启灾备交易bussvr成功....')
            else:
                print(host['hostname'], '启灾备交易bussvr失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启灾备交易bussvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()
    print('启灾备交易bussvr成功')


# 启灾备交易其他服务
def run_zaibei_tra_other(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    traser_len = len(hostinfo)
    print('servernum %d'%traser_len)
    # print(hostinfo)
    time.sleep(5)
    for host in hostinfo:
        print('ready to start server: %s on %s '%(host['script_run'],host['hostname']))
        # try:
        ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command(host['script_run'])
        time.sleep(8)
        stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
        result = stdout_1.read()
        time.sleep(1)
        if str(host['check']) in result:
            print(host['hostname'] + host['sername'] + ' success !')
            time.sleep(5)
        else:
            print(host['hostname'] + ' 启灾备交易其他 '  + host['sername'] + '服务失败，请手动检查')
            exit(1)
        # except Exception as e:
        #     print(host['hostname'], '启交易', host['sername'], '失败，服务器可能连接失败')
        #     print(e)
        # finally:
        #     ssh.close()
    print('启灾备交易其他服务成功 ！')


#停灾备登记ctrlsvr
def stop_zaibei_reg_ctrlsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停灾备登记ctrlsvr成功')


#停灾备登记acctsvr
def stop_zaibei_reg_acctsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()
    print('停灾备登记acctsvr成功')


# 停灾备登记其他服务
def stop_zaibei_reg_other(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_stop'])
            time.sleep(2)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'], '停登记其他服务', host['sername'], '失败，请手动检查')
                exit(1)
            else:
                print(host['hostname'], '停登记其他服务', host['sername'], '成功....')
        except Exception as e:
            print(host['hostname'], '停登记其他服务', host['sername'], '失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()

# 启灾备登记ctrlsvr
def run_zaibei_reg_ctrlsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            # 检查流文件
            stdin1, stdout1, stderr1 = ssh.exec_command(host['check_flow_path'])
            result = stdout1.read()
            # 如果流文件为空，则执行后续操作
            if 0 == int(result):
                stdin, stdout, stderr = ssh.exec_command(host['script_run'])
                # 暂停3s，防止服务没启动
                time.sleep(3)
                stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
                result = stdout_1.read()
                if str(host['check']) in result:
                    print(host['hostname'] + '*************** 启灾备登记ctrlsvr成功 ! *****************')
                else:
                    print(host['hostname'], '启灾备登记ctrlsvr失败，请手动检查')
                    exit(1)
        except Exception as e:
            print(host['hostname'], '启灾备登记ctrlsvr失败，服务器可能连接失败')
            print(e)
        finally:
            ssh.close()


# 启灾备登记acctsvr
def run_zaibei_reg_acctsvr(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(3)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '***************** 启灾备登记acctsvr成功 ! ****************')
            else:
                print(host['hostname'], '启灾备登记失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启灾备登记acctsvr失败，服务器可能连接失败，请手动检查')
            print(e)
        finally:
            ssh.close()


# 启灾备登记其他服务
def run_zaibei_reg_other(hostinfo):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 遍历启登记其他服务
    for host in hostinfo:
        try:
            ssh.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
            print(host['script_run'])
            # time.sleep(10)
            stdin, stdout, stderr = ssh.exec_command(host['script_run'])
            time.sleep(5)
            stdin_1, stdout_1, stderr_1 = ssh.exec_command(ps)
            result = stdout_1.read()
            if str(host['check']) in result:
                print(host['hostname'] + '启灾备登记' + host['sername'] + '服务成功....')
            else:
                print(host['hostname'] + '启灾备登记' + host['sername'] + '服务失败，请手动检查')
                exit(1)
        except Exception as e:
            print(host['hostname'], '启灾备登记', host['sername'], '服务失败，服务器可能连接失败，请手动检查')
            print(e)
        # finally:
        #     ssh.close()

# 根据提供的服务名列表获取到服务器信息
def get_need_hostinfo(data_list, search_list):
    res = list(filter(lambda data: data if str(data.keys()[0]) in search_list else False, data_list))
    need_list = []
    for host in res:
        need_list.append(host.values()[0])
    return need_list


# 单步执行操作选项
def self_choice():
    while True:
        print('\n根据下面的提示选择操作\n')
        print('01)停交易服务                      02)备份交易日志               03)清算预导出')
        print('04)日终登账前预导出                05)停登记系统                 06)备份登记日志')
        print('07)停ETF系统                       08)停风控系统                 09)备份风控日志')
        print('10)登记初始化                      11)交易初始化                 12)指数初始化')
        print('13)启动登记ctrlsvr                 14)启动登记acctsvr            15)启动登记其他服务')
        print('16)启动交易keepsvr                 17)启动交易bussvr             18)启动交易其他服务')
        print('19)重启黄马甲审计日志              20)启动仓储                   21)启动ETF系统')
        print('22)启动风控系统                    23)启动数据同步               24)启动监控服务')
        print('25)停灾备交易keepsvr               26)停灾备交易bussvr           27)停灾备交易其他服务')
        print('28)启动灾备交易keepsvr                29)启动灾备交易bussvr           30)启动灾备交易其他服务')
        print('31)停灾备登记ctrlsvr               32)停灾备登记acctsvr           33)停灾备登记其他服务')
        print('34)启动灾备登记ctrlsvr             35)启动灾备登记acctsvr         36)启动灾备登记其他服务')
        print('37)启动灾备交易同步服务syncsvr          38)启动灾备登记同步服务syncsvr         ')
        print('99)回到上一级操作选项\n\n')

        choice = raw_input('请输入操作选项：')

        if choice == '1' or choice == '01':
            choice_again = raw_input('确认黄马甲完成收盘收市，国际版完成清算，回车进行 停交易服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['trans_mem2dbsvr', 'quot_mem2dbsvr', 'bussvr-A',
                                                     'keepsvr-A', 'matchsvr-A', 'qsvr-A', 'quotaacsvr-A', 'bridgesvr-A', 'acsvr101', 'acsvr102', 'intacsvr-A', 'qrysvr-A',
                                                     'keepsvr-B', 'matchsvr-B', 'qsvr-B', 'quotaacsvr-B', 'bridgesvr-B', 'acsvr104', 'intacsvr-B', 'qrysvr-B',
                                                     'bussvr-B',
                                                     ])
            # for i in hostinfo:
            #     print(i)
            stop_tra(hostinfo)
            continue
        elif choice == '2' or choice == '02':
            choice_again = raw_input('回车进行 备份交易日志 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['bussvr-A', 'keepsvr-A', 'keepsvr-B', 'bussvr-B'])
            bak_log(hostinfo)
            continue
        elif choice == '3' or choice == '03':
            choice_again = raw_input('回车进行 清算预导出 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['clean_pre'])
            # print(hostinfo)
            clean_pre(hostinfo)
            continue
        elif choice == '4' or choice == '04':
            choice_again = raw_input('确认询价客户端完成复核状态维护，回车进行 日终登账前预导出 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['day_clean_pre'])
            # print(hostinfo)
            day_clean_pre(hostinfo)
            continue
        elif choice == '5' or choice == '05':
            choice_again = raw_input('确认业服完成清算->日终登账、国际版清算->初始化->停服务，回车进行 停登记服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['ctrlsvr-A', 'acctsvr-A', 'acsvr_web', 'acsvr_qury-A', 'acsvr_shau-A',
                                                     'acsvr_trad-A', 'acsvr_int-A', 'acsvr_etf-A', 'bridgesvr_reg-A', 'magic_m2d',
                                                     'acsvr_acct', 'd2msvr', 'm2dsvr', 'wh-main', 'wh-watch',
                                                     'ctrlsvr-B', 'acctsvr-B', 'acsvr_wh', 'acsvr_qury-B', 'acsvr_shau-B',
                                                     'acsvr_trad-B', 'acsvr_int-B', 'acsvr_etf-B', 'bridgesvr_reg-B', 'acsvr_wm','acsvr_bank'
                                                     ])
            stop_reg(hostinfo)
            continue
        elif choice == '6' or choice == '06':
            choice_again = raw_input('回车进行 备份登记日志 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['ctrlsvr-A', 'acctsvr-B'])
            bak_log(hostinfo)
            continue
        elif choice == '7' or choice == '07':
            choice_again = raw_input('回车进行 停ETF系统 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['etfsvr', 'etfacsvr', 'w2e_acsvr', 'etfsseacsvr', 'etfszseacsvr'])
            stop_etf(hostinfo)
            continue
        elif choice == '8' or choice == '08':
            choice_again = raw_input('回车进行 停风控系统 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            # hostinfo = get_need_hostinfo(data_list, ['risk_sgw_1', 'risk_sgw_2', 'risk_engine', 'risk_redis',
            #                                          'risk_fileManage',
            #                                          ])
            hostinfo = get_need_hostinfo(data_list, ['risk_sgw_1','risk_engine', 'risk_redis',
                                                     'risk_fileManage',
                                                     ])
            stop_fisk(hostinfo)
            continue
        elif choice == '9' or choice == '09':
            choice_again = raw_input('回车进行 备份风控日志 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['risk_riskacsvr'])
            # print(hostinfo)
            bak_log(hostinfo)
            continue
        elif choice == '10':
            choice_again = raw_input('确认业服完成运维初始化，回车进行 登记初始化 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['init_reg'])
            # print(hostinfo)
            init_reg(hostinfo)
            continue
        elif choice == '11':
            choice_again = raw_input('回车进行 交易初始化 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['init_tra'])
            # print(hostinfo)
            init_tra(hostinfo)
            continue
        elif choice == '12':
            choice_again = raw_input('回车进行 指数初始化 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['init_tip'])
            init_tip(hostinfo)
            continue
        elif choice == '13':
            choice_again = raw_input('回车进行 启动登记ctrlsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['ctrlsvr-A', 'ctrlsvr-B'])
            run_reg_ctrlsvr(hostinfo)
            continue
        elif choice == '14':
            choice_again = raw_input('回车进行 启动登记acctsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['acctsvr-A', 'acctsvr-B'])
            run_reg_acctsvr(hostinfo)
            continue
        elif choice == '15':
            choice_again = raw_input('回车进行 启动登记其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['bridgesvr_reg-A', 'acsvr_etf-A', 'acsvr_int-A', 'acsvr_qury-A',
                                                     'acsvr_shau-A', 'acsvr_trad-A', 'acsvr_web', 'acsvr_acct',
                                                     'acsvr_wh','acsvr_bank', 'bridgesvr_reg-B', 'acsvr_etf-B', 'acsvr_int-B',
                                                     'acsvr_qury-B', 'acsvr_shau-B', 'acsvr_trad-B', 'acsvr_wm'
                                                     ])
            run_reg_other(hostinfo)
            continue
        elif choice == '16':
            choice_again = raw_input('回车进行 启动交易keepsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['keepsvr-A', 'keepsvr-B'])
            run_tra_keep(hostinfo)
            continue
        elif choice == '17':
            choice_again = raw_input('回车进行 启动交易bussvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['bussvr-A', 'bussvr-B'])
            run_tra_bus(hostinfo)
            continue
        elif choice == '18':
            choice_again = raw_input('回车进行 启动交易其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['matchsvr-A', 'qsvr-A', 'quotaacsvr-A', 'bridgesvr-A', 'acsvrA','qrysvr-A','acsvrB','matchsvr-B','qsvr-B','bridgesvr-B','qrysvr-B','intacsvr-A'])
            run_tra(hostinfo)
            continue
        elif choice == '19':
            choice_again = raw_input('确认业服开工，确认国际版启动服务，回车进行 重启黄马甲审计日志 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['yellow_log'])
            restart_yellow_log(hostinfo)
            continue
        elif choice == '20':
            choice_again = raw_input('确认已启动黄马甲检查日期状态，回车进行 启动仓储服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['wh-main', 'wh-watch'])
            run_wh(hostinfo)
            continue
        elif choice == '21':
            choice_again = raw_input('回车进行 启动ETF系统 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['etfsvr', 'etfacsvr', 'etfsseacsvr', 'etfszseacsvr', 'w2e_acsvr','shield_sse','shield_szse'])
            run_etf(hostinfo)
            continue
        elif choice == '22':
            choice_again = raw_input('回车进行 启动风控系统 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            # hostinfo = get_need_hostinfo(data_list,['risk_sgw_1', 'risk_sgw_2', 'risk_engine','risk_riskacsvr','risk_fileManage'])
            hostinfo = get_need_hostinfo(data_list,['risk_sgw_1','risk_engine','risk_fileManage','risk_riskacsvr'])

            run_risk(hostinfo)
            continue
        elif choice == '23':
            choice_again = raw_input('回车进行 启动数据同步服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['d2msvr','m2dsvr','magic_m2d','trans_mem2dbsvr', 'quot_mem2dbsvr'])
            run_sync(hostinfo)
            continue
        elif choice == '24':
            choice_again = raw_input('回车进行 启动监控服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['reg229moni', 'reg20moni', 'moni95', 'moni97', 'moni99','moni200','moni228','moni31','moni32'])
            # hostinfo = get_need_hostinfo(data_list,['reg20moni', 'moni95', 'moni97', 'moni99','moni200','moni228'])

            print('开始启动所有监控服务！')
            run_monitor(hostinfo)
            print('启动所有监控服务完成！！')
            continue
        elif choice == '25':
            choice_again = raw_input('回车进行 停止灾备交易keepsvr服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['zaibei_keepsvr-A', 'zaibei_keepsvr-B'])
            # hostinfo = get_need_hostinfo(data_list,['reg20moni', 'moni95', 'moni97', 'moni99','moni200','moni228'])

            print('开始 停止灾备交易keepsvr服务！')
            stop_zaibei_tra_keep(hostinfo)
            print('停止灾备交易keepsvr服务完成！')
            continue
        elif choice == '26':
            choice_again = raw_input('回车进行 停止灾备交易bussvr服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['zaibei_bussvr-A', 'zaibei_bussvr-B'])

            print('开始 停止灾备交易bussvr服务！')
            stop_zaibei_tra_bus(hostinfo)
            print('停止灾备交易bussvr服务完成！')
            continue
        elif choice == '27':
            choice_again = raw_input('回车进行 停止灾备交易其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['zaibei_matchsvr-A', 'zaibei_bridgesvr_tra-A', 'zaibei_intacsvr',
                                                    'zaibei_quotaacsvr', 'zaibei_qsvrA', 'zaibei_acsvrA', 'zaibei_qrysvr-A',
                                                    'zaibei_matchsvr-B', 'zaibei_bridgesvr_tra-B', 'zaibei_qrysvr-B',
                                                    'zaibei_acsvrB', 'zaibei_qsvrB'
                                                    ])
            print('开始 停止灾备交易其他服务！')
            stop_zaibei_tra_other(hostinfo)
            print('停止灾备交易其他服务完成！')
            continue
        elif choice == '28':
            choice_again = raw_input('回车进行 启动灾备交易keepsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_keepsvr-A', 'zaibei_keepsvr-B'])
            run_zaibei_tra_keep(hostinfo)
            continue
        elif choice == '29':
            choice_again = raw_input('回车进行 启动灾备交易bussvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_bussvr-A', 'zaibei_bussvr-B'])
            run_zaibei_tra_bus(hostinfo)
            continue
        elif choice == '30':
            choice_again = raw_input('回车进行 启动灾备交易其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_matchsvr-A', 'zaibei_bridgesvr_tra-A', 'zaibei_intacsvr',
                                                    'zaibei_quotaacsvr', 'zaibei_qsvrA', 'zaibei_acsvrA', 'zaibei_qrysvr-A',
                                                    'zaibei_matchsvr-B', 'zaibei_bridgesvr_tra-B', 'zaibei_qrysvr-B',
                                                    'zaibei_acsvrB', 'zaibei_qsvrB'])
            run_zaibei_tra_other(hostinfo)
            continue
        elif choice == '31':
            choice_again = raw_input('回车进行 停止灾备登记ctrlsvr服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['zaibei_ctrlsvr-A', 'zaibei_ctrlsvr-B'])
            # hostinfo = get_need_hostinfo(data_list,['reg20moni', 'moni95', 'moni97', 'moni99','moni200','moni228'])

            print('开始 停止灾备登记ctrlsvr服务！')
            stop_zaibei_reg_ctrlsvr(hostinfo)
            print('停止灾备登记ctrlsvr服务完成！')
            continue
        elif choice == '32':
            choice_again = raw_input('回车进行 停止灾备登记acctsvr服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list,['zaibei_acctsvr-A', 'zaibei_acctsvr-B'])
            # hostinfo = get_need_hostinfo(data_list,['reg20moni', 'moni95', 'moni97', 'moni99','moni200','moni228'])

            print('开始 停止灾备登记acctsvr服务！')
            stop_zaibei_reg_acctsvr(hostinfo)
            print('停止灾备登记acctsvr服务完成！')
            continue
        elif choice == '33':
            choice_again = raw_input('回车进行 停止灾备登记其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_acsvr_acct', 'zaibei_acsvr_bank', 'zaibei_acsvr_web',
                                                     'zaibei_acsvr_wh', 'zaibei_acsvr_wm', 'zaibei_acsvr_etf-A',
                                                     'zaibei_acsvr_int-A', 'zaibei_acsvr_qury-A', 'zaibei_acsvr_shau-A',
                                                     'zaibei_acsvr_trad-A', 'zaibei_bridgesvr-A', 'zaibei_acsvr_etf-B',
                                                     'zaibei_acsvr_int-B', 'zaibei_acsvr_qury-B', 'zaibei_acsvr_shau-B',
                                                     'zaibei_acsvr_trad-B', 'zaibei_bridgesvr-B'
                                                     ])
            stop_zaibei_reg_other(hostinfo)
            continue
        elif choice == '34':
            choice_again = raw_input('回车进行 启动灾备登记ctrlsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_ctrlsvr-A', 'zaibei_ctrlsvr-B'])
            run_reg_ctrlsvr(hostinfo)
            continue
        elif choice == '35':
            choice_again = raw_input('回车进行 启动灾备登记acctsvr [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_acctsvr-A', 'zaibei_acctsvr-B'])
            run_zaibei_reg_acctsvr(hostinfo)
            continue
        elif choice == '36':
            choice_again = raw_input('回车进行 启动灾备登记其他服务 [99回到选择菜单]....')
            if choice_again == '99':
                continue
            hostinfo = get_need_hostinfo(data_list, ['zaibei_acsvr_acct', 'zaibei_acsvr_bank', 'zaibei_acsvr_web',
                                                     'zaibei_acsvr_wh', 'zaibei_acsvr_wm', 'zaibei_acsvr_etf-A',
                                                     'zaibei_acsvr_int-A', 'zaibei_acsvr_qury-A', 'zaibei_acsvr_shau-A',
                                                     'zaibei_acsvr_trad-A', 'zaibei_bridgesvr-A', 'zaibei_acsvr_etf-B',
                                                     'zaibei_acsvr_int-B', 'zaibei_acsvr_qury-B', 'zaibei_acsvr_shau-B',
                                                     'zaibei_acsvr_trad-B', 'zaibei_bridgesvr-B'
                                                     ])
            run_zaibei_reg_other(hostinfo)
            continue
        elif choice == '99':
            break


# 操作选项
def choice_op():
    while True:
        print('根据下面的提示选择操作\n')
        print('1)启动验收服务器                      3)自定义操作')
        print('2)停止验收服务器                      90)查询系统磁盘空间')
        print('99)退出\n\n')

        choice = raw_input('请输入操作选项：')

        if choice == '1':
            print('启动验收服务器')
            continue
        elif choice == '2':
            print('停止验收服务器')
            continue
        elif choice == '90':
            print('查询系统磁盘空间')
            continue
        elif choice == '99':
            print('正在退出....')
            break
        elif choice == '3':
            self_choice()
            continue

if __name__ == '__main__':
    data_list = get_all_data('liantiao-0820.xls')  # 全部源数据
    choice_op()
