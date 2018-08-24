# -*- coding:utf-8 -*-

#新版交易前置acsvr信息
new_acsvr = {
    'hostname': '182.2.35.130', #服务器地址
    'username': 'zhiban', #服务器用户名
    'password': 'zhiban', #服务器密码
    'new_acsvr_address': '', #最新acsvr路径
    'new_acsvr_file': '', #最新acsvr的文件名
}

#要更换wh版本的服务器信息
old_acsvr = {
    'hostname': '182.2.32.20', #服务器地址
    'username': 'reg1', #服务器用户名
    'password': 'reg1', #服务器密码
    'old_wh_address': '/home/reg1/', #acsvr路径
    'old_wh_file': 'wh', #acsvr的文件名
    'new_wh_file': '', #從本地上傳的新版本wh
    'old_wh_conf_add': '/home/reg1/wh/config/' #acsvr的需要修改的配置文件路徑
}

#中转文件本地信息，即文件下载、更改配置文件的本地目录
local_wh = {
    'local_address': 'd:\\sshclient\\', #存储在本地的路径
}