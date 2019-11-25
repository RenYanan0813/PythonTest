#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import logging

logger = logging.getLogger('main.core')

def run():
    logger.info('Core Info')
    logger.debug('Core Debug')
    logger.error('Core Error')


