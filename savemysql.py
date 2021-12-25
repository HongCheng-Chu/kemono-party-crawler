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


def sql_saved(dicts):

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
        sql = "create table if not exists artwork(\
               day varchar(50),\
               name varchar(50),\
               title varchar(250),\
               image varchar(300),\
               video varchar(300),\
               primary key (title)\
               )engine=InnoDB DEFAULT CHARSET=utf8;"

        cursor.execute(sql)

        connection.commit()

        print('Create artwork success')

    except:
        connection.rollback()
        print('Already have artwork')

    for dict in dicts:

        iter = 0

        for i in dict["img"]:

            sql = "insert into artwork (day, name, title, image) VALUES (%s, %s, %s, %s)"

            val = (dict['day'], dict['name'], dict['title']+"-{0}".format(iter), i)

            iter = iter + 1
        
            try:
                # 執行sql
                cursor.execute(sql, val)

                # 提交到數據庫
                connection.commit()

                print('{0} save success in vidoes list'.format(dict['name']))
            except:
                # 發生錯誤跳回
                connection.rollback()

                print('{0} already save in vidoes list'.format(dict['name']))
        
        for i in dict["video"]:

            sql = "insert into artwork (day, name, title, video) VALUES (%s, %s, %s, %s)"

            val = (dict['day'], dict['name'], dict['title']+"-{0}".format(iter), i)

            iter = iter + 1
        
            try:
                # 執行sql
                cursor.execute(sql, val)

                # 提交到數據庫
                connection.commit()

                print('{0} save success in vidoes list'.format(dict['name']))
            except:
                # 發生錯誤跳回
                connection.rollback()

                print('{0} already save in vidoes list'.format(dict['name']))

        iter = 0


    connection.close()


def check_day():

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

    recent_day = ''

    try:
        sql = "select day from artwork order by day desc"

        cursor.execute(sql)

        recent_day = cursor.fetchone()

        print('get recent update day success')

    except:
        connection.rollback()

        print('Can not find artwork table')

    return recent_day
