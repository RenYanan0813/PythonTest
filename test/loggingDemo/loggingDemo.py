#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"
'''
在这里我们首先引入了 logging 模块，
    然后进行了一下基本的配置，这里通过 basicConfig 配置了 level 信息和 format 信息，
    这里 level 配置为 INFO 信息，即只输出 INFO 级别的信息，另外这里指定了 format 格式的字符串，
    包括 asctime、name、levelname、message 四个内容，
    分别代表运行时间、模块名称、日志级别、日志内容，
    这样输出内容便是这四者组合而成的内容了，这就是 logging 的全局配置。

接下来声明了一个 Logger 对象，它就是日志输出的主类，
    调用对象的 info() 方法就可以输出 INFO 级别的日志信息，
    调用 debug() 方法就可以输出 DEBUG 级别的日志信息，
    非常方便。在初始化的时候我们传入了模块的名称，
    这里直接使用 __name__ 来代替了，就是模块的名称，
    如果直接运行这个脚本的话就是 __main__，如果是 import 的模块的话就是被引入模块的名称，
    这个变量在不同的模块中的名字是不同的，所以一般使用 __name__ 来表示就好了，
    再接下来输出了四条日志信息，其中有两条 INFO、一条 WARNING、一条 DEBUG 信息，我们看下输出结果：

作者：崔庆才丨静觅
链接：https://juejin.im/post/5b13fdd0f265da6e0b6ff3dd
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')

'''
可以看到输出结果一共有三条日志信息，
    每条日志都是对应了指定的格式化内容，
    另外我们发现 DEBUG 的信息是没有输出的，
    这是因为我们在全局配置的时候设置了输出为 INFO 级别，
    所以 DEBUG 级别的信息就被过滤掉了。
    这时如果我们将输出的日志级别设置为 DEBUG，
    就可以看到 DEBUG 级别的日志输出了：

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
输出结果：

2018-06-03 13:49:22,770 - __main__ - INFO - This is a log info
2018-06-03 13:49:22,770 - __main__ - DEBUG - Debugging
2018-06-03 13:49:22,770 - __main__ - WARNING - Warning exists
2018-06-03 13:49:22,770 - __main__ - INFO - Finish

作者：崔庆才丨静觅
链接：https://juejin.im/post/5b13fdd0f265da6e0b6ff3dd
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''