# -*- coding:utf-8 -*-
"""
    author: rony
"""

import logging
import core
import core1

logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)

# Handler
handler = logging.FileHandler('main_result.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Main Info')
logger.debug('Main Debug')
logger.error('Main Error')
core.run()
core1.run()