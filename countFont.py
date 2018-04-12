#c:/Python34/python
# coding: utf-8

import os,re
from collections import Counter

#目标文件所在目录
FILE_PATH = './count'

def getCounter(articlefilesource):
    ''' 输入一个英文的纯文本文件，统计其中的单词出现的个数'''
    pattern = r'''[A-Za-z]+|\$?\d+%?$'''
    with open(articlefilesource) as f:
        r = re.findall(pattern, f.read())
        return Counter(r)


#过滤词
stop_word = ['I','the','in','of','and','to','has','that','is','a','an','as','with']

def run(FILE_PATH):
    #切换到目标文件所在目录
    os.chdir(FILE_PATH)
    #遍历该目录下的txt文件
    total_counter = Counter()
    for i in os.listdir(os.getcwd()):
        if os.path.splitext(i)[1] == '.txt':
            total_counter += getCounter(i)
        #排除stopword的影响
        for i in stop_word:
            total_counter[i] = 0
        #print total_counter.most_common()[0][0]
        #print total_counter.most_common()
        print (total_counter.most_common()[0])

if __name__ == '__main__':
    run(FILE_PATH)
