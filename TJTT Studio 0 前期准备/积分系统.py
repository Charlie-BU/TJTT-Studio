from tkinter import *
from tkinter.ttk import *
import math
win = Tk()
win.title("高校TJTT积分赛系统（同济内测版）")
win.geometry("700x600")
library = {}

def Lu():
    global win2,E1,E2
    win2 = Tk()
    win2.title("高校TJTT积分赛系统（同济内测版）")
    win2.geometry("700x600")

    L2 = Label(win2,text="请输入选手姓名")
    L2.pack()
    E1 = Entry(win2,width=20)
    E1.pack()
    L3 = Label(win2,text="请输入初始积分")
    L3.pack()
    E2 = Entry(win2,width=20)
    E2.pack()
    B3 = Button(win2,text="确定",command=Que)
    B3.pack()
    win2.mainloop()

def Que():
    try:
        library.setdefault(E1.get(),int(E2.get()))
        L4 = Label(win2,text="成功")
        L4.pack()
    except ValueError:
        L23 = Label(win2, text="请输入数字")
        L23.pack()

def Cha():
    global win3,E3,E4
    win3 = Tk()
    win3.title("高校TJTT积分赛系统（同济内测版）")
    win3.geometry("700x600")

    L5 = Label(win3,text="请输入选手姓名")
    L5.pack()
    E3 = Entry(win3,width=20)
    E3.pack()
    B4 = Button(win3,text="确定",command=Xian)
    B4.pack()
    win3.mainloop()

def Xian():
    if E3.get() in library:
        L38 = Label(win3,text=f"姓名：{E3.get()}     积分：{library[E3.get()]}")
        L38.pack()
    else:
        L28 = Label(win3,text="该选手不存在")
        L28.pack()

def Geng():
    global win4,E28,E22
    win4 = Tk()
    win4.title("高校TJTT积分赛系统（同济内测版）")
    win4.geometry("700x600")
    L43 = Label(win4,text="请输入胜者姓名")
    L43.pack()
    E28 = Entry(win4,width=20)
    E28.pack()
    L72 = Label(win4,text="请输入负者姓名")
    L72.pack()
    E22 = Entry(win4,width=20)
    E22.pack()
    B18 = Button(win4,text="确认",command=Jisuan)
    B18.pack()

    win4.mainloop()

def Jisuan():
    if E28.get() not in library or E22.get() not in library:
        L88 = Label(win4,text="选手不存在")
        L88.pack()
    else:
        L77 = Label(win4,text="成功")
        L77.pack()

        WIN = int(library[E28.get()])
        LOSE = int(library[E22.get()])
        delta = math.fabs(WIN-LOSE)

        if WIN >= LOSE:
            if delta <= 12:
                library.update({E28.get(): WIN + 8})
                library.update({E22.get(): LOSE - 8})
            elif 13 <= delta <= 37:
                library.update({E28.get(): WIN + 7})
                library.update({E22.get(): LOSE - 7})
            elif 38 <= delta <= 62:
                library.update({E28.get(): WIN + 6})
                library.update({E22.get(): LOSE - 6})
            elif 63 <= delta <= 87:
                library.update({E28.get(): WIN + 5})
                library.update({E22.get(): LOSE - 5})
            elif 88 <= delta <= 112:
                library.update({E28.get(): WIN + 4})
                library.update({E22.get(): LOSE - 4})
            elif 113 <= delta <= 137:
                library.update({E28.get(): WIN + 3})
                library.update({E22.get(): LOSE - 3})
            elif 138 <= delta <= 162:
                library.update({E28.get(): WIN + 2})
                library.update({E22.get(): LOSE - 2})
            elif 163 <= delta <= 187:
                library.update({E28.get(): WIN + 2})
                library.update({E22.get(): LOSE - 2})
            elif 188 <= delta <= 212:
                llibrary.update({E28.get(): WIN + 1})
                library.update({E22.get(): LOSE - 1})
            elif 213 <= delta <= 237:
                library.update({E28.get(): WIN + 1})
                library.update({E22.get(): LOSE - 1})
            elif delta >= 238:
                pass
            else:
                print("错误")

        else:
            if delta <= 12:
                library.update({E28.get(): WIN + 8})
                library.update({E22.get(): LOSE - 8})
            elif 13 <= delta <= 37:
                library.update({E28.get(): WIN + 10})
                library.update({E22.get(): LOSE - 10})
            elif 38 <= delta <= 62:
                library.update({E28.get(): WIN + 13})
                library.update({E22.get(): LOSE - 13})
            elif 63 <= delta <= 87:
                library.update({E28.get(): WIN + 16})
                library.update({E22.get(): LOSE - 16})
            elif 88 <= delta <= 112:
                library.update({E28.get(): WIN + 20})
                library.update({E22.get(): LOSE - 20})
            elif 113 <= delta <= 137:
                library.update({E28.get(): WIN + 25})
                library.update({E22.get(): LOSE - 25})
            elif 138 <= delta <= 162:
                library.update({E28.get(): WIN + 30})
                library.update({E22.get(): LOSE - 30})
            elif 163 <= delta <= 187:
                library.update({E28.get(): WIN + 35})
                library.update({E22.get(): LOSE - 35})
            elif 188 <= delta <= 212:
                library.update({E28.get(): WIN + 40})
                library.update({E22.get(): LOSE - 40})
            elif 213 <= delta <= 237:
                library.update({E28.get(): WIN + 45})
                library.update({E22.get(): LOSE - 45})
            elif delta >= 238:
                library.update({E28.get(): WIN + 50})
                library.update({E22.get(): LOSE - 50})
            else:
                print("错误")




L1 = Label(win,text="")
L1.pack()

B1 = Button(win,text="录入初始积分",command=Lu)
B1.pack()

B2 = Button(win,text="更新积分",command=Geng)
B2.pack()

B12 = Button(win,text="查询积分",command=Cha)
B12.pack()



win.mainloop()