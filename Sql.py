#!/usr/bin/python
# -*- coding: UTF-8 -*-
import config
import mysql.connector
import MySQLdb
import cPickle

loginSql = "SELECT c_account, c_password FROM t_user WHERE c_account = %s"

modelSql = "SELECT n_id, c_project, n_pid FROM t_project"

selectProj = "SELECT n_id, c_project, n_pid FROM t_project where c_project = %s"\
             "and n_pid = %s"

insertProj = "insert into t_project(c_project, n_pid, c_descr) values(%s, %s, %s)"

updateProj = "update t_project set c_project = %s, c_descr = %s where n_id = %s"

importSql = "insert into t_file(n_project, c_dir, c_filename, b_pyfile) " \
            "values(%s, %s, %s, %s)"
            
exportSql = "SELECT c_dir, c_filename, b_pyfile FROM t_file WHERE n_project = %s"

insertParam = "insert into model_arg(arg_name, model_id, arg_descr, arg_unit, " \
            "arg_init) values(%s, %s, %s, %s, %s)"

insertVar = "insert into model_arg(arg_name, model_id, arg_descr, arg_unit, " \
            "arg_init, arg_type) values(%s, %s, %s, %s, %s, '0')"

selectModel = "SELECT c_project,c_descr,n_pid FROM t_project WHERE n_id = %s"


selectModelArgs = "SELECT arg_name,arg_descr,arg_init,arg_id FROM model_arg WHERE model_id = %s"\
                  " and (arg_type != 0 or arg_type is NULL) order by arg_id asc"

selectModelVars = "SELECT arg_name,arg_descr,arg_init,arg_id,arg_type FROM model_arg WHERE model_id = %s"\
                  " and arg_type = 0 order by arg_id asc"

selectModelOutputArgs = "SELECT op_name,op_descr,op_id FROM t_output_param WHERE model_id = %s order by op_id asc"
            
selectParams = "SELECT arg_name, arg_id, arg_init, arg_descr, arg_unit, arg_type," \
            "dis_type, dis_arg FROM model_arg WHERE model_id = %s order by arg_id asc"

updateParams = "update model_arg set arg_type = %s, dis_type = %s, dis_arg = %s where arg_id = %s"

deleteModel = "DELETE FROM t_project WHERE n_id = %s"

deleteFile = "DELETE FROM t_file WHERE n_project = %s"

deleteModelArgs = "DELETE FROM model_arg WHERE model_id = %s"

deleteModelOutputArgs = "DELETE FROM t_output_param WHERE model_id = %s"

#获取认知不确定性参数
selectArgs_2 = "SELECT arg_init FROM model_arg WHERE model_id = %s and arg_type = 2"

# selectModel = "SELECT c_project,c_descr,n_pid FROM t_project WHERE n_id = %s"

# selectModelArgs = "SELECT arg_name,arg_id,arg_init FROM model_arg WHERE model_id = %s"

# deleteModel = "DELETE FROM t_project WHERE n_id = %s"

# deleteModelArgs = "DELETE FROM model_arg WHERE model_id = %s"

deleteSamplingResult = "DELETE FROM t_sampling_result WHERE r_id in "\
                       "(SELECT arg_id FROM model_arg WHERE model_id = %s)"

model_d_Sql = "SELECT arg_name FROM model_arg ORDER BY arg_id"

get_model_Sql = "SELECT m.model_name, a.arg_name, a.dis_type, a.dis_arg FROM model_arg a, model m  WHERE m.model_id = a.model_id AND m.model_name = "

# 连接模型和参数表 查询选中的模型的名称 和其对应的参数名 分布类型 分布参数 参数ID 和 参数类型
get_arg_Sql = "SELECT m.c_project, a.arg_name, a.dis_type, a.dis_arg, a.arg_id ,a.arg_type,a.model_id FROM model_arg a, t_project m "\
              "WHERE m.n_id = a.model_id AND m.n_id = "

#第一种取抽样结果方法
get_sampling_count = "select count(1) from sampling_result sa "\
                     "left join model_arg arg on sa.arg_id = arg.arg_id "\
                     "where arg.model_id = %s and arg.arg_type = %s "\
                     "group by arg.arg_id limit 1"
 
get_samp1 = "select arg.arg_name, result_value from sampling_result sa "\
            "left join model_arg arg on sa.arg_id = arg.arg_id "\
            "where arg.model_id = %s and arg.arg_type = %s "\
            "order by arg.arg_id, result_id"

#第二种取抽样结果方法
get_samp2 = "select arg.arg_name, GROUP_CONCAT(result_value order by result_id) "\
            "from sampling_result sa "\
            "left join model_arg arg on sa.arg_id = arg.arg_id "\
            "where arg.model_id = %s and arg.arg_type = %s "\
            "group by arg.arg_id order by arg.arg_id asc"

get_order = "select rownum from(" \
            "SELECT arg_id, (@rownum:=@rownum+1) AS rownum " \
            "FROM model_arg, (SELECT @rownum:=-1) r " \
            "WHERE model_id = %s and arg_type != 0 " \
            "ORDER BY arg_type, arg_id) temp order by arg_id" \

def selectSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        record = cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return record

def updateSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True


