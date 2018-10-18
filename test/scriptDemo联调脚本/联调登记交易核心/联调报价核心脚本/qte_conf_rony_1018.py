# -*- coding:utf-8 -*-

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
        temp_dict = dict(zip(row1, each))
        temp = {sername : temp_dict}
        data_list.append(temp)
    return data_list


# 操作选项
def choice_op():
    while True:
        print('根据下面的提示选择操作\n')
        print('1)启动验收服务器                      3)自定义操作')
        print('2)停止验收服务器                      90)查询系统磁盘空间')
        print('99)退出\n\n')

        choice = raw_input('请输入操作选项：')

        if choice == '1':
            print('启动验收服务器')
            continue
        elif choice == '2':
            print('停止验收服务器')
            continue
        elif choice == '90':
            print('查询系统磁盘空间')
            continue
        elif choice == '99':
            print('正在退出....')
            break
        elif choice == '3':
            self_choice()
        else:
            print("")
            continue

if __name__ == '__main__':
    data_list = get_all_data('liantiao-0824.xls')  # 全部源数据
    choice_op()