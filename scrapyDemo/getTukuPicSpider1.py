# -*- coding: utf-8 -*-
import scrapy


class Gettukupicspider1Spider(scrapy.Spider):
    name = 'getTukuPicSpider1'
    allowed_domains = ['www.zhuoku.com']
    start_urls = ['http://www.zhuoku.com/']

    def parse(self, response):
        pass
