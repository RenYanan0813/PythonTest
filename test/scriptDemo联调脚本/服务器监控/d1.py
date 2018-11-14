# -*- coding:utf-8 -*-

from tkinter import *
import time


def onGo():
    print("0000")
    t.delete('1.0', 'end')
    for i in range(50):
        t.insert(INSERT, 'a_' + str(i))
        time.sleep(0.1)



root = Tk()
t = Text(root)
t.pack()
goBtn = Button(text="Go!", command=onGo)
goBtn.pack()
root.mainloop()