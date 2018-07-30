#coding:utf-8
import urllib.request

response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))
print(type(response))
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))