import pymysql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import tkinter.messagebox as messagebox
import time

Permissions = False  # 超级管理权限
sqlUser = 'root'  # 数据库账户
sqlPwd = 'Yqyq7878'  # 数据库密码


class MainInterface:
    """主界面"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('MainInterface')
        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        def getTime():
            timeStr = time.strftime('%H:%M:%S')
            Rtime.configure(text=timeStr)
            self.window.after(1000, getTime)

        Rtime = Label(self.window, text='')
        Rtime.pack(pady=25)
        getTime()

        labelOne = Label(self.window, text='图书馆管理系统', font=("华文中宋", 40))
        labelTwo = Label(self.window,
                         text='                                                                               by 杨钦',
                         font=('华文中宋', 10))
        labelOne.pack(pady=100)  # pady=100 界面的长度
        labelTwo.pack(pady=100)  # pady=100 界面的长度

        # 按钮
        Button(self.window, text='登录', font=tkFont.Font(size=16), command=lambda: LoginInterface(self.window),
               width=20, height=2, fg='white', bg='gray').place(x=100, y=300)
        Button(self.window, text='退出', font=tkFont.Font(size=16), command=self.window.destroy, width=20, height=2,
               fg='white', bg='gray').place(x=400, y=300)

        self.window.mainloop()


class LoginInterface:
    """登录界面"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('LoginInterface')
        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        label = tk.Label(self.window, text='登录', bg='SkyBlue', font=('华文中宋', 20), width=70, height=2)
        label.pack()

        Label(self.window, text='账号', font=('华文中宋', 14)).pack(pady=25)
        self.account = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory')
        self.account.pack()

        Label(self.window, text='密码', font=('华文中宋', 14)).pack(pady=25)
        self.password = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.password.pack()

        Button(self.window, text='登录', width=8, font=tkFont.Font(size=12), command=self.login).pack(pady=40)
        Button(self.window, text='返回', width=8, font=tkFont.Font(size=12), command=self.back).pack()

    def login(self):
        _password = None

        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select 账号, 密码, 备注 from Lad where 账号 = '%s'" % (self.account.get())  # 查询管理员账号密码
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                _account = row[0]
                _password = row[1]
                _remark = row[2]
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '账号或密码不正确！')
        conn.close()

        if self.account.get() == _account and self.password.get() == _password:
            # 如果登录的是超级管理员账号，赋予超级管理员权限
            if _remark == '超级管理员':
                global Permissions
                Permissions = True
            ActionSelectionInterface(self.window)
        else:
            messagebox.showinfo('警告！', '账号或密码不正确！')

    def back(self):
        MainInterface(self.window)


