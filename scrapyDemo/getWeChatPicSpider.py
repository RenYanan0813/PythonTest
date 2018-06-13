#c:/python36/

#-*- coding: utf-8 -*-
from urllib.request import urlopen
from re import findall
import urllib3
import urllib
from urllib import request
from random import Random


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    #url = r'http://www.weather.com.cn/shandong/index.shtml'
headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0"}

# url = r'http://www.zhuoku.com/zhuomianbizhi/star-starcn/20180529164133.htm'
url = 'http://www.zhuoku.com/zhuomianbizhi/star-starcn/20180530160327.htm'
req = urllib.request.Request(url=url, headers=headers)
with urlopen(req) as fp:
    content = fp.read().decode("ascii","ignore")

# pattern = 'data-type="png" data-src="(.+?)"'
#pattern = '<a title=".*?" href="(.+?)" target="_blank">(.+?)</a>'
pattern = '<div class="bizhiin"><a href="(.+?)" target="_blank">(.+?)</a></div>'
result = findall(pattern, content)
x = 1119
for index, item in enumerate(result):
    # url = urllib.request.Request(url=str(item), headers=headers)
    url1 = 'http://www.zhuoku.com/zhuomianbizhi/star-starcn/' + item[0] + '#turn'
    url1 = urllib.request.Request(url=str(url1), headers=headers)
    with urlopen(url1) as fp:
        content1 = fp.read().decode("ascii","ignore")
        pattern1 = r'id="imageview" src="(.+?)" '
        result1 = findall(pattern1, content1)
        urlrlt = result1[0]
        # urlrlt = urllib.request.Request(url=str(urlrlt), headers=headers)
        # with urlopen(urlrlt) as fp3:
        #     with open('(.+?)'+'.jpg', 'wb') as fp1:
        #         fp1.write(fp3.read().decode("ascii","ignore"))
        urllib.request.urlretrieve(str(urlrlt), 'D:\SpiderImage\%s.jpg' % x)
        x += 1