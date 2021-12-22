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


def sql_saved(images):

    sql_password = input('sql password : ')

    sql_database = create_sql_database(sql_password)

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
               )engine=InnoDB DEFAULT CHARSET=utf8;"

        cursor.execute(sql)

        connection.commit()

        print('Create artwork success')
    except:
        connection.rollback()
        print('Already have artwork')

    for image in images:  

        sql = "insert into artwork (day, name, title, image, video) VALUES (%s, %s, %s, %s, %s)"

        val = (image['day'], image['name'], image['title'], image['image'], image['video'])
        
        try:
            # 執行sql
            cursor.execute(sql, val)

            # 提交到數據庫
            connection.commit()

            print('{0} save success in vidoes list'.format(video['name']))
        except:
            # 發生錯誤跳回
            connection.rollback()

            print('{0} already save in vidoes list'.format(video['name']))

    connection.close()