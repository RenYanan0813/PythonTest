# -*- coding:utf-8 -*-
"""
    author: rony
"""

import os
import re
from tkinter.filedialog import askdirectory,askopenfilename
import time

def count_lines(filepath):
    count = 0
    for index, line in enumerate(open(filepath, 'r')):
        count += 1
    return count

#清理服务监控数据
def getMainData(file_path, catch_data_file):
    try:
        with open(file_path, 'r+') as fp:
        # for index, line in enumerate(open(file_path, 'r')):
            num_lines = count_lines(file_path)
            lenghts = fp.readlines()
            start_time = time.time()
            for i in range(num_lines):
                with open(catch_data_file, 'a') as cf:
                    if '' == lenghts[i] or lenghts[i] == '\n' or lenghts[i] == None or "grep" in lenghts[i] or "sar" in lenghts[i]\
                            or "bash" in lenghts[i] or "<defunct>" in lenghts[i] or "sadc" in lenghts[i] or "ps" in lenghts[i] \
                            or "tail" in lenghts[i] or "%" in lenghts[i] or "sshd" in lenghts[i] or "df" in lenghts[i]:
                    # if '' == line or line == '' or line == None or "grep" in line or "sar" in \
                    #         line \
                    #         or "bash" in line or "<defunct>" in line or "sadc" in line or "ps" in \
                    #         line \
                    #         or "tail" in line or "%" in line or "sshd" in line:
                        pass
                    # elif len(lenghts[i].split()) == 0:
                    #     pass
                    else:
                        if "某些服务使用 cpu 情况" in lenghts[i]:
                            lenghts[i] = str(re.findall('(\d{8}).*(\d{2}:\d{2}:\d{2}).*(\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', lenghts[i]))
                            lenghts[i] = lenghts[i].replace('[(', '').replace(')]', '').replace('\\', '').replace(',', '')
                            cf.write(lenghts[i])
                        else:
                            lenghts[i] = lenghts[i].replace('...', ' ')
                            cf.write(lenghts[i])
                end_time = time.time()
                if i%100 == 0:
                    print("正在清理数据中，已用时***** %s 秒 ......."%(int(end_time - start_time)))
    except IOError as e:
        e.with_traceback()
    finally:
        # fp.close()
        cf.close()


if __name__ == "__main__":
    #获取要分析文件的路径
    path_file = askopenfilename()
    file_name = path_file.split('/')[-1].replace('.txt', '')
    file_name = "%s.csv"%(file_name, )
    getMainData(path_file, file_name)