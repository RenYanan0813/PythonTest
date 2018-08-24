# -*- coding:utf-8 -*-

import re
import xlrd

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
            wh_config = raw_input("输入  ，(如 /home/zhiban/guoqing/20180822/wh/):")
            # wh_config.new_wh['new_wh_file'] = raw_input("输入最新仓储核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            # cangchu()
            print "---------------完成 更换更改交易前置acsvr 操作-----------------"
        elif com == '8':
            flag = False
        else:
            print "没有该命令，请重新输入:"


if __name__ == '__main__':
    data_list = get_all_data('liantiao-0824.xls')  # 全部源数据
    main()