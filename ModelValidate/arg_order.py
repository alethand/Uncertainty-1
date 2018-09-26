# -*- coding: utf-8 -*-

import Sql
from ModelManage import Run
# 假设原来参数顺序0，1，2，3 输出按照arg_type，arg_id递增的序
def get_order(nid):
    records = Sql.selectSql((nid,), Sql.get_order)
    order = []
    for record in records:
        order.append(int(record[0]))
    # print 'order: %s' % order
    return order
# 给定不确定参数的序，转化为原来模型参数的序
# inp应该是变量，inh，cog是不确定参数
def get_result(nid, order, inp, inh, cog):
    # 把认知不确定参数列表和固有不确定性参数列表合并
    arg = inh + cog
    arg_order = [] 
    for i in range(len(arg)):
        arg_order.append(arg[order[i]])
    return Run.tryrun(nid, inp, arg_order)

if __name__ == '__main__':
    order = get_order(76)