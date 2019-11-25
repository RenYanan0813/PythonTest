# -*- coding:utf-8 -*-
"""
    author: rony
"""

import queue

q = queue.Queue()

q.put(111)
q.task_done()
# q.join()
q.put(111)
# q.task_done()
# q.join()
q.task_done()
q.put(333)


print(q.get())
print(q.get())
print(q.get())