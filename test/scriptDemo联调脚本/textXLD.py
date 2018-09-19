#-*- coding: utf-8 -*-
# python version: 3.6

__author__ = "renyanan"

import xlrd

# 获取全部数据
def get_all_data(filename):
    table = xlrd.open_workbook(filename)
    data = table.sheet_by_name('Sheet1')
    row1 = data.row_values(0)
    data_list = []
    for r in xrange(1, data.nrows):
        sername = data.row_values(r)[0]  # 获取服务名
        each = data.row_values(r)  # 每一个服务对应的信息列表
        zip1 = zip(row1, each)
        temp_dict = dict(zip(row1, each))
        temp = {sername : temp_dict}
        data_list.append(temp)
    return data_list


# 根据提供的服务名列表获取到服务器信息
def get_need_hostinfo(data_list, search_list):
    res = list(filter(lambda data: data if str(data.keys()[0]) in search_list else False, data_list))
    need_list = []
    for host in res:
        need_list.append(host.values()[0])
    return need_list

def testing1():
    needlist = get_need_hostinfo(data_list, ['ctrlsvr-A', 'ctrlsvr-B'])
    print needlist

if __name__ == '__main__':
    data_list = get_all_data('liantiao-0817.xls')  # 全部源数据
    print data_list

    print "--------------------------"

    testing1()
