#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
Level
首先我们来了解一下输出日志的等级信息，logging 模块共提供了如下等级，每个等级其实都对应了一个数值，列表如下：



等级
数值




CRITICAL
50


FATAL
50


ERROR
40


WARNING
30


WARN
30


INFO
20


DEBUG
10


NOTSET
0



这里最高的等级是 CRITICAL 和 FATAL，两个对应的数值都是 50，另外对于 WARNING 还提供了简写形式 WARN，两个对应的数值都是 30。
我们设置了输出 level，系统便只会输出 level 数值大于或等于该 level 的的日志结果，例如我们设置了输出日志 level 为 INFO，那么输出级别大于等于 INFO 的日志，如 WARNING、ERROR 等，DEBUG 和 NOSET 级别的不会输出。
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)

# Log
logger.debug('Debugging')
logger.critical('Critical Something')
logger.error('Error Occurred')
logger.warning('Warning exists')
logger.info('Finished')
这里我们设置了输出级别为 WARN，然后对应输出了五种不同级别的日志信息，运行结果如下：
Critical Something
Error Occurred
Warning exists
可以看到只有 CRITICAL、ERROR、WARNING 信息输出了，DEBUG、INFO 信息没有输出。
Handler

作者：崔庆才丨静觅
链接：https://juejin.im/post/5b13fdd0f265da6e0b6ff3dd
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import logging
logging.basicConfig(level=logging.DEBUG,
                    filename='outputLevel.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)

# Log
logger.debug('Debugging')
logger.critical('Critical Something')
logger.error('Error Occurred')
logger.warning('Warning exists')
logger.info('Finished')