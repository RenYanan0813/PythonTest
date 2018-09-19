# -*- coding:utf-8 -*-

#最新wh版本信息
new_wh = {
    'hostname': '180.2.35.130', #服务器地址
    'username': 'zhiban', #服务器用户名
    'password': 'zhiban', #服务器密码
    'new_wh_address': '', #最新wh路径
    'new_wh_file': '', #最新wh的文件名
}

#要更换wh版本的服务器信息
old_wh = {
    'hostname': '180.2.32.20', #服务器地址
    'username': 'reg1', #服务器用户名
    'password': 'reg1', #服务器密码
    'old_wh_address': '/home/reg1/', #wh路径
    'old_wh_file': 'wh', #wh的文件名
    'new_wh_file': '', #從本地上傳的新版本wh
    'old_wh_conf_add': '/home/reg1/wh/config/' #wh的需要修改的配置文件路徑
}

#中转文件本地信息，即文件下载、更改配置文件的本地目录
local_wh = {
    'local_address': 'd:\\sshclient\\', #存储在本地的路径
}

#仓储服务信息
wh_svr = {
    'hostname': '180.2.32.20', #服务器地址
    'username': 'reg1', #服务器用户名
    'password': 'reg1', #服务器密码
    'svr_address':'/home/reg1/wh/', #服务地址
    'svr_state': './ctrl state', #查看服务状态
    'svr_stop': './ctrl stop', #停服务
    'svr_run_main': './ctrl start', #启动main
    'svr_run_watch': 'nohup ./watch &' #启动watch
}