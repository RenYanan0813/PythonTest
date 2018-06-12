# -*- coding: utf-8 -*-
import scrapy
from urllib.request import urlopen
from re import findall
import urllib
from myFirstSpider.items import MyfirstspiderItem

class Everycityinsd1Spider(scrapy.Spider):
    name = 'everyCityinSD1'
    allowed_domains = ['www.weather.com.cn']
    start_urls = ['http://www.weather.com.cn/']

    # 遍历各城市，获取要爬取的页面url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    url = r'http://www.weather.com.cn/shandong/index.shtml'
    req = urllib.request.Request(url=url, headers=headers)
    with urlopen(req) as fp:
        contents = fp.read().decode()
    # <a title="济南天气预报" href="http://www.weather.com.cn/weather/101120101.shtml" target="_blank">济南</a>
    pattern = '<a title=".*?" href="(.+?)" target="_blank">(.+?)</a>'
    for url in findall(pattern, contents):  # 遍历寻找相关城市连接且打开
        start_urls.append(url[0])

    def parse(self, response):
        # 处理每个城市的天气预报页面数据
        item = MyfirstspiderItem()
        # xpath的路径： /html/body/div[5]/div[1]/div[1]/div[1]/a[2]
        # extract()[] ??????
        city = response.xpath('//div[@class="crumbs fl"]//a[2]// text()').extract()[0]
        item['city'] = city

        # 每个页面只有一个城市的天气数据，直接取[0]
        selector = response.xpath('//ul[@class="t clearfix"]')[0]

        # 存放天气数据
        weather = ''
        for li in selector.xpath('./li'):
            date = li.xpath('./h1// text()').extract()[0]
            cloud = li.xpath('./p[@class="wea"]// text()').extract()[0]
            temp = li.xpath('./p[@class="tem"]//i// text()').extract()[0]
            wind = li.xpath('./p[@class="win"]//em//span[1]/@title').extract()[0]
            wind = wind + li.xpath('./p[@class="win"]//i// text()').extract()[0]

            weather = weather + date + ':' + cloud + ',' + temp + ',' + wind + '\n'

        item['weather'] = weather
        return [item]

