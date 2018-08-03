# coding:utf-8
import db_config
import cx_Oracle


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

def main():
    connectOracle('reg_user', 'oracle123', '180.2.35.162:1521/djtest','162', './sql.txt')



if __name__ == "__main__":
    main()