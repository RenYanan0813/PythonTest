from translate import Translator
import time
import tkinter
from PIL import Image,ImageTk

class translate(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Qucik 词典")
        self.root.geometry("304x260")#定制主窗体大小
        self.im=Image.open("pic.gif")
        self.img=ImageTk.PhotoImage(self.im)
        self.f0 = tkinter.Frame(self.root,width=300,height=70)
        self.f1 = tkinter.Frame(self.root,width=300,height=70)
        self.f2 = tkinter.Frame(self.root,width=300,height=70)
        self.f3 = tkinter.Frame(self.root,width=300,height=70)
        self.imLabel=tkinter.Label(self.f0,image=self.img)
        self.l1 = tkinter.Label(self.f1,text='原文',width=10)
        self.get_words = tkinter.Text(self.f1,width=31,height=2)
        self.l2 = tkinter.Label(self.f2,text='译文',width=10)
        self.display_info = tkinter.Text(self.f2,width=31,height=2)
        self.result_button = tkinter.Button(self.f3,width=20,height=2,command=self.translates,text="翻译")
        self.dele_botton = tkinter.Button(self.f3,width=20,height=2,command=self.dele_text,text="清空")

    def gui_arrang(self):
        self.f0.grid(row=0, column=0)
        self.f1.grid(row=1, column=0)
        self.f2.grid(row=2, column=0)
        self.f3.grid(row=3, column=0)
        self.imLabel.grid(row=0,column=0)
        self.l1.grid(row=0, column=0)
        self.get_words.grid(row=0, column=1)
        self.l2.grid(row=0, column=0)
        self.display_info.grid(row=0, column=1)
        self.result_button.grid(row=0, column=0)
        self.dele_botton.grid(row=0, column=1)

    def translates(self):
        self.words = self.get_words.get('0.0','end')
        self.translator= Translator(from_lang='zh',to_lang='en')
        self.translation = self.translator.translate(self.words)
        self.time_format = '%Y-%m-%d %X'
        self.time_current = time.strftime(self.time_format)
        with open('翻译记录.txt','a',encoding='utf8') as f:
            f.write('时间:%s 原文:%s译文:%s\n' % (self.time_current,self.words,self.translation))
        self.display_info.insert('insert',self.translation)

    def dele_text(self):
        self.display_info.delete(0.0,tkinter.END)
        self.get_words.delete(0.0,tkinter.END)


def main():
    TL = translate()
    TL.gui_arrang()
    tkinter.mainloop()

if __name__ == "__main__":
    main()































