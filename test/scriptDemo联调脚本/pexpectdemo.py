#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import pexpect

# child = pexpect.popen_spawn.PopenSpawn('ssh zhiban@180.2.35.130', encoding='utf-8')

child = pexpect.spawn('ssh zhiban@180.2.35.130', encoding='utf-8')

child.expect('.*password:.* ')# 等待password:字符出现
print(child.before + child.after)#  输出password:前后的字符
child.sendline('zhiban') #  发送密码
child.expect(']\$')#  等待]$字符出现
print(child.before + child.after)
child.interact()#  把ssh的连接交给用户控制。
child.close()


