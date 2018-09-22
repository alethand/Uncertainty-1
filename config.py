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
    'password': 'abc',
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

uncertaintyKind = OrderedDict([
    (0, '参数不确定性'),
    (1, '耦合不确定性'),
    (2, '状态转移不确定性'),
    (3, '海洋环境不确定性'),
    (4, '作战态势不确定性'),
    (5, '人为因素不确定性'),
    (6, '测试的不确定性'),
    (7, '评估的不确定性')
])

uncertaintyKind_set = {
    '参数不确定性': 0,
    '耦合不确定性': 1,
    '状态转移不确定性': 2,
    '海洋环境不确定性': 3,
    '作战态势不确定性': 4,
    '人为因素不确定性': 5,
    '测试的不确定性': 6,
    '评估的不确定性': 7
}

measurement = OrderedDict([
    (0, '数值概率'),
    (1, '分布概率'),
    (2, '区间度量'),
    (3, '证据理论'),
    (4, '可能性理论'),
    (5, '模糊集'),
    (6, '凸模型方法')
])

measurement_set = {
    '数值概率': 0,
    '分布概率': 1,
    '区间度量': 2,
    '证据理论': 3,
    '可能性理论': 4,
    '模糊集': 5,
    '凸模型方法': 6
}

pattern = OrderedDict([
    (0, '持续的'),
    (1, '周期的'),
    (2, '不定时发生的'),
    (3, '短暂的/瞬间的')
])

pattern_set = {
    '持续的': 0,
    '周期的': 1,
    '不定时发生的': 2,
    '短暂的/瞬间的': 3
}

arg_type_set = {
    '自变量': 0,
    '固有不确定性参数': 1,
    '认知不确定性参数': 2
}
