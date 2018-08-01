# -*- coding:utf-8 -*-

import sys
from winpexpect import winspawn
import win32gui

ipaddress = 'zhiban@180.2.34.203'
cmd = ipaddress
loginname = u'zhiban'
ippassword = u'zhiban'


# child = winspawn('ssh',['-tty','zhiban@180.2.34.203'])
child = winspawn('c:\windows\system32\cmd.exe')

#定义了常用按键的编码
n=win32gui.FindWindow('ConsoleWindowClass',None)
# child = winpexpect.winspawn("ssh zhiban@180.2.34.203 ")
child.sendline(u"ssh zhiban@180.2.34.203 ")
# child.logfile = sys.stdout
# child.expect('User.*:')
# child.sendline(loginname)
child.expect('password:')
child.sendline(ippassword)
child.sendline('ls')
# print('Now enter the ssh interactive mode')
child.interact()