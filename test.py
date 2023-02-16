import datetime
import pymysql


def dbConnector(cmd,fetchtype):
    # fetchtype is fetchall or fetchone
    DBUserName = "root"
    DBName = "measure"
    password = ""
    
    conn = pymysql.Connect(host="localhost",port=3306,user = DBUserName,password="",db = DBName,autocommit=True)
    cur = conn.cursor()
    
    cur.execute(cmd)

    if fetchtype == 'fetchall':
        return cur.fetchall()

    
def generatingOrder():
    idList = []
    date = datetime.datetime.today().strftime("%y") + datetime.datetime.today().strftime("%m")
    print("SELECT order_id FROM order_table where order_id LIKE '2212%';")
    cmd = "SELECT order_id FROM order_table WHERE order_id LIKE '{}'".format(date+'%')
    print(cmd)
    cmd = "SELECT order_id FROM order_table where order_id LIKE '2312%';"
    data = dbConnector(cmd,'fetchall')
    if data :   
        for da in data:
            if da[0].startswith(date):
                idList.append(da[0])
        if idList:
            max_ = max([int(x) for x in idList])
            return max_+1
    else:
        return date+ '001'





print(generatingOrder())
