import socket
import os
from tkinter import *  # NOQA
from tkinter.ttk import *  # NOQA
from tkinter import messagebox
from PIL import Image, ImageTk

ip_port = ('127.0.0.1', 6969)
path = os.getcwd() + "/cdata"


def mainfunc(s):
    print("get in")
    cmd = combo.get()
    argc = txt1.get()
    inp = cmd + ' ' + argc
    s.sendall(inp.encode())
    if not cmd:  # 防止输入空信息，导致异常退出
        print("输入有误，请重新输入")
        messagebox.showinfo("Message", "输入有误，请重新输入")
        return  # continue
    if cmd == "view":
        reply = s.recv(1024).decode()
        print("1")
        if reply == "no":
            print("查询失败，没有这个学生")
            messagebox.showinfo("Message", "查询失败，没有这个学生")
            return
        num = s.recv(1024).decode()
        name = s.recv(1024).decode()
        print("学号:" + num + "姓名:" + name)
        messagebox.showinfo("Message", "学号:" + num + "姓名:" + name)
        pic = s.recv(1024 * 1024)
        dir = path + '/' + argc
        if not os.path.exists(dir):
            os.mkdir(dir)
        ftxt = open(path + '/' + argc + '/' + argc + '.txt', "w")
        ftxt.write(num)
        ftxt.write(name)
        ftxt.close()
        fjpg = open(path + '/' + argc + '/' + argc + '.jpg', "wb")
        fjpg.write(pic)
        fjpg.close()
        # 显示照片
        img = Image.open(path + '/' + argc + '/' + argc + '.jpg')
        img.show()

    if cmd == "delete":
        reply = s.recv(1024).decode()
        print(reply)
        messagebox.showinfo("Message", reply)

    if cmd == "add":
        reply = s.recv(1024).decode()
        if reply == "no":
            print("该学号学生已存在，无法添加；如需修改，请先删除")
            messagebox.showinfo("Message", "该学号学生已存在，无法添加；如需修改，请先删除")
        else:
            # addName = input("请输入要添加的学生名字： ").strip()
            addName = txt2.get()
            s.send(addName.encode())
            # picDir = input("请输入要添加的照片路径（以jpg文件）： ").strip()
            picDir = txt3.get()
            pic = open(picDir, "rb").read()
            s.send(pic)
            ans = s.recv(1024).decode()
            print(ans)
            messagebox.showinfo("Message", ans)


if __name__ == "__main__":
    s = socket.socket()  # 创建套接字
    s.connect(ip_port)  # 连接服务器
    print("create client: ")
    print(s)
    re = s.recv(1024).decode()  # 这里接受一个是否连接成功的请求
    print(re)

    window = Tk()  # NOQA
    window.title("Socket PJ")
    window.geometry("1280x720")
    # function选项
    lb0 = Label(window, text="功能：")  # NOQA
    lb0.grid(column=0, row=0, pady=25, sticky=W)
    combo = Combobox(window)  # NOQA
    combo['values'] = ("add", "delete", "view")
    combo.current(0)
    combo.grid(column=1, row=0, pady=25, sticky=W)
    # 学号
    lb1 = Label(window, text="学号：")  # NOQA
    lb1.grid(column=0, row=1, pady=25, sticky=W)
    txt1 = Entry(window, width=25)  # NOQA
    txt1.grid(column=1, row=1, pady=25, sticky=W)
    # 姓名
    lb2 = Label(window, text="姓名：")  # NOQA
    lb2.grid(column=0, row=2, pady=25, sticky=W)
    txt2 = Entry(window, width=25)  # NOQA
    txt2.grid(column=1, row=2, pady=25, sticky=W)
    # 照片位置
    lb3 = Label(window, text="本地照片地址：")  # NOQA
    lb3.grid(column=0, row=3, pady=25, sticky=W)
    txt3 = Entry(window, width=100)  # NOQA
    txt3.grid(column=1, row=3, pady=25, sticky=W)
    # run it
    btn = Button(window, text="Run", command=lambda: mainfunc(s))  # NOQA 传递参数
    btn.grid(column=1, row=10, pady=25, sticky=W)

    window.mainloop()

    # while True:
    #   mainfunc(s)
    s.close()
