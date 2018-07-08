#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
Handler
下面我们先来了解一下 Handler 的用法，看下面的实例：
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('output.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')
这里我们没有再使用 basicConfig 全局配置，而是先声明了一个 Logger 对象，然后指定了其对应的 Handler 为 FileHandler 对象，然后 Handler 对象还单独指定了 Formatter 对象单独配置输出格式，最后给 Logger 对象添加对应的 Handler 即可，最后可以发现日志就会被输出到 output.log 中，内容如下：
2018-06-03 14:53:36,467 - __main__ - INFO - This is a log info
2018-06-03 14:53:36,468 - __main__ - WARNING - Warning exists
2018-06-03 14:53:36,468 - __main__ - INFO - Finish
另外我们还可以使用其他的 Handler 进行日志的输出，logging 模块提供的 Handler 有：

StreamHandler：logging.StreamHandler；日志输出到流，可以是 sys.stderr，sys.stdout 或者文件。
FileHandler：logging.FileHandler；日志输出到文件。
BaseRotatingHandler：logging.handlers.BaseRotatingHandler；基本的日志回滚方式。
RotatingHandler：logging.handlers.RotatingHandler；日志回滚方式，支持日志文件最大数量和日志文件回滚。
TimeRotatingHandler：logging.handlers.TimeRotatingHandler；日志回滚方式，在一定时间区域内回滚日志文件。
SocketHandler：logging.handlers.SocketHandler；远程输出日志到TCP/IP sockets。
DatagramHandler：logging.handlers.DatagramHandler；远程输出日志到UDP sockets。
SMTPHandler：logging.handlers.SMTPHandler；远程输出日志到邮件地址。
SysLogHandler：logging.handlers.SysLogHandler；日志输出到syslog。
NTEventLogHandler：logging.handlers.NTEventLogHandler；远程输出日志到Windows NT/2000/XP的事件日志。
MemoryHandler：logging.handlers.MemoryHandler；日志输出到内存中的指定buffer。
HTTPHandler：logging.handlers.HTTPHandler；通过"GET"或者"POST"远程输出到HTTP服务器。

下面我们使用三个 Handler 来实现日志同时输出到控制台、文件、HTTP 服务器：
import logging
from logging.handlers import HTTPHandler
import sys

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)

# FileHandler
file_handler = logging.FileHandler('output.log')
file_handler.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# HTTPHandler
http_handler = HTTPHandler(host='localhost:8001', url='log', method='POST')
logger.addHandler(http_handler)

# Log
logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')
运行之前我们需要先启动 HTTP Server，并运行在 8001 端口，其中 log 接口是用来接收日志的接口。
运行之后控制台输出会输出如下内容：
This is a log info
Debugging
Warning exists
Finish
output.log 文件会写入如下内容：
2018-06-03 15:13:44,895 - __main__ - INFO - This is a log info
2018-06-03 15:13:44,947 - __main__ - WARNING - Warning exists
2018-06-03 15:13:44,949 - __main__ - INFO - Finish

作者：崔庆才丨静觅
链接：https://juejin.im/post/5b13fdd0f265da6e0b6ff3dd
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('outputhandel.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')
