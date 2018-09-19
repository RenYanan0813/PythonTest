# coding:utf-8

import re
def readData(localtxt):
    with open(localtxt, 'r') as f:
        # lenght = f.read()
        lenght = f.readlines()
        print(len(lenght[0]))
        # for i in range(len(lenght[0])-1):
        #     print(lenght[i] +"\n")

        print(len(lenght))
        print(type(lenght[0]))
        # print(lenght[0].replace(r"datetime\((.*)", ""))

        with open('./c.txt','w') as f:
            for i in range(len(lenght) - 1):
                s = re.sub(r'datetime\.datetime(\()((\w+, ))+(\w+\))', '', lenght[i])
                print >> f, s



if __name__ == "__main__":
    readData("./b.txt")