class ActionSelectionInterface:
    """操作选择界面"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('ActionSelectionInterface')

        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        label = tk.Label(self.window, text='选择要进行的操作', bg='SkyBlue', font=('华文中宋', 20), width=70, height=2)
        label.pack(pady=100)

        # 按钮
        self.button1 = ttk.Button(text='操作图书信息', width=30,
                                  command=lambda: BookInformationOperation(self.window)).pack(pady=10)
        self.button2 = ttk.Button(text='操作读者信息', width=30,
                                  command=lambda: ReaderInformationOperation(self.window)).pack(pady=10)
        if Permissions == True:
            self.button3 = ttk.Button(text='操作管理员信息', width=30,
                                      command=lambda: ADInformationOperation(self.window)).pack(pady=10)
        self.button4 = ttk.Button(text='返回', width=30, command=self.back).pack(pady=10)

        self.window.mainloop()

    def back(self):
        global Permissions
        Permissions = False
        LoginInterface(self.window)


class BookInformationOperation:
    """图书信息操作界面(含删除操作)"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = Tk()
        self.window.title('OperatorInterface')
        wdWidth = 650
        wdHeigh = 700
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
        self.start

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=200)
        self.frameCenter = tk.Frame(width=600, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.varID = StringVar()  # 图书ID
        self.varBookName = StringVar()  # 书名
        self.varAuthor = StringVar()  # 作者
        self.varPublishingHouse = StringVar()  # 出版社
        self.varTime = StringVar()  # 出版年月
        self.varPrice = StringVar()  # 价格
        self.varWhether = StringVar()  # 是否借出
        self.varCertificate = StringVar()  # 借书证号

        self.rightTopBookNameLabel = Label(self.frameLeftTop, text='请输入书名', font=('华文中宋', 15))
        self.rightTopBookNameEntry = Entry(self.frameLeftTop, textvariable=self.varBookName, font=('Verdana', 15))
        self.rightTopBookNameButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopBookNameLabel.grid(row=1, column=1)  # 位置信
        self.rightTopBookNameEntry.grid(row=2, column=1)
        self.rightTopBookNameButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('图书ID', '书名', '作者', '出版社', '出版年月', '价格', '是否借出', '借书证号')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格标题
        self.tree.column('图书ID', width=50, anchor='center')
        self.tree.column('书名', width=75, anchor='center')
        self.tree.column("作者", width=75, anchor='center')
        self.tree.column("出版社", width=100, anchor='center')
        self.tree.column("出版年月", width=100, anchor='center')
        self.tree.column("价格", width=50, anchor='center')
        self.tree.column("是否借出", width=75, anchor='center')
        self.tree.column("借书证号", width=75, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)

        self.id = []
        self.name = []
        self.author = []
        self.publishingHouse = []
        self.time = []
        self.price = []
        self.whether = []
        self.certificate = []
        # 数据库操作 查询图书信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from LBook"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.author.append(row[2])
                self.publishingHouse.append(row[3])
                self.time.append(row[4])
                self.price.append(row[5])
                self.whether.append(row[6])
                self.certificate.append(row[7])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()
        for i in range(len(self.id)):
            self.tree.insert('', i, values=(
            self.id[i], self.name[i], self.author[i], self.publishingHouse[i], self.time[i], self.price[i],
            self.whether[i], self.certificate[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=('华文中宋', 18))

        self.tree.bind('<Button-1>', self.click)
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加图书', width=20,
                                          command=lambda: AddBook(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选中图书', width=20,
                                          command=lambda: EditBookInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中图书', width=20, command=self.delRow)

        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)

        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(0)
        self.frameRightTop.grid_propagate(0)
        self.frameCenter.grid_propagate(0)
        self.frameBottom.grid_propagate(0)

        self.frameLeftTop.tkraise()
        self.frameRightTop.tkraise()
        self.frameCenter.tkraise()
        self.frameBottom.tkraise()

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def find(self):
        FindBookInformation(self.window, self.rightTopBookNameEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条图书信息')
        else:
            # 数据库操作 查询图书信息表
            conn = pymysql.connect(
                host='127.0.0.1', port=3306,
                user=sqlUser, passwd=sqlPwd,
                database='library', charset='utf8'
            )
            cursor = conn.cursor()
            sql = "delete from LBook where 图书ID = '%s'" % (self.rowInfo[0])
            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt == True:
                    if self.rowInfo[6] == '是':
                        messagebox.showinfo('警告！', '该图书已被借出，无法删除！')
                    else:
                        cursor.execute(sql)
                        conn.commit()
                        idIndex = self.id.index(self.rowInfo[0])
                        del self.id[idIndex]
                        del self.name[idIndex]
                        del self.author[idIndex]
                        del self.publishingHouse[idIndex]
                        del self.time[idIndex]
                        del self.price[idIndex]
                        del self.whether[idIndex]
                        del self.certificate[idIndex]
                        self.tree.delete(self.tree.selection()[0])
                        messagebox.showinfo('提示！', '删除成功！')
            except:
                conn.rollback
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()
            file = open('a.txt', 'r+')
            file.seek(0)
            file.truncate()
            file.close()
            file = open('a.txt', 'w+')
            file.write('未选中')
            file.close()



class ReaderInformationOperation:
    """读者信息操作界面(含删除操作)"""

    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁登录界面
        self.window = Tk()
        self.window.title('ReaderInformationOperation')
        wdWidth = 650
        wdHeigh = 700
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
        self.start

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=200)
        self.frameCenter = tk.Frame(width=500, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.varCertificate = StringVar()  # 借书证号
        self.varName = StringVar()  # 姓名
        self.varSex = StringVar()  # 性别
        self.varData = StringVar()  # 出生时间
        self.varMeasure = StringVar()  # 借书量
        self.varNumber = StringVar()  # 联系方式
        self.varremark = StringVar()  # 备注

        self.rightTopNameLabel = Label(self.frameLeftTop, text='请输入姓名', font=('华文中宋', 15))
        self.rightTopNameEntry = Entry(self.frameLeftTop, textvariable=self.varName, font=('Verdana', 15))
        self.rightTopNameButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopNameLabel.grid(row=1, column=1)  # 位置信息
        self.rightTopNameEntry.grid(row=2, column=1)
        self.rightTopNameButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('借书证号', '姓名', '性别', '出生时间', '借书量', '联系方式', '备注')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('借书证号', width=75, anchor='center')
        self.tree.column('姓名', width=75, anchor='center')
        self.tree.column("性别", width=50, anchor='center')
        self.tree.column("出生时间", width=100, anchor='center')
        self.tree.column("借书量", width=50, anchor='center')
        self.tree.column("联系方式", width=100, anchor='center')
        self.tree.column("备注", width=50, anchor='center')

        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)

        self.certificate = []
        self.name = []
        self.sex = []
        self.data = []
        self.measure = []
        self.number = []
        self.remark = []
        # 数据库操作 查询读者信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from LReader"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.certificate.append(row[0])
                self.name.append(row[1])
                self.sex.append(row[2])
                self.data.append(row[3])
                self.measure.append(row[4])
                self.number.append(row[5])
                self.remark.append(row[6])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()

        for i in range(len(self.certificate)):
            self.tree.insert('', i, values=(
            self.certificate[i], self.name[i], self.sex[i], self.data[i], self.measure[i], self.number[i],
            self.remark[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=('华文中宋', 18))

        self.tree.bind('<Button-1>', self.click)
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加读者', width=20,
                                          command=lambda: AddReader(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选中读者', width=20,
                                          command=lambda: EditReaderInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中读者', width=20, command=self.delRow)

        # 位置设置
        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(0)
        self.frameRightTop.grid_propagate(0)
        self.frameCenter.grid_propagate(0)
        self.frameBottom.grid_propagate(0)

        self.frameLeftTop.tkraise()
        self.frameRightTop.tkraise()
        self.frameCenter.tkraise()
        self.frameBottom.tkraise()

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def find(self):
        FindReaderInformation(self.window, self.rightTopNameEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)
        self.row = self.tree.identify_row(event.y)
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条读者信息')
        else:
            # 数据库操作 查询读者信息表
            conn = pymysql.connect(
                host='127.0.0.1', port=3306,
                user=sqlUser, passwd=sqlPwd,
                database='library', charset='utf8'
            )
            cursor = conn.cursor()
            sql = "delete from LReader where 借书证号 = '%s'" % (self.rowInfo[0])
            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt == True:
                    con = int(self.rowInfo[4])
                    if con > 0:
                        messagebox.showinfo('警告！', '该读者有借书未归还，无法删除！')
                    else:
                        cursor.execute(sql)
                        conn.commit()
                        idIndex = self.id.index(self.rowInfo[0])
                        del self.certificate[idIndex]
                        del self.name[idIndex]
                        del self.sex[idIndex]
                        del self.data[idIndex]
                        del self.measure[idIndex]
                        del self.number[idIndex]
                        del self.remark[idIndex]
                        self.tree.delete(self.tree.selection()[0])
                        messagebox.showinfo('提示！', '删除成功！')
            except:
                conn.rollback
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()
            file = open('a.txt', 'r+')
            file.seek(0)
            file.truncate()
            file.close()
            file = open('a.txt', 'w+')
            file.write('未选中')
            file.close()


class ADInformationOperation:
    """管理员信息操作界面(含删除操作)"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = Tk()
        self.window.title('ADInformationOperation')
        wdWidth = 650
        wdHeigh = 700
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
        self.start

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=200)
        self.frameCenter = tk.Frame(width=450, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.varAccount = StringVar()  # 账号
        self.varPassword = StringVar()  # 密码
        self.varRemark = StringVar()  #备注

        self.rightTopAccountLabel = Label(self.frameLeftTop, text='请输入账号', font=('华文中宋', 15))
        self.rightTopAccountEntry = Entry(self.frameLeftTop, textvariable=self.varAccount, font=('Verdana', 15))
        self.rightTopAccountButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopAccountLabel.grid(row=1, column=1)
        self.rightTopAccountEntry.grid(row=2, column=1)
        self.rightTopAccountButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('账号', '密码', '备注')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('账号', width=150, anchor='center')
        self.tree.column('密码', width=150, anchor='center')
        self.tree.column("备注", width=150, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)

        self.account = []
        self.password = []
        self.remark = []
        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from Lad"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.account.append(row[0])
                self.password.append(row[1])
                self.remark.append(row[2])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()
        for i in range(len(self.account)):
            self.tree.insert('', i, values=(self.account[i], self.password[i], self.remark[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        # 定义右上方区域
        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=('华文中宋', 18))

        self.tree.bind('<Button-1>', self.click)
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加管理员', width=20,
                                          command=lambda: AddAD(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选择管理员密码', width=20,
                                          command=lambda: EditADInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中管理员', width=20, command=self.delRow)

        # 位置设置
        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(0)
        self.frameRightTop.grid_propagate(0)
        self.frameCenter.grid_propagate(0)
        self.frameBottom.grid_propagate(0)

        self.frameLeftTop.tkraise()
        self.frameRightTop.tkraise()
        self.frameCenter.tkraise()
        self.frameBottom.tkraise()

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def find(self):
        FindADInformation(self.window, self.rightTopAccountEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)
        self.row = self.tree.identify_row(event.y)
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条管理员信息')
        else:
            # 数据库操作 查询管理员信息表
            conn = pymysql.connect(
                host='127.0.0.1', port=3306,
                user=sqlUser, passwd=sqlPwd,
                database='library', charset='utf8'
            )
            cursor = conn.cursor()
            sql = "delete from Lad where 账号 = '%s'" % (self.rowInfo[0])
            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt == True:
                    if self.rowInfo[2] == '超级管理员':
                        messagebox.showinfo('警告！', '不能删除超级管理员账户！')
                    else:
                        cursor.execute(sql)
                        conn.commit()
                        idIndex = self.id.index(self.rowInfo[0])
                        del self.account[idIndex]
                        del self.password[idIndex]
                        del self.remark[idIndex]
                        self.tree.delete(self.tree.selection()[0])  # 删除所选行
                        messagebox.showinfo('提示！', '删除成功！')
            except:
                conn.rollback
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()
            file = open('a.txt', 'r+')
            file.seek(0)
            file.truncate()
            file.close()
            file = open('a.txt', 'w+')
            file.write('未选中')
            file.close()


class FindBookInformation:
    """查找图书信息"""

    def __init__(self, subInterface, NAME):
        self.id = '图书ID：' + ' '
        self.name = '书名：' + ' '
        self.author = '作者：' + ' '
        self.publishingHouse = '出版社：' + ' '
        self.time = '出版年月：' + ' '
        self.price = '价格：' + ' '
        self.whether = '是否借出：' + ''
        self.certificate = '借书证号：' + ' '

        # 数据库操作 查询图书信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from LBook where 书名 = '%s'" % (NAME)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.id = '图书ID：' + row[0]
                self.name = '书名：' + row[1]
                self.author = '作者：' + row[2]
                self.publishingHouse = '出版社：' + row[3]
                self.time = '出版年月：' + row[4]
                self.price = '价格：' + row[5]
                self.whether = '是否借出：' + row[6]
                self.certificate = '借书证号：' + row[7]
        except:
            print("Error: unable to fecth data")
        conn.close()
        if NAME == '':
            messagebox.showinfo('警告！', '请输入书名！')
        elif self.id == '图书ID：' + ' ':
            messagebox.showinfo('警告！', '找不到这本图书！')
        else:
            self.window = tk.Tk()
            self.window.title('FindBookInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
            label = tk.Label(self.window, text='图书信息搜索结果', bg='SkyBlue', font=('华文中宋', 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.id, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.name, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.author, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.publishingHouse, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.time, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.price, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.whether, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.certificate, font=('华文中宋', 18)).pack(pady=5)
            self.window.mainloop()


class FindReaderInformation:
    """查找读者信息"""

    def __init__(self, subInterface, NAME):
        self.certificate = '借书证号：' + ' '
        self.name = '姓名：' + ' '
        self.sex = '性别：' + ' '
        self.data = '出生时间：' + ' '
        self.measure = '借书量：' + ' '
        self.number = '联系方式：' + ' '

        # 数据库操作 查询读者信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select 借书证号, 姓名, 性别, 出生时间, 借书量, 联系方式 from LReader where 姓名 = '%s'" % (
            NAME)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.certificate = '借书证号：' + row[0]
                self.name = '姓名：' + row[1]
                self.sex = '性别：' + row[2]
                self.data = '出生时间：' + row[3]
                self.measure = '借书量：' + row[4]
                self.number = '联系方式：' + row[5]
        except:
            print("Error: unable to fecth data")
        conn.close()
        if NAME == '':
            messagebox.showinfo('警告！', '请输入姓名！')
        elif self.certificate == '借书证号：' + ' ':
            messagebox.showinfo('警告！', '找不到这名读者！')
        else:
            self.window = tk.Tk()
            self.window.title('FindReaderInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
            label = tk.Label(self.window, text='读者信息搜索结果', bg='SkyBlue', font=('华文中宋', 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.certificate, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.name, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.sex, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.data, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.measure, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.number, font=('华文中宋', 18)).pack(pady=5)
            self.window.mainloop()


class FindADInformation:
    """查找管理员信息"""

    def __init__(self, subInterface, ACCOUNT):
        self.account = '账号：' + ' '
        self.password = '密码：' + ' '
        self.remark = '备注：' + ' '

        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from Lad where 账号 = '%s'" % (ACCOUNT)  # 查询该账号的所有信息
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.account = '账号：' + row[0]
                self.password = '密码：' + row[1]
                self.remark = '备注：' + row[2]
        except:
            print("Error: unable to fecth data")
        conn.close()
        if ACCOUNT == '':
            messagebox.showinfo('警告！', '请输入账号！')
        elif self.account == '账号：' + ' ':
            messagebox.showinfo('警告！', '找不到这个账号！')
        else:
            self.window = tk.Tk()
            self.window.title('FindADInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))
            label = tk.Label(self.window, text='管理员信息搜索结果', bg='SkyBlue', font=('华文中宋', 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.account, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.password, font=('华文中宋', 18)).pack(pady=5)
            Label(self.window, text=self.remark, font=('华文中宋', 18)).pack(pady=5)
            self.window.mainloop()


class AddBook:
    """添加图书"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('AddBook')
        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        self.TopTitle = Label(self.window, text='添加图书', bg='SkyBlue', font=('华文中宋', 20), width=70, height=2)
        self.TopTitle.pack()

        self.varID = StringVar()  #声明图书ID
        self.varBookName = StringVar()  # 书名
        self.varAuthor = StringVar()  # 作者
        self.varPublishingHouse = StringVar()  # 出版社
        self.varTime = StringVar()  # 出版年月
        self.varPrice = StringVar()  # 价格
        # 图书ID
        self.rightTopIdLabel = Label(text='图书ID：（格式：PXXXX）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopIdEntry = Entry(textvariable=self.varID, font=('华文中宋', 10)).pack()
        # 书名
        self.rightTopBookNameLabel = Label(text='书名：', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopBookNameEntry = Entry(textvariable=self.varBookName, font=('华文中宋', 10)).pack()
        # 作者
        self.rightTopAuthorLabel = Label(text='作者：', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopAuthorEntry = Entry(textvariable=self.varAuthor, font=('华文中宋', 10)).pack()
        # 出版社
        self.rightTopPublishingHouseLabel = Label(text='出版社：', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopPublishingHouseEntry = Entry(textvariable=self.varPublishingHouse, font=('华文中宋', 10)).pack()
        # 出版年月
        self.rightTopTimeLabel = Label(text='出版年月：（格式：XXXX-XX-XX）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopTimeEntry = Entry(textvariable=self.varTime, font=('华文中宋', 10)).pack()
        # 价格
        self.rightTopPriceLabel = Label(text='价格：', font=('华文中宋', 10)).pack(pady=10)
        self.rigthTopPriceEntry = Entry(textvariable=self.varPrice, font=('华文中宋', 10)).pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add).pack(pady=30)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)

        self.id = []
        self.bookName = []
        self.author = []
        self.publishingHouse = []
        self.time = []
        self.price = []
        self.whether = []
        self.certificate = []
        # 数据库操作 查询图书信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from LBook"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.bookName.append(row[1])
                self.author.append(row[2])
                self.publishingHouse.append(row[3])
                self.time.append(row[4])
                self.price.append(row[5])
                self.whether.append(row[6])
                self.certificate.append(row[7])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()

    def back(self):
        BookInformationOperation(self.window)

    def Add(self):
        if str(self.varID.get()) in self.id or str(self.varBookName.get()) in self.bookName:
            messagebox.showinfo('警告！', '该图书已存在！')
        else:
            if self.varID.get() != '' and self.varBookName.get() != '' and self.varAuthor.get() != '' and self.varPublishingHouse.get() != '' and self.varTime.get() != '' and self.varPrice.get() != '':
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "insert into LBook(图书ID, 书名, 作者, 出版社, 出版年月, 价格) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.varID.get(), self.varBookName.get(), self.varAuthor.get(), self.varPublishingHouse.get(),
                self.varTime.get(), self.varPrice.get())
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()


class AddReader:
    """添加读者"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('AddReader')
        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        self.TopTitle = Label(self.window, text='添加读者', bg='SkyBlue', font=('华文中宋', 20), width=70, height=2)
        self.TopTitle.pack()

        self.varCertificate = StringVar()  # 借书证号
        self.varName = StringVar()  # 姓名
        self.varSex = StringVar()  # 性别
        self.varData = StringVar()  # 出生时间
        self.varMeasure = StringVar()  # 借书量
        self.varNumber = StringVar()  # 联系方式
        # 借书证号
        self.rightTopCertificateLabel = Label(text='借书证号：（格式：PXXX）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopCertificateEntry = Entry(textvariable=self.varCertificate, font=('华文中宋', 10)).pack()
        # 姓名
        self.rightTopNameLabel = Label(text='姓名：', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopNameEntry = Entry(textvariable=self.varName, font=('华文中宋', 10)).pack()
        # 性别
        self.rightTopSexLabel = Label(text='性别：（格式：填‘男’或‘女’）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopSexEntry = Entry(textvariable=self.varSex, font=('华文中宋', 10)).pack()
        # 出生时间
        self.rightTopDataLabel = Label(text='出生时间：（格式：XXXX-XX-XX）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopDataEntry = Entry(textvariable=self.varData, font=('华文中宋', 10)).pack()
        # 联系方式
        self.rightTopNumberLabel = Label(text='联系方式：(格式：电话号码或手机号码)', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopNumberEntry = Entry(textvariable=self.varNumber, font=('华文中宋', 10)).pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add).pack(pady=30)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)

        self.certificate = []
        self.name = []
        self.sex = []
        self.data = []
        self.measure = []
        self.number = []
        self.remark = []
        # 数据库操作 查询读者信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from LReader"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.certificate.append(row[0])
                self.name.append(row[1])
                self.sex.append(row[2])
                self.data.append(row[3])
                self.measure.append(row[4])
                self.number.append(row[5])
                self.remark.append(row[6])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()

    def back(self):
        ReaderInformationOperation(self.window)

    def Add(self):
        if str(self.varCertificate.get()) in self.certificate:
            messagebox.showinfo('警告！', '该读者已存在！')
        else:
            if self.varCertificate.get() != '' and self.varName.get() != '' and self.varSex.get() != '' and self.varData.get() != '' and self.varMeasure.get() != '' and self.varNumber.get() != '':
                # 数据库操作 查询读者信息表
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "insert into LReader(借书证号, 姓名, 性别, 出生时间, 借书量, 联系方式) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.varCertificate.get(), self.varName.get(), self.varSex.get(), self.varData.get(),
                self.varMeasure.get(), self.varNumber.get())
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()


class AddAD:
    """添加管理员"""

    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title('AddAD')
        wdWidth = 700
        wdHeigh = 600
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

        self.TopTitle = Label(self.window, text='添加管理员', bg='SkyBlue', font=('华文中宋', 20), width=70, height=2)
        self.TopTitle.pack()

        self.varAccount = StringVar()  # 账号
        self.varPassword = StringVar()  # 密码
        self.varRemark = StringVar()  # 备注
        # 账号
        self.rightTopAccountLabel = Label(text='账号：（格式：XXXXXXX）', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopAccountEntry = Entry(textvariable=self.varAccount, font=('华文中宋', 10)).pack()
        # 密码
        self.rightTopPasswordLabel = Label(text='密码：', font=('华文中宋', 10)).pack(pady=10)
        self.rightTopPasswordEntry = Entry(textvariable=self.varPassword, font=('华文中宋', 10)).pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add).pack(pady=30)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)

        self.account = []
        self.password = []
        self.remark = []
        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user=sqlUser, passwd=sqlPwd,
            database='library', charset='utf8'
        )
        cursor = conn.cursor()
        sql = "select * from Lad"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.account.append(row[0])
                self.password.append(row[1])
                self.remark.append(row[2])
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()

    def back(self):
        ADInformationOperation(self.window)

    def Add(self):
        if str(self.varAccount.get()) in self.account:
            messagebox.showinfo('警告！', '该管理员已存在！')
        else:
            if self.varAccount.get() != '' and self.varPassword.get() != '':
                # 数据库操作 查询管理员信息表
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "insert into Lad(账号, 密码, 备注) values ('%s', '%s', '%s')" % (
                self.varAccount.get(), self.varPassword.get(), '普通管理员')
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()


class EditBookInformation:
    """修改图书信息"""

    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条图书信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title('EditBookInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

            self.topTitle = Label(self.window, text='输入新的图书信息', bg='SkyBlue', font=('华文中宋', 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.varID = StringVar()  # 图书ID
            self.varBookName = StringVar()  # 书名
            self.varAuthor = StringVar()  # 作者
            self.varPublishingHouse = StringVar()  # 出版社
            self.varTime = StringVar()  # 出版年月
            self.varPrice = StringVar()  # 价格

            # 图书ID
            self.idLabel = Label(text='图书ID（不可修改）：（格式：PXXXX）', font=('华文中宋', 10)).pack(pady=10)
            self.idEntry = Entry(textvariable=self.varID, font=('华文中宋', 10)).pack()
            # 书名
            self.nameLabel = Label(text='书名：', font=('华文中宋', 10)).pack(pady=10)
            self.nameEntry = Entry(textvariable=self.varBookName, font=('华文中宋', 10)).pack()
            # 作者
            self.authorLabel = Label(text='作者：', font=('华文中宋', 10)).pack(pady=10)
            self.authorEntry = Entry(textvariable=self.varAuthor, font=('华文中宋', 10)).pack()
            # 出版社
            self.publishingHouseLabel = Label(text='出版社：', font=('华文中宋', 10)).pack(pady=10)
            self.publishingHouseEntry = Entry(textvariable=self.varPublishingHouse, font=('华文中宋', 10)).pack()
            # 出版年月
            self.timeLabel = Label(text='出版年月：（格式：XXXX-XX-XX）', font=('华文中宋', 10)).pack(pady=10)
            self.timeEntry = Entry(textvariable=self.varTime, font=('华文中宋', 10)).pack()
            # 价格
            self.priceLabel = Label(text='价格：', font=('华文中宋', 10)).pack(pady=10)
            self.priceEntry = Entry(textvariable=self.varPrice, font=('华文中宋', 10)).pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.updata).pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back).pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        BookInformationOperation(self.window)
    def updata(self):
        self.id = StringVar()
        file = open('a.txt', 'r')
        self.id = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt == True:
            if self.varID.get() == self.id and self.varID.get() != '' and self.varBookName.get() != '' and self.varAuthor.get() != '' and self.varPublishingHouse.get() != '' and self.varTime.get() != '' and self.varPrice.get() != '':
                # 数据库操作 查询图书信息表
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "update LBook set 书名 = '%s', 作者 = '%s', 出版社 = '%s', 出版年月 = '%s', 价格 = '%s' where 图书ID = '%s'" % (
                self.varBookName.get(), self.varAuthor.get(), self.varPublishingHouse.get(), self.varTime.get(),
                self.varPrice.get(), self.varID.get())
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()
            else:
                messagebox.showinfo('警告！', '图书ID不可修改且输入完整数据！')


class EditReaderInformation:
    """修改读者信息"""

    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条读者信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title('EditReaderInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

            self.topTitle = Label(self.window, text='输入新的读者信息', bg='SkyBlue', font=('华文中宋', 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.varCertificate = StringVar()  # 借书证号
            self.varName = StringVar()  # 姓名
            self.varSex = StringVar()  # 性别
            self.varData = StringVar()  # 出生时间
            self.varNumber = StringVar()  # 联系方式

            # 借书证号
            self.certificateLabel = Label(text='借书证号（不可修改）：（格式：PXXX）', font=('华文中宋', 10)).pack(pady=10)
            self.certificateEntry = Entry(textvariable=self.varCertificate, font=('华文中宋', 10)).pack()
            # 姓名
            self.nameLabel = Label(text='姓名：', font=('华文中宋', 10)).pack(pady=10)
            self.nameEntry = Entry(textvariable=self.varName, font=('华文中宋', 10)).pack()
            # 性别
            self.sexLabel = Label(text='性别：', font=('华文中宋', 10)).pack(pady=10)
            self.sexEntry = Entry(textvariable=self.varSex, font=('华文中宋', 10)).pack()
            # 出生时间
            self.dataLabel = Label(text='出生时间：（格式：XXXX-XX-XX）', font=('华文中宋', 10)).pack(pady=10)
            self.dataEntry = Entry(textvariable=self.varData, font=('华文中宋', 10)).pack()
            # 联系方式
            self.numberLabel = Label(text='联系方式：(格式：电话号码或手机号码)', font=('华文中宋', 10)).pack(pady=10)
            self.numberEntry = Entry(textvariable=self.varNumber, font=('华文中宋', 10)).pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.updata).pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back).pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        ReaderInformationOperation(self.window)

    def updata(self):
        self.certificate = StringVar()
        file = open('a.txt', 'r')
        self.certificate = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt == True:
            if self.varCertificate.get() == self.certificate and self.varCertificate.get() != '' and self.varName.get() != '' and self.varSex.get() != '' and self.varData.get() != '' and self.varNumber.get() != '':
                # 数据库操作 查询读者信息表
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "update LReader set 姓名 = '%s', 性别 = '%s', 出生时间 = '%s', 联系方式 = '%s' where 借书证号 = '%s'" % (
                self.varName.get(), self.varSex.get(), self.varData.get(), self.varNumber.get(),
                self.varCertificate.get())
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()
            else:
                messagebox.showinfo('警告！', '借书证号不可修改且输入完整数据！')


class EditADInformation:
    """修改管理员信息"""

    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条管理员信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title('EditADInformation')
            wdWidth = 700
            wdHeigh = 600
            screenWidth = self.window.winfo_screenwidth()
            screenHeight = self.window.winfo_screenheight()
            self.window.geometry(
                '%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

            self.topTitle = Label(self.window, text='输入新的密码', bg='SkyBlue', font=('华文中宋', 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.varPassword = StringVar()

            self.passwordLabel = Label(text='密码：（格式：不可超过16位）', font=('华文中宋', 10)).pack(pady=10)
            self.passwordEntry = Entry(textvariable=self.varPassword, font=('华文中宋', 10)).pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.updata).pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back).pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        ADInformationOperation(self.window)

    def updata(self):
        self.account = StringVar()
        file = open('a.txt', 'r')
        self.account = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt == True:
            if self.varPassword.get() != '':
                # 数据库操作 查询管理员信息表
                conn = pymysql.connect(
                    host='127.0.0.1', port=3306,
                    user=sqlUser, passwd=sqlPwd,
                    database='library', charset='utf8'
                )
                cursor = conn.cursor()
                sql = "update Lad set 密码 = '%s' where 账号 = '%s'" % (
                self.varPassword.get(), self.account)
                try:
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except:
                    conn.rollback()
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()
            else:
                messagebox.showinfo('警告！', '请输入新的密码！')


def main():
        window = tk.Tk()
        MainInterface(window)
if __name__ == '__main__':
    main()