#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import mysql.connector
from mysql.connector import Error
import config
import Sql

    #写文件
def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

    #拼接绝对路径
def get_dir(project, c_dir):
    _dir = os.path.join(os.getcwd(), 'model_'+ str(project))
    _dir = _dir + c_dir.encode("utf-8")
    _dir = unicode(_dir, "utf-8")
    return _dir
        
    #从数据库读出模型文件
def read_blob(project):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(Sql.exportSql, (project,))
        for c_dir, c_filename, b_pyfile in cursor.fetchall():
            _dir = get_dir(project, c_dir)
            if not(os.path.exists(_dir)):
                os.makedirs(_dir)
            path = _dir + "\\" + c_filename.encode("utf-8")
            write_file(b_pyfile, path)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        
def run():
    sys.path.append(r"E:\MyEclipse 2015 CI\test\src\test")
    print sys.path
#     kNN=imp.load_source('kNN', 'E:\MyEclipse 2015 CI\test\src\一元非线性回归\test.py')
    filename = "test1"
    method = "function"
    variable = [1,2,3]

    obj = __import__(filename) # import module
    c = getattr(obj,method)
    print c(x = variable) # call def

def tryrun(proj, vars=[], inputargs=[]):
    sys_path = get_dir(proj, '')
    print sys_path
    if sys_path in sys.path:
        sys.path.remove(sys_path)   #使当前模型路径为系统环境变量
    sys.path.insert(0, sys_path)
#     print sys.path
#     kNN=imp.load_source('kNN', 'E:\MyEclipse 2015 CI\test\src\一元非线性回归\test.py')
#     filename = "test1"
#     method = "function"
#     variable = [1,2,3]
#     ax = [1,2,3,4]
    try:
        __import__(config.main_file)
    except ImportError:
        print 33333
    if sys.modules.has_key(config.main_file):
        del sys.modules[config.main_file]
    obj = __import__(config.main_file) # import module
    c = getattr(obj, config.main_func)
#     print c(x = vars,a = inputargs) # call def
    return c(x = vars,a = inputargs)
    
def  read_param(proj, func):
    sys_path = get_dir(proj, '')
    if sys_path in sys.path:
        sys.path.remove(sys_path)   #使当前模型路径为系统环境变量
    sys.path.insert(0, sys_path)
    #删除之前导入的模块 避免同名模块
    if sys.modules.has_key(config.main_file):
        del sys.modules[config.main_file]
    ip_module = __import__(config.main_file)
    descr = getattr(ip_module, func)
    return descr()
    
def init_param():
    db_config = config.datasourse
    query = "insert into t_param_model(c_project, c_description, c_modeltype) " \
            "values(%s, %s, %s)"
    sys.path.append(r"E:\MyEclipse 2015 CI\test\src\test")
    print sys.path
    filename = "test1"
    method = "description"
    variable = [1,2,3]

    obj = __import__(filename) # import module
    c = getattr(obj, method)
    c = getattr(c, method)
    params = c()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for param in params:
            cursor.execute(query, ("test", param, "1"))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    

 
if __name__ == '__main__':
    read_blob("3")
#     init_param()
#     run()
