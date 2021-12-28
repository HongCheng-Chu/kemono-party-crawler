import json
import os
import pymysql
from pymysql import cursors
from datetime import datetime


def create_database(sql_password):

    try:
        connection = pymysql.connect(host='localhost',
                           user='root',
                           password= sql_password,
                           cursorclass=pymysql.cursors.DictCursor,
                           charset='utf8')
        if connection:
            print('Connect success')
    except:
        print('Connect fail')

    cursor = connection.cursor()

    sql = "create database if not exists kemono"

    cursor.execute(sql)

    print('Create avgirls database success')

    connection.close()

    return 'kemono'


def sql_saved(dicts, name):

    sql_password = input('sql password : ')

    sql_database = create_database(sql_password)

    try:
        # 建立Connection物件
        connection = pymysql.connect(host='localhost',
                               user='root',
                               password= sql_password,
                               database= sql_database,
                               cursorclass=pymysql.cursors.DictCursor, # 以字典的形式返回操作結果
                               charset='utf8')
        if connection:
            print('Connect success')
    except:
        print('Connect fail')

    cursor = connection.cursor()

    try:
        sql = "create table if not exists {0}(\
               day varchar(50),\
               name varchar(50),\
               title varchar(250),\
               image varchar(300),\
               video varchar(300),\
               primary key (title)\
               )engine=InnoDB DEFAULT CHARSET=utf8;".format(name)

        cursor.execute(sql)

        connection.commit()

        print('Create artwork success')

    except:
        connection.rollback()
        print('Already have artwork')

    for dict in dicts:

        iter = 0

        for i in dict["img"]:

            sql = "insert into {0} (day, name, title, image) VALUES (%s, %s, %s, %s)".format(dict['name'])

            val = (dict['day'], dict['name'], dict['title']+"-{0}".format(iter), i)

            iter = iter + 1
        
            try:
                # 執行sql
                cursor.execute(sql, val)

                # 提交到數據庫
                connection.commit()

                print('{0} image put in {1} book success'.format(dict['title'], dict['name']))
            except:
                # 發生錯誤跳回
                connection.rollback()

                print('{0} image already save in {1} book'.format(dict['title'], dict['name']))
        
        for i in dict["video"]:

            sql = "insert into {0} (day, name, title, video) VALUES (%s, %s, %s, %s)".format(dict['name'])

            val = (dict['day'], dict['name'], dict['title']+"-{0}".format(iter), i)

            iter = iter + 1
        
            try:
                # 執行sql
                cursor.execute(sql, val)

                # 提交到數據庫
                connection.commit()

                print('{0} video put in {1} book success'.format(dict['title'], dict['name']))
            except:
                # 發生錯誤跳回
                connection.rollback()

                print('{0} video already save in {1} book'.format(dict['title'], dict['name']))

        iter = 0


    connection.close()


def check_day(name):

    sql_password = input('sql password : ')

    sql_database = create_database(sql_password)

    try:
        # 建立Connection物件
        connection = pymysql.connect(host='localhost',
                               user='root',
                               password= sql_password,
                               database= sql_database,
                               cursorclass=pymysql.cursors.DictCursor, # 以字典的形式返回操作結果
                               charset='utf8')
        if connection:
            print('Connect success')
    except:
        print('Connect fail')

    cursor = connection.cursor()

    try:
        sql = "select day from artwork where name = '{0}' order by day desc".format(name)

        cursor.execute(sql)

        recent_day = cursor.fetchone()['day']

        print('get recent update day success')

    except:
        connection.rollback()

        recent_day = '0000-00-00'

        print('Can not find {0} table'.format(name))

    return recent_day
