# -*- coding:utf-8 -*-
import config
import datetime


def qq():
    delFile(old_acsvr_wm_add, config.old_acsvr_wm['hostname'], config.old_acsvr_wm['username'],
                    config.old_acsvr_wm['password'])
    print "删除 acsvr_wm{date}.tar.gz 压缩包完成！"