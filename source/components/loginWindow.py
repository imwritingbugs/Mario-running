from tkinter import *
import tkinter.messagebox
from . import mydatabase as db

class LoginWindow():
    def __init__(self):
        self.loginwindow = Tk()
        self.loginwindow.title('login in')

        width = 300
        height = 150

        screenwidth = self.loginwindow.winfo_screenwidth()
        screenheight = self.loginwindow.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.loginwindow.geometry(alignstr)

        Label(self.loginwindow, text="用户名：", font=',10').grid(row=2, column=1)
        Label(self.loginwindow, text="密码：", font=',10').grid(row=3, column=1)
        self.entry1 = Entry(self.loginwindow)
        self.entry2 = Entry(self.loginwindow, show='*')
        self.entry1.grid(row=2, column=2)
        self.entry2.grid(row=3, column=2)

        Button(self.loginwindow, text='登录', command=self.loginIn, width=8, height=2).grid(row=4, column=1, sticky=W, padx=5,
                                                                                pady=5)
        Button(self.loginwindow, text='注册', command=self.register, width=8, height=2).grid(row=4, column=2, sticky=W, padx=5,
                                                                                 pady=5)
        Button(self.loginwindow, text='退出', command=self.quit, width=8, height=2).grid(row=4, column=3)
        self.loginwindow.resizable(width=False, height=True)
        self.loginwindow.mainloop()

    def loginIn(self):
        username=self.entry1.get()
        password=self.entry2.get()
        print(username)
        print(password)
        try:
            if(self.lengthControl(username, password)):
                info = db.login(username, password)
                if info == 'notfinduser':
                    self.wantToRegister(username, password)
                if info == 'wrongpassword':
                    tkinter.messagebox.showerror('错误','密码错误!')
                if info == 'loginsuccess':
                    tkinter.messagebox.showinfo('成功', '恭喜你成功登录!')
                    self.quit()
        except:
            tkinter.messagebox.showerror('错误', '连接失败!')

    def wantToRegister(self,username, password):
        result = tkinter.messagebox.askokcancel(title='是否注册', message='您尚未注册，是否要注册？')
        if result :
            print("yes")
            self.register()

    def register(self):
        username = self.entry1.get()
        password = self.entry2.get()
        print(username)
        print(password)
        if(self.lengthControl(username, password)):
            info = db.register(username, password)
            if info == 'alreadyexist':
                tkinter.messagebox.showerror('错误','已经存在该用户!')
            if info == 'registersuccess':
                tkinter.messagebox.showinfo('成功', '恭喜你成功注册!')
                self.quit()

    def lengthControl(self, username, password):
        if len(username) < 6:
            tkinter.messagebox.showwarning('警告', '用户名过短，请输入6-15个字符')
            return False
        if len(password) < 6:
            tkinter.messagebox.showwarning('警告', '密码过短，请输入6-15个字符')
            return False
        if len(username) > 16:
            tkinter.messagebox.showwarning('警告', '用户名过长，请输入6-15个字符')
            return False
        if len(username) > 16:
            tkinter.messagebox.showwarning('警告', '密码过长，请输入6-15个字符')
            return False
        return True

    def quit(self):
        self.loginwindow.withdraw()
        self.loginwindow.quit()
