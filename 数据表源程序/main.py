import xlrd
import pymysql

for i in range(1, 4):
    # 创建连接
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='Yqyq7878',
        database='library', charset='utf8'
    )
    # 获取游标对象
    cur = conn.cursor()
    if (i == 1):
        sql = 'insert into Lad(账号, 密码, 备注) values(%s, %s, %s)'
        filename = '管理员信息表.xls'
    elif (i == 2):
        sql = 'insert into LReader(借书证号, 姓名, 性别, 出生时间, 借书量, 联系方式, 备注) values(%s, %s, %s, %s, %s, %s, %s)'
        filename = '读者信息表.xls'
    elif (i == 3):
        sql = 'insert into LBook(图书ID, 书名, 作者, 出版社, 出版年月, 价格, 是否借出, 借书证号) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        filename = '图书信息表.xls'
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name('Sheet1')
    if (i == 1):
        for r in range(1, sheet.nrows):
            values = (sheet.cell(r, 0).value, sheet.cell(r, 1).value, sheet.cell(r, 2).value)
            cur.execute(sql, values)
        conn.commit()
    elif (i == 2):
        for r in range(1, sheet.nrows):
            values = (sheet.cell(r, 0).value, sheet.cell(r, 1).value, sheet.cell(r, 2).value, sheet.cell(r, 3).value,
                      sheet.cell(r, 4).value, sheet.cell(r, 5).value, sheet.cell(r, 6).value)
            cur.execute(sql, values)
        conn.commit()
    elif (i == 3):
        for r in range(1, sheet.nrows):
            values = (sheet.cell(r, 0).value, sheet.cell(r, 1).value, sheet.cell(r, 2).value, sheet.cell(r, 3).value,
                      sheet.cell(r, 4).value, sheet.cell(r, 5).value, sheet.cell(r, 6).value, sheet.cell(r, 7).value)
            cur.execute(sql, values)
        conn.commit()
    cur.close()
    conn.close()