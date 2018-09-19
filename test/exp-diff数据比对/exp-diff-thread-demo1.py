#!/usr/bin/python
#-*- coding: utf-8 -*-


import sys
# sys.path.append("/home/zhiban/hjx/lib")
import cx_Oracle
import db_config
import difflib
import re
import threading
import time
import os


#多线程存储数据到本地




def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
 
    if not isExists:
        os.makedirs(path) 
 
        print path+' 创建成功'
        # return True
    else:
        print path+' 目录已存在'
        # return False

def get_data(rows, fp):

    for row in rows:
        out = row
        print >> fp, out
    print '数据存储成功'

def sql_thread(curs, line, table1):
    # thread_num = len(fd_sql)
    shell_split = '\x01'
    fields = [x.strip() for x in line.split(shell_split)]
    filename = fields[0]
    sql = fields[1]
    curs.execute(sql)
    rows = curs.fetchall()
    out_file = './' + table1 + '/' + filename + '.txt'
    mkdir('./' + table1)
    fp = open(out_file, "w+")




def connectOracle(user1, password1, database1, table1, sql_txt):
    shell_split = '\x01'
    fd_sql = open(sql_txt, 'r')
    conn = cx_Oracle.connect(user1, password1, database1)
    curs = conn.cursor()
    sql_threads = []
    with open(sql_txt, 'r') as fp1:
        num = fp1.readlines()
    try:
        gettime = time.time()
        for i in range(len(num)):
            sql_td = threading.Thread(target=sql_thread, args=(curs, num[i], table1))

            sql_threads.append(sql_td)
            sql_td.start()

        for i in range(len(num)):
            sql_threads[i].join()
        print("从数据库读取数据和存储数据用时：", time.time() - gettime)


        for line in fd_sql:
            fields = [x.strip() for x in line.split(shell_split)]
            filename = fields[0]
            sql = fields[1]
            curs.execute(sql)
            rows = curs.fetchall()
            out_file = './'+ table1 +'/' + filename + '.txt'
            mkdir('./' + table1)
            fp = open(out_file, "w+")
            for row in rows:
                out = row
                print >> fp, out
            print '数据存储成功'
    finally:
        curs.close()
        conn.close()
        fp.close()
        fp1.close()

def deldatetime(table1, sql_txt):
    shell_split = '\x01'
    fd_sql = open(sql_txt, 'r')
    try:
        for line in fd_sql:
            fields = [x.strip() for x in line.split(shell_split)]
            filename = fields[0]
            out_file = './' + table1 + '/' + filename + '.txt'
            with open(out_file, 'r') as fp1:
                lenght = fp1.readlines()
                print("正在读取原数据...")

                with open(out_file, 'w') as fp2:
                    for i in range(len(lenght) - 1):
                        s = re.sub(r'datetime\.datetime(\()((\w+, ))+(\w+\))', '', lenght[i])
                        print >> fp2, s
                        print("删除datetime成功。")
    except IOError as e:
        print("删除datetime出错。")
    finally:
        fp1.close()
        fp2.close()


def diff_data(table1, table2, sql_txt):
    shell_split = '\x01'
    allfile = open(sql_txt, 'r')
    a = 0
    b= 0
    for line in allfile:
        fields = [x.strip() for x in line.split(shell_split)]
        file1 = './'+ table1 +'/' + fields[0] + '.txt'
        file2 = './'+ table2 +'/' + fields[0] + '.txt'
        try:
            fd_file1 = open(file1, 'U')
            fd_file2 = open(file2, 'U')
            line1 = fd_file1.readlines()
            line2 = fd_file2.readlines()
            # print 'line1的数据：%s \n' % (line1, )
            # print 'line2的数据：%s \n' % (line2, )
            print '****  ' + fields[0] + ' **** 生产不在灾备的有 : \n'
            print '表'+ table1 +'的数据, 不在表'+ table2 +'的有: \n'

            for i in line1:
                a += 1
                if i not in line2:
                    b += 1
                    print '表%s第%s行的数据, 与表%s第%s行的不同: \n'% (table1, a,table2, b)
                    print '表%s第%s行的数据为: \n'% (table1, a)
                    print i + '\n'
                    print '表%s第%s行的数据为: \n'% (table2, b)
                    d = 0
                    for j in line2:
                        if d == (b-1):
                            print j + '\n'
                            print '-------------------------------------------'
                        d += 1
            print '**************************************************'       
            print '****  ' + fields[0] + ' **** 灾备不在生产的有 : \n'
            print '表'+ table2 +'的数据, 不在表'+ table1 +'的有: \n'
            a = 0
            b = 0
            for j in line2:
                a += 1
                if j not in line1:
                    b += 1
                    print '表%s第%s行的数据, 与表%s第%s行的不同: \n'% (table2, a,table1, b)
                    print '表%s第%s行的数据为: \n'% (table2, a)
                    print j + '\n'
                    print '表%s第%s行的数据为: \n'% (table1, b)
                    c = 0
                    for i in line1:                        
                        if c == (b-1):
                            print i + '\n'
                            print '-------------------------------------------'
                        c += 1

        except IOError as e:
            print '**** 没有获取到文件！\n'
        else:
            print "获取到文件，完成差异匹配！"

def main():
    try:
        for i in range(len(db_config.data)):
            table1 = db_config.data[i]["id"]
            user1 = db_config.data[i]["user"]
            pw1 = db_config.data[i]["pw"]
            dsn1 = db_config.data[i]["dsn"]
            sql_txt = db_config.data[i]["sql_txt"]
            print user1, pw1, dsn1,table1, sql_txt
            try:
                connectOracle(user1, pw1, dsn1,table1, sql_txt)
            except:
                print "数据库连接错误"
            deldatetime(table1, sql_txt)
    except :
        print '获取储存出错'

    table1 = db_config.data[0]["id"]  
    table2 = db_config.data[1]["id"]
    sql_txt = db_config.data[0]["sql_txt"]

    diff_data(table1, table2, sql_txt)


if __name__ == "__main__":
    main()
