# -*- coding: utf-8 -*-
import mysql.connector


class MyDB:
     def __init__(self , host="127.0.0.1", username="root", password="*****", port=3306, database="test"):
        '''类例化，处理一些连接操作'''
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.cur = None
        self.con = None
        # connect to mysql
        try:
            self.con = mysql.connector.connect(host = self.host, user = self.username, password = self.password, port = self.port, database = self.database)
            self.cur = self.con.cursor()
        except :
            print("DataBase connect error,please check the db config.")
            #raise "DataBase connect error,please check the db config."

     def close(self):
        '''结束查询和关闭连接'''
        self.con.close()

     def create_table(self,sql_str):
        '''创建数据表'''
        try:
            self.cur.execute(sql_str)
        except Exception as e:
            print(e)
     def query_formatrs(self,sql_str):
         '''查询数据，返回一个列表，里面的每一行是一个字典，带字段名
             cursor 为连接光标
             sql_str为查询语句
         '''
         try:
             self.cur.execute(sql_str)
             rows = self.cur.fetchall()
             r = []
             for x in rows:
                 r.append(dict(zip(self.cur.column_names,x)))

             return r
         except:
             return False

     def query(self,sql_str):
        '''查询数据并返回
             cursor 为连接光标
             sql_str为查询语句
        '''
        try:

            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            return rows
        except:
            return False

     def execute_update_insert(self,sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.lastrowid

if __name__ == "__main__":
    mydb = MyDB()
    #创建表
    mydb.create_table('create table user (id varchar(20) primary key, name varchar(20))')
    #插入数据
    mydb.execute_update_insert("insert into user (id, name) values  ('1', 'Michael')")
    # 查询数据表
    mydb_new = MyDB()
    results = mydb.query("SELECT * FROM detailinfo")
    print(results)
    for row in results:
        productname = row[0]
        supportname = row[1]
        productinterface = row[2]
        print("productname=%s,supportname=%s,productinterface=%s" % \
               (productname, supportname, productinterface))
    list = mydb.query_formatrs("SELECT * FROM detailinfo")
    for i in list:
        print ("记录号：%s   值：%s" % (list.index(i) + 1, i))
    #关闭数据库
    mydb.close()
