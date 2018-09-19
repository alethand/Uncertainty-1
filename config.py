#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import OrderedDict

# datasourse = {
#     'host': '118.89.198.205',
#     'user': 'certainty',
#     'password': 'Nuaa666',
#     'port': 3306,
#     'database': 'work',
#     'charset': 'utf8'
# }

datasourse = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'work',
    'charset': 'utf8'
}

# datasourse = {
#     'host': '192.168.43.241',
#     'user': 'root',
#     'password': '123456',
#     'port': 3306,
#     'database': 'work',
#     'charset': 'utf8'
# }

main_file = 'test1'

main_func = 'function'

param_func = 'description' 

var_func = 'descr_var'

dis_type_get = OrderedDict([
            ('normal', '正态分布'),
            ('uniform', '均匀分布'),
            ('exponential', '指数分布'),
            ('other', '任意分布')])

dis_type_set = {
    '正态分布': 'normal',
    '均匀分布': 'uniform',
    '指数分布': 'exponential',
    '任意分布': 'other'
}

dis_index_set = {
    u'正态分布': 0,
    u'均匀分布': 1,
    u'指数分布': 2,
    u'任意分布': 3
}

arg_type_get = OrderedDict([
            (0, '自变量'),
            (1, '固有不确定性参数'),
            (2, '认知不确定性参数')])

arg_type_set = {
    '自变量': 0,
    '固有不确定性参数': 1,
    '认知不确定性参数': 2
}
