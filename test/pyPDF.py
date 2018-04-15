#-*- coding:utf-8 -*-

	"""

	"""

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

base_url = 'http://python3-cookbook.readthedocs.io/zh_CN/latest/'
book_name = ''
chapter_info = []



def get_one_page(url):
	"""
	获取网页html内容并返回
    :param url: 目标网址
    :return html
	"""

	header = {
		"User-Agent":""" Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"""
	}