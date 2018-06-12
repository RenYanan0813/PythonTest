#c:/python36/

#-*- coding: utf-8 -*-
'''
问题描述：
    读入一个字符串str，输出字符串str中的连续最长的数字串。
'''
import re
def getLongStr(str):
    t = re.findall('\d+', str)
    if t:
        return max(t, key=len) #max高级函数
    return 'No'


def longest2(s):
    '''使用非数字作为分隔符'''
    import re
    t = re.split('[^\d]+', s)
    if t:
        return max(t, key=len)
    return 'No'


def longest3(s):
    '''笨办法'''
    result = []
    t = []
    # 遍历字符串中所有字符
    for ch in s:
        # 遇到数字，记录到临时变量
        if '0' <= ch <= '9':
            t.append(ch)
        elif t:
            # 遇到非数字，把临时变量中的连续数字记下来
            result.append(''.join(t))
            t = []
    # 考虑原字符串以数字结束的情况
    if t:
        result.append(''.join(t))

    if result:
        return max(result, key=len)
    return 'No'

if __name__ == '__main__':
    str = input("please input a string:")
    print(getLongStr(str))