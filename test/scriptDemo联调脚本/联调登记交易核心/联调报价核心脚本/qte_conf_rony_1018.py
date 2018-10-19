# -*- coding:utf-8 -*-


import os
import qte_config
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


def main():
    flag = True
    while flag:
        print "\n根据下面提示输入指令:\n"
        com = raw_input(" 1) 更换报价 34.23 的核心服务          2) 更换报价 34.24 的核心服务 \n"                        
                        "88) 退出 \n"
                        " 请输入指令：")
        if com == '99':
            continue
        elif com == '1':
            print "更换报价 34.23 的核心服务"
            qte_config.new_version['new_version_address'] = raw_input("输入最新版报价地址 ，(如 /home/zhiban/guoqing/20180822/sha/  (最后要加'/')):")
            qte_config.new_version['new_version_file'] = raw_input("输入最新acsvrA核心文件，(如 wh.tar.gz):")
            queren = raw_input("重新检查服务器地址 输入 99， 否则回车继续进行...")
            if queren == "99":
                    continue
            mkdir(config.local_svr['local_address'])
            acsvr101()
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
            print "---------------完成 更换更改交易前置 quotaacsvr 操作-----------------"
        else:
            print "没有该命令，请重新输入..."
            continue

if __name__ == '__main__':
    mkdir(qte_config.local_info['local_address'])
    main()
    print "删除 %s" % (qte_config.local_svr['local_address'],)
    shutil.rmtree(qte_config.local_svr['local_address'])
    print "已删除 %s 目录" % (qte_config.local_svr['local_address'],)