def clear_sampling_result():
    query = "delete from  t_sampling_result"

    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def clear_sampling_result_of_model(model_id):
    query = "delete from  sampling_result where arg_id in (select arg_id from model_arg where model_id = " + str(model_id) + " );"
    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# 传入参数名和所有抽样结果 循环写入
def insert_sampling_result(arg_names,results):
    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        j = 0
        for result in results:
            for i in result:
                query = "insert into t_sampling_result(r_value,arg_name) values(%s,%s)"
                args = (float(i), arg_names[j])
                cursor.execute(query, args)
            j += 1
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# 传入参数名和所有抽样结果 循环写入 sampling_result 表 其中arg_id 需要查询model_arg 表
def insert_sampling_results(arg_id,results,method_name):
    db_config = config.datasourse

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        j = 0
        for result in results:
            for i in result:

                # '''查询arg_name对应的arg_id'''
                # query = "select arg_id from model_arg  where arg_name = '" + arg_names[j] + "';"
                # cursor = conn.cursor()
                # cursor.execute(query)
                # # 获取所有记录列表
                # results = cursor.fetchall()
                #
                # '''ends of 查询arg_name对应的arg_id'''

                query = "insert into sampling_result(result_value,arg_id,sampling_method) values(%s,%s,%s)"
                args = (float(i), arg_id[j],method_name[j])
                cursor.execute(query, args)
            j += 1
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def deleteSql(args=(), sql=''):
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def show_sampling_result(name):
    query = "select r_value from t_sampling_result  where arg_name = '" + name + "' order by r_id;"
    try:
        db_config = config.datasourse
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as e:
        print(e)
    cursor.close()
    conn.close()

# 参数是参数类型 返回结果是对应类型的抽样结果
def show_sampling_result_with_type(type, model_id, arg_id):
    # query = "select r_value from t_sampling_result  where arg_name = '" + name + "' order by r_id;"
    # query = "select r_value from sampling_result where arg_id in (select arg_id from model_arg where arg_type =  "+ type +" ) order by result_id;"
    query = "select sr.result_value, m.arg_name from sampling_result sr, model_arg m " \
            "where sr.arg_id = m.arg_id AND m.arg_type =  " + str(type) + " AND m.model_id = " + str(model_id) + " AND sr.arg_id = " + str(arg_id) + " "\
            "order by sr.result_id;"
    try:
        db_config = config.datasourse
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as e:
        print(e)
    cursor.close()
    conn.close()


def insert_new_model(model_id,inputargs=[],vars = [],outputargs=[] ):
    """保存新建模型数据信息"""
    sql = "insert into model_arg (arg_name,arg_descr,arg_init,model_id) values(%s,%s,%s,%s)"
    sql1 = "insert into model_arg (arg_name,arg_descr,arg_init,arg_type,model_id) values(%s,%s,%s,%s,%s)"
    sql2 = "insert into t_output_param (op_name,op_descr,model_id) values(%s,%s,%s)"
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        """写输入参数信息到数据库"""
        for i in inputargs:
#             print i
            i.append(model_id)
            cursor.execute(sql, i)
        """写自变量信息到数据库"""
        for i in vars:
#             print i
            i.append(model_id)
            cursor.execute(sql1, i)
        """写输出参数信息到数据库"""
        for i in outputargs:
            i.append(model_id)
#             print i
            cursor.execute(sql2, i)

        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return True


def update_model(model_id,inputargs=[],vars = [],outputargs=[] ):
    """更新模型数据信息"""
    sql = "update model_arg set arg_name=%s,arg_descr=%s,arg_init=%s where arg_id=%s and model_id=%s"
    sql1 = "update model_arg set arg_name=%s,arg_descr=%s,arg_init=%s where arg_id=%s and arg_type=%s and model_id=%s"
    sql2 = "update t_output_param set op_name=%s,op_descr=%s where op_id=%s and model_id=%s"
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        """写输入参数信息到数据库"""
        for i in inputargs:
#             print i
            i.append(model_id)
            cursor.execute(sql, i)

        """写自变量信息到数据库"""
        for i in vars:
#             print i
            i.append(model_id)
            cursor.execute(sql1, i)

        """写输出参数信息到数据库"""
        for i in outputargs:
            i.append(model_id)
#             print i
            cursor.execute(sql2, i)

        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return True

"""保存元模型"""
def insert_metamodel(model_id,type,metamodel ):
    """保存新建模型数据信息"""
    sql = "insert into t_metamodel (model_id,metamodel_type,metamodel) values(%s,%s,%s)"
    sql2 = "update t_metamodel set metamodel = %s where model_id=%s and metamodel_type=%s"
    sql3 = "delete from t_metamodel where model_id=%s and metamodel_type=%s"

    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        """保存元模型到数据库"""
        print "111111111111111111111111111",MySQLdb.escape_string(cPickle.dumps(metamodel))
        cursor.execute(sql2, (cPickle.dumps(metamodel),model_id, type))
        if cursor.rowcount == 0:
            cursor.execute(sql,(model_id,type,MySQLdb.escape_string(cPickle.dumps(metamodel))))
        #cursor.execute(sql3, ( model_id, type))
        print cursor.rowcount

        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return True

def selectMetaModel(model_id,type):
    sql = "select metamodel from t_metamodel where model_id=%s and metamodel_type=%s"
    db_config = config.datasourse
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql,(model_id,type))
        record = cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    print record[0]
    return cPickle.loads(str(record[0]))