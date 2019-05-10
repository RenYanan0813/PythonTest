#c:/python36/

#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import logging
import core
import core1
import yaml
import logging.config
import os


def setup_logging(default_path, default_level=logging.DEBUG):
    path = default_path
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def log():
    result = 5 / 0
    print(result)

if __name__ == '__main__':
    # log()
    yaml_path = 'config.yaml'
    setup_logging(yaml_path)
    # core1.run()
    log()
