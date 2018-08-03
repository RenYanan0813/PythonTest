# coding:utf-8
def diff_data(table1='222', table2='69'):
    shell_split = '\x01'
    allfile = open('./sql.txt', 'r')
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
                    print line2[b-1] + '\n'
                    print '-------------------------------------------'
                    
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
                    print line1[b-1] + '\n'
                    print '-------------------------------------------'

        except IOError as e:
            print '**** 没有获取到文件！\n'
        else:
            print "获取到文件，完成差异匹配！"

if __name__ == '__main__':
        diff_data()