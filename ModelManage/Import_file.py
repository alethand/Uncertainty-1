#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector
from mysql.connector import Error
import config
import os
import Sql


def read_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data


# nid = 0为新建模型时第一次导入

def insert_blob(project, pid, descr, _dir, nid=0):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        if nid == 0:
            cursor.execute(Sql.insertProj, (project, pid, descr))
            cursor.execute(Sql.selectProj, (project, pid))
            record = cursor.fetchall()
            nid = record[0][0]
        for (root, dirs, files) in os.walk(_dir):
            for _file in files:
                absPath = os.path.join(root, _file)  # 绝对路径
                data = read_file(absPath)
                relDir = root.split(_dir, 1)[1]  # 相对路径
                args = (nid, relDir, _file, data)
                cursor.execute(Sql.importSql, args)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return nid


if __name__ == '__main__':
    insert_blob('test', 0, '', r"E:\MyEclipse 2015 CI\test\src\model")
