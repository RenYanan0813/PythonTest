# -*- coding:utf-8 -*-


#要更换报价34.23版本的服务器信息
svr_info_A = {
    'hostname': '180.2.34.23', #服务器地址
    'username': 'qte', #服务器用户名
    'password': 'qte', #服务器密码
    'old_version_address': '/home/qte/install/', #旧版本路径(最后要加'/')
    'old_version_folder': 'authsvr, bridgesvr_qte, corpsvr, dealsvr,'
                          'infosvr, loginsvr, qte_acsvr, qte_qy_acsvr,'
                          'qte_quotaacsvr, qte_initsvr, qte_mem2dbsvr',    #各服务的文件夹名
    'new_version_folder': '', #從本地上傳的新版本文件夹名(为空，不要填)
    'old_svr_conf_adds': '/home/qte/install/%s/conf/', #acsvr_acct的需要修改的配置文件路徑(最后要加'/')
    'svr_conf_files': 'authsvr-A.cfg, bridgesvr.cfg, corpsvr.cfg, dealsvr.cfg,'
                      'infosvr.cfg, loginsvr.cfg, qte_acsvr.cfg, qte_qy_acsvr.cfg,'
                      'qte_quotaacsvr.cfg,qte_initsvr.cfg, qte_mem2dbsvr.cfg', #需要更改的配置文件
}

#要更换报价34.24版本的服务器信息
svr_info_B = {
    'hostname': '180.2.34.24', #服务器地址
    'username': 'qte', #服务器用户名
    'password': 'qte', #服务器密码
    'old_version_address': '/home/qte/install/', #旧版本路径(最后要加'/')
    'old_version_folder': 'authsvr, bridgesvr_qte, corpsvr, dealsvr,'
                          'infosvr, loginsvr, qte_acsvr, qte_qy_acsvr,'
                          'qte_quotaacsvr',  #各服务的文件夹名
    'new_version_folder': '', #從本地上傳的新版本文件夹名(为空，不要填)
    'old_svr_conf_adds': '/home/qte/install/%s/conf/', #acsvr_acct的需要修改的配置文件路徑(最后要加'/')
    'svr_conf_files': 'authsvr-B.cfg, bridgesvr.cfg, corpsvr.cfg, dealsvr.cfg,'
                      'infosvr.cfg, loginsvr.cfg, qte_acsvr.cfg, qte_qy_acsvr.cfg,'
                      'qte_quotaacsvr.cfg', #需要更改的配置文件
}

#新版报价信息
new_version = {
    'hostname': '180.2.35.130', #服务器地址
    'username': 'zhiban', #服务器用户名
    'password': 'zhiban', #服务器密码
    'new_version_address': '', #最新acsvr_acct路径
    'new_version_file': '', #最新acsvr_acct的文件名
}

#中转文件本地信息，即文件下载、更改配置文件的本地目录
local_info = {
    'local_address': 'd:\\qteconfig\\', #存储在本地的路径(最后要加'\\')
}