#-*- codeing = utf-8 -*-
#@Time :  
#@Author: Mianbao
#@File : DBManger.py
#@Software : PyCharm
import sqlite3
import os
'''
数据库设计：
    first:  movieinformation 影片展示的信息         4个字段
        movieid             主键
        moviename           持械抢劫 (2012)
        movieresource       http://www.xxi5.cn//m_185.html
        moviepicture        https://pianyuan-1251752595.file.myqcloud.com/d/file/titlepic/2015/11/15/01/0gdezwy0ecg172.jpg
    second: resourceinformation 下载信息              9个字段
        id                  主键
        movieid             外键
        resourcename        梦幻天堂·龙网(lwgod.com).720p.疾速追杀.杀神.捍卫任务
        resourcequality     BluRay-720P
        resourcefoundpage   http://www.xxi5.cn/r_5752.html
        resourcesize        2.72GB
        resourcedate        5年前
        downloadnum         19
        resourcedownload    magnet:?xt=urn:btih:0bec7f2aad1f88d99a65f511adc656709b3c66a2&dn=%E6%A2%A6%E5%B9%BB%E5%A4%A9%E5%A0%82%C2%B7%E9%BE%99%E7%BD%91%28lwgod.com%29.720p.%E7%96%BE%E9%80%9F%E8%BF%BD%E6%9D%80.%E6%9D%80%E7%A5%9E.%E6%8D%8D%E5%8D%AB%E4%BB%BB%E5%8A%A1&tr=http%3A%2F%2Ft
    first和second两者连表查询，通过first的主键去second查找其外键以获取资源个数和资源下载的各项信息
    second中应该在每个first生成时如果其未有下载资源的话应当给予补齐，除id外其余属性全为空即可
'''
class sqlite_db():
    def __init__(self):
        self.MovieDBPath = 'moviedata.sqlite'
        # 只有sqlite文件不存在时才创建该文件。
        if not os.path.exists(self.MovieDBPath):
            # 创建SQLite数据库
            self.conn = sqlite3.connect(self.MovieDBPath,check_same_thread=False)
            #获取sqlite3.Cursor对象
            self.cur = self.conn.cursor()
            #创建数据表
            self.cur.execute("DROP TABLE IF EXISTS MOVIEINFORMATION")
            self.cur.execute('''CREATE TABLE MOVIEINFORMATION(
            movieid INTEGER PRIMARY KEY AUTOINCREMENT,
            moviename TEXT,
            movieresource TEXT,
            moviepicture TEXT);''')
            #修改数据库后必须调用commit方法提交才能生效
            self.conn.commit()
            print('电影信息数据库创建成功.')
            #创建数据表
            self.cur.execute("DROP TABLE IF EXISTS RESOURCEINFORMATION")
            self.cur.execute('''CREATE TABLE RESOURCEINFORMATION(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resourcename TEXT,
            resourcequality TEXT,
            resourcefoundpage TEXT,
            resourcesize TEXT,
            resourcedate TEXT,
            downloadnum TEXT,
            resourcedownload TEXT,
            movieid INTEGER);''')
            #修改数据库后必须调用commit方法提交才能生效
            self.conn.commit()
            #关闭数据库
            self.conn.close()
            print('下载信息数据库创建成功.')

        self.conn=sqlite3.connect(self.MovieDBPath,timeout=50,check_same_thread=False)
        self.cur = self.conn.cursor()

    def addMovieInformation(self, moviename, movieresource, moviepicture):
        is_OK = False
        sql = "insert into MOVIEINFORMATION(movieid, moviename, movieresource, moviepicture) values ( NULL , '{}' , '{}' , '{}' )".format(moviename, movieresource, moviepicture)
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()
        # self.close_connect()
        is_OK = True
        return self.cur.lastrowid

    def addResourceInformation(self, resourcename, resourcequality, resourcefoundpage, resourcesize, resourcedate, downloadnum, resourcedownload, movieid):
        is_OK = False
        sql = "insert into RESOURCEINFORMATION(id, resourcename, resourcequality, resourcefoundpage, resourcesize, resourcedate, downloadnum, resourcedownload, movieid) " \
              "values ( NULL , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' )".format(resourcename, resourcequality, resourcefoundpage, resourcesize, resourcedate, downloadnum, resourcedownload, movieid)
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()
        # self.close_connect()
        is_OK = True
        return is_OK

    def selectResourceByMovieid(self, moviename):
        sql = r"SELECT m.movieid, m.moviename, r.resourcename, r.resourcequality, r.resourcesize, r.resourcedownload, m.movieresource, m.moviepicture " \
              r"FROM MOVIEINFORMATION AS m INNER JOIN RESOURCEINFORMATION AS r ON m.movieid = r.movieid WHERE m.moviename LIKE '{}';".format("%"+moviename+"%")
        info = self.cur.execute(sql)
        return info

    def continueSearch(self):
        pass
