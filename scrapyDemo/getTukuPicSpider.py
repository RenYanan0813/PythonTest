# -*- coding: utf-8 -*-
import scrapy


class GettukupicspiderSpider(scrapy.Spider):
    name = 'getTukuPicSpider'
    allowed_domains = ['www.zhuoku.com']
    start_urls = ['http://www.zhuoku.com/']

    def parse(self, response):
        pass
