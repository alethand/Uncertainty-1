# -*- coding: utf-8 -*-
import ValidateUi as cp
import arg_order as ao
from compiler.ast import flatten
import numpy as np
import Sql

# 用来给其他模块返回真实的认知参数,这里写好的是arg_init值
cog_p_real = 0
# 用来形成真实数据
# 从这里看是一个认知不确定性参数对应所有固有参数，形成最终参数组合
# 最后输出对所有参数组合的平均值
def run_real_model(inh_p, input_X):
    global cog_p_real
    args = Sql.selectSql(args=(cp.n_id,), sql=Sql.selectArgs_2)
    arg = []
    for Xi in args:
        arg.append(Xi[0])

    # 认知不确定参数
    cog_p_real = arg
    cog_p_real = np.mat(cog_p_real)


    order = ao.get_order(cp.n_id)
    shape_inh = inh_p.shape
    ret = RunImportedModel(order, cog_p_real, inh_p[0], input_X)

    for i in range(shape_inh[0]):
        if i==0:
            continue
        tret = RunImportedModel(order, cog_p_real, inh_p[i], input_X)
        ret = ret + tret
    ret = ret/shape_inh[0]
    return ret

# 从这里看来是一个认知不确定行，一个固有不确定行对应所有输入变量
# 相当于一个参数组合对所有输入变量
# 输出对应X的模型输出，对应于一个参数组合
def RunImportedModel(order, cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    n = shape_v[0]
    cog_p_r_l = flatten(cog_p_r.tolist())
    inh_p_r_l = flatten(inh_p_r.tolist())
    inp_l = flatten(input_X[0].tolist())

    rans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
    for i in range(n):
        if i == 0:
            continue
        inp_l = flatten(input_X[i].tolist())
        tans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
        rans = np.row_stack((rans, tans))
    return np.mat(rans)