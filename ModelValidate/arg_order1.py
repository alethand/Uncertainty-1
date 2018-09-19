# -*- coding: utf-8 -*-

import Sql
from ModelManage import Run
import numpy as np

def get_order(nid):
    records = Sql.selectSql((nid,), Sql.get_order)
    order = []
    for record in records:
        order.append(int(record[0]))
    return order

def get_result(nid, order, inp, inh, cog):
#     inh = inh.tolist()
#     cog = cog.tolist()
    arg = inh + cog
    arg_order = [] 
    for i in range(len(arg)):
        arg_order.append(arg[order[i]])
    return Run.tryrun(nid, inp, arg_order)

if __name__ == '__main__':
    order = get_order(9)
    get_result(9, order, (1, 2, 3), (4, 5, 6), (7, 8, 9))