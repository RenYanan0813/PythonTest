# -*- coding:utf-8 -*-
1. py�汾: python3.6

2. ��cmd��Ľű���ǰ·���£����У�
 pip3 install -r requirement.txt


 命令说明：

 cpu监控： sar -u 1 3
     #%user #用户空间的CPU使用

    #%nice 改变过优先级的进程的CPU使用率

    #%system 内核空间的CPU使用率

    #%iowait CPU等待IO的百分比

    #%steal 虚拟机的虚拟机CPU使用的CPU

    #%idle 空闲的CPU

    #在以上的显示当中，主要看%iowait和%idle，%iowait过高表示存在I/O瓶颈，
    即磁盘IO无法满足业务需求，如果%idle过低表示CPU使用率比较严重，
    需要结合内存使用等情况判断CPU是否瓶颈。


mem 监控： sar -r 1 3
    #kbmemfree  空闲的物理内存大小

    #kbmemused  使用中的物理内存大小

    #%memused 物理内存使用率

    #kbbuffers 内核中作为缓冲区使用的物理内存大小，kbbuffers和kbcached:这两个值就是free命令中的buffer和cache.

    #kbcached 缓存的文件大小

    #kbcommit  保证当前系统正常运行所需要的最小内存，即为了确保内存不溢出而需要的最少内存（物理内存+Swap分区）

    #commit 这个值是kbcommit与内存总量（物理内存+swap分区）的一个百分比的值


IO 监控 ： sar -b 1 3
    #tps  磁盘每秒钟的IO总数，等于iostat中的tps

    #rtps 每秒钟从磁盘读取的IO总数

    #wtps 每秒钟从写入到磁盘的IO总数

    #bread/s 每秒钟从磁盘读取的块总数

    #bwrtn/s 每秒钟此写入到磁盘的块总数