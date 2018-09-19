# -*- coding:utf-8 -*-


#更改交易前置acsvr
def change_tra_acsvr(target_txt, target_txt1):
    if target_txt1 == '' and target_txt == '':
        com_txt = '/home/reg1/install/acsvr_bank/conf/acsvr_bank.cfg'
        target_txt = 'd:\\sshclient\\acsvr_bank.cfg'
        target_txt1 = 'd:\\sshclient\\acsvr_bank1.cfg'
        txt = '#北京银行       204.78.79.3     16800'\
           "{"\
               '"end_id" : "01170000",'\
               '"ip" : "180.2.31.299",'\
               '"port" :18888'\
           '},'
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


import datetime
if __name__ == '__main__':
    # change_tra_acsvr('d:\\sshclient\\quotaacsvr.cfg', 'd:\\sshclient\\quotaacsvr1.cfg')
    change_tra_acsvr('','')
    # print datetime.date(year=2018, month=8, day=22)
    # tar = 'acsvr1.cfg' + datetime.datetime.now().strftime('%Y%m%d')
    # print(type(datetime.datetime.now().strftime('%Y%m%d')))
    # print(tar)