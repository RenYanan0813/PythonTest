# -*- coding:utf-8 -*-

import pexpect

ipaddress = 'zhiban@180.2.34.230'
cmd = 'ssh' + ipaddress
loginname = 'cln'
ippassword = 'cln'

#链接到ssh服务器上
# child = pexpect.spawn(cmd)
child = pexpect.spawn("c:\windows\system32\cmd.exe")
child.expect('Password:')
child.sendline(ippassword)

#根据获取的关键字来判断输入内容


