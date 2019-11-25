# -*- coding:utf-8 -*-
"""
    author: rony
"""

version_svr = {
        "hostname": "180.2.35.130",
        "usrename": "zhiban",
        "password": "zhiban",
        "new_version_path": "",  #新版本路径
        "new_version_file": ""   #新版本tar压缩包
}

qte_acsvr = {
    {
        "hostname": "180.2.34.23",
        "usrename": "qte",
        "password": "thisisapwd",
        "server_path": "/home/qte/install/",   #前置服务安装路径
        "flag": "A",
        "svr_cfgs": ['qte_acsvr', 'qte_quotaacsvr', 'qte_qy_acsvr']
    },
    {
        "hostname": "180.2.34.24",
        "usrename": "qte",
        "password": "thisisapwd",
        "server_path": "/home/qte/install/",  #前置服务安装路径
        "flag": "B",
        "svr_cfgs": ['qte_acsvr', 'qte_quotaacsvr', 'qte_qy_acsvr']
    }
}

bpt_acsvr = {
    {
        "hostname": "180.2.34.30",
        "usrename": "ac",
        "password": "ac",
        "server_path": "/home/ac/install/" ,  #前置服务安装路径
        "flag": "A",
        "svr_cfgs": ['']
    },
    {
        "hostname": "180.2.34.31",
        "usrename": "ac",
        "password": "ac",
        "server_path": "/home/ac/install/",   #前置服务安装路径
        "flag": "B",
        "svr_cfgs": ['']
    }
}

common_local_path = {
    "local_address": "d:\\svrconfig\\", #存储在本地的路径(最后要加'\\')
}