# coding:utf-8
import db_config
import cx_Oracle
import os
import paramiko
import re

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

        print path + ' 创建成功'
        # return True
    else:
        print path + ' 目录已存在'
        # return False


def connectOracle(user1 , password1, database1, table1, sql_txt):
    shell_split = '\x01'
    fd_sql = open(sql_txt, 'r')
    conn = cx_Oracle.connect(user1, password1, database1)
    curs = conn.cursor()
    try:
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

def getFileToLocal(com_add, target_add):
    t = paramiko.Transport(('180.2.34.203', 22))
    t.connect(username='cln', password='cln')
    sftp = paramiko.SFTPClient.from_transport(t)
    # com_add = '/home/cln/ryn.tar'
    # target_add = raw_input('输入文件存放地址:')
    # target_add = 'd:\\sshclient\\ryn.tar'
    try:
        sftp.get(com_add, target_add)
    except:
        print '服务器没有该文件!'
    print '下载完成[=========================] 100%  ', "文件存放在:%s" % (target_add)
    sftp.close()

def changeFile():
    com_txt = '/home/cln/ryn/text.py'
    target_txt = 'd:\\sshclient\\text\\text.py'
    getFileToLocal(com_txt, target_txt)
    # txt = '/home/cln/ryn/ryn/pexpectdemo.py'
    # fd_sql = open(target_txt, 'r')
    try:
        with open(target_txt, 'r') as fp1:
            lenght = fp1.readlines()
            print("正在读取原数据...")
            with open(target_txt, 'w') as fp2:
                s = re.sub(r'server_port = ((\w+, ))+(\w+\))', '', lenght)
                print >> fp2, s
                print("更改成功。")
    except IOError as e:
        print("更改出错。")
    finally:
        fp1.close()
        fp2.close()


def main():
    # connectOracle('reg_user', 'oracle123', '180.2.35.162:1521/djtest','162', './sql.txt')
    changeFile()



if __name__ == "__main__":
    main()