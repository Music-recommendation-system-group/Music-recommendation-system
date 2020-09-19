#-*- codeing = utf-8 -*-
#@Time : 2020/9/16 0016 19:29
#@Author :DongSW
#@File : db_fun.py
#@Software : PyCharm

import pymysql

# username : root
# password : 68691102


class DataBaseHandle(object):
    ''' 定义一个 MySQL 操作类'''


    def __init__(self,host,username,password,database,port):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8')



    #  这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    #
    def connDataBase(self):
        self.db = pymysql.connect(self.host,self.username,self.password,self.port,self.database)
        self.cursor = self.db.cursor()
        return self.db


    def insertDB(self,sql):
        ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()



    def deleteDB(self,sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()





    def updateDb(self,sql):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()





    def selectDb(self,sql):
        ''' 数据库查询 '''
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchall() # 返回所有记录列表

            print(data)

            # 结果遍历
            for row in data:
                row1= row[0]
                row4 = row[4]
                # 遍历打印结果
                result=[row1,row4]
                print('row1 = %s,  row4 = %s'%(row1,row4))
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()
        return data

    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()



if __name__ == '__main__':

    DbHandle = DataBaseHandle('127.0.0.1','root','68691102','recommend',3306)#初始化


    new111= DbHandle.selectDb('select * from allsong')#分别输出歌曲名，时间，作者，专辑，歌单

    new222 = DbHandle.selectDb('select distinct songlist from allsong')#输出所有歌单

    DbHandle.closeDb()