#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

'''
接下来我们首先来全面了解一下 basicConfig 的参数都有哪些：

filename：即日志输出的文件名，如果指定了这个信息之后，实际上会启用 FileHandler，而不再是 StreamHandler，这样日志信息便会输出到文件中了。
filemode：这个是指定日志文件的写入方式，有两种形式，一种是 w，一种是 a，分别代表清除后写入和追加写入。
format：指定日志信息的输出格式，即上文示例所示的参数，详细参数可以参考：docs.python.org/3/library/l…，部分参数如下所示：

%(levelno)s：打印日志级别的数值。
%(levelname)s：打印日志级别的名称。
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]。
%(filename)s：打印当前执行程序名。
%(funcName)s：打印日志的当前函数。
%(lineno)d：打印日志的当前行号。
%(asctime)s：打印日志的时间。
%(thread)d：打印线程ID。
%(threadName)s：打印线程名称。
%(process)d：打印进程ID。
%(processName)s：打印线程名称。
%(module)s：打印模块名称。
%(message)s：打印日志信息。


datefmt：指定时间的输出格式。
style：如果 format 参数指定了，这个参数就可以指定格式化时的占位符风格，如 %、{、$ 等。
level：指定日志输出的类别，程序会输出大于等于此级别的信息。
stream：在没有指定 filename 的时候会默认使用 StreamHandler，这时 stream 可以指定初始化的文件流。
handlers：可以指定日志处理时所使用的 Handlers，必须是可迭代的。

下面我们再用一个实例来感受一下：
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')
这里我们指定了输出文件的名称为 output.log，另外指定了日期的输出格式，其中年月日的格式变成了 %Y/%m/%d，另外输出的 format 格式增加了 lineno、module 这两个信息，运行之后便会生成一个 output.log 的文件，内容如下：
2018/06/03 14:43:26 - __main__ - INFO - 9 - demo3 - This is a log info
2018/06/03 14:43:26 - __main__ - DEBUG - 10 - demo3 - Debugging
2018/06/03 14:43:26 - __main__ - WARNING - 11 - demo3 - Warning exists
2018/06/03 14:43:26 - __main__ - INFO - 12 - demo3 - Finish
可以看到日志便会输出到文件中，同时输出了行号、模块名称等信息。
以上我们通过 basicConfig 来进行了一些全局的配置，我们同样可以使用 Formatter、Handler 进行更灵活的处理，下面我们来了解一下。

作者：崔庆才丨静觅
链接：https://juejin.im/post/5b13fdd0f265da6e0b6ff3dd
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')


