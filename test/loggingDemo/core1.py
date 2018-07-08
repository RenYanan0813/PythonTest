#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import logging

logger = logging.getLogger('main.core')

def run():
    try:
        result = 5 / 0
    except:
        logger.info('Core1 Info')
        logger.debug('Core1 Debug')
        logger.error('Core1 Error', exc_info=True)
        logger.exception('error')
