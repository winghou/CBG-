# -*- coding: utf-8 -*-
from db import MyDB

class selec:
    def __init__(self):
        self.db_host = '*****'
        self.db_port = '3306'
        self.db_db = 'fee'
        self.db_user = '********'
        self.db_pwd = '*******'
        self.db = self.init_db()



    def init_db(self):
        db = MyDB(host=self.db_host,port=self.db_port,username=self.db_user,password=self.db_pwd,database=self.db_db)
        #print(dir(db))
        return db

    def init_data(self):
        sql = "select * from lgz_search where `delete`=0 "
        data = self.db.query_formatrs(sql)
        return  data


