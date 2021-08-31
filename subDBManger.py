#-*- codeing = utf-8 -*-
#@Time :  
#@Author: Mianbao
#@File : subDBManger.py
#@Software : PyCharm
import sqlite3
import os

class subtitle_db():
    def __init__(self):
        self.MovieDBPath = 'subtitle.sqlite'
        # 只有sqlite文件不存在时才创建该文件。
        if not os.path.exists(self.MovieDBPath):
            # 创建SQLite数据库
            self.conn = sqlite3.connect(self.MovieDBPath,check_same_thread=False)
            #获取sqlite3.Cursor对象
            self.cur = self.conn.cursor()
            #创建数据表
            self.cur.execute("DROP TABLE IF EXISTS NAMEINFORMATION")
            self.cur.execute('''CREATE TABLE NAMEINFORMATION(
            nameid INTEGER PRIMARY KEY AUTOINCREMENT,
            subtitlename TEXT,
            keywords TEXT);''')
            #修改数据库后必须调用commit方法提交才能生效
            self.conn.commit()
            print('字幕名称数据库创建成功.')
            #创建数据表
            self.cur.execute("DROP TABLE IF EXISTS DOWNLOADINFORMATION")
            self.cur.execute('''CREATE TABLE DOWNLOADINFORMATION(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            downloadurl TEXT,
            keywords TEXT);''')
            #修改数据库后必须调用commit方法提交才能生效
            self.conn.commit()
            #关闭数据库
            self.conn.close()
            print('字幕下载数据库创建成功.')

        self.conn=sqlite3.connect(self.MovieDBPath,timeout=50,check_same_thread=False)
        self.cur = self.conn.cursor()

    def addNameInformation(self, subtitlename, keywords):
        is_OK = False
        sql = "insert into NAMEINFORMATION(nameid, subtitlename,keywords) values ( NULL , '{}', '{}')".format(subtitlename,keywords)
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()
        is_OK = True
        return self.cur.lastrowid

    def addDownloadInformation(self, downloadurl, keywords):
        is_OK = False
        sql = "insert into DOWNLOADINFORMATION(id, downloadurl, keywords ) " \
              "values ( NULL , '{}' , '{}' )".format(downloadurl, keywords)
        self.cur.execute(sql)
        self.conn.commit()
        is_OK = True
        return is_OK

    def selectResourceByMovieid(self, moviename):
        sql = r"SELECT n.subtitlename, d.downloadurl FROM NAMEINFORMATION AS n INNER JOIN DOWNLOADINFORMATION AS d ON n.keywords = d.keywords WHERE n.subtitlename LIKE '{}' group by n.subtitlename;".format("%"+moviename+"%")
        info = self.cur.execute(sql)
        return info

    def selectMovie(self, moviename):
        sql = r"SELECT subtitlename, keywords FROM NAMEINFORMATION WHERE subtitlename LIKE '{}' group by subtitlename;".format(
            "%" + moviename + "%")
        info = self.cur.execute(sql)
        return info

    def continueSearch(self):
        pass

    def close_connect(self):
        self.conn.close()
