#-*- coding:utf-8 -*-
import xlrd


#获取全部数据
def get_all_data(filename):
    table = xlrd.open_workbook(filename)
    data = table.sheet_by_name('Sheet1')
    row1 = data.row_values(0)
    data_list = []
    for r in xrange(1, data.nrows):
        sername = data.row_values(r)[0]  # 获取服务名
        each = data.row_values(r)  # 每一个服务对应的信息列表
        temp_dict = dict(zip(row1, each))
        temp = {sername : temp_dict}
        data_list.append(temp)
    return data_list



if __name__ == '__main__':
    data_list = get_all_data('liantiao-0824.xls')  # 全部源数据
