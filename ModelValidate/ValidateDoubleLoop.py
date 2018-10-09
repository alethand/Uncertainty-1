# -*- coding: utf-8 -*-
import ValidateUi as cp
import arg_order as ao
from compiler.ast import flatten
import numpy as np

# 从这里看来是一个认知不确定行，一个固有不确定行对应所有输入变量
# 相当于一个参数组合对所有输入变量
# 输出与输入变量维度相对应的输出
def RunImportedModel(order, cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    # 自变量的条数
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
#一组认知不确定参数，固有不确定参数被积分，对应自变量
#代表该次认知不确定下，所对应的模型输出
def inner_level_loop(cog_p_r, inh_p, input_X, order=0):
    output_m = RunImportedModel(order, cog_p_r, inh_p[0], input_X)
    shape_va = inh_p.shape
    M_v = shape_va[0]
    for i in range(M_v):
        if i == 0:
            continue
        inh_p_r = inh_p[i]  # 每一组固有不确定参数
        output_ma = RunImportedModel(order, cog_p_r, inh_p_r, input_X)
        output_m = output_m + output_ma

    output_m = output_m/M_v
    return output_m  # 是一个在该认知不确定参数下得到的输出特征矩阵M*p p为输出个数

# 外层循环对每个认知不确定参数循环，循环后，一个认知不确定参数对应一个输出，

def outer_level_loop(cog_p, inh_p, input_X):
    """
    用来产生模型数据
    :param cog_p:
    :param inh_p:
    :param input_X:
    :return: 一个3维矩阵
    """
    print('认知不确定参数:')
    print cog_p.shape
    print('固有不确定参数:')
    print inh_p.shape
    print('输入为:')
    print input_X.shape

    order = ao.get_order(cp.n_id)

    shape_v = cog_p.shape
    N_v = shape_v[0]  # 认知不确定性参数的组数
    model_data = []
    for i in range(N_v):  # 每一组认知不确定参数
        cog_pi_output = inner_level_loop(cog_p[i], inh_p, input_X, order)
        model_data.append(cog_pi_output)
    return np.array(model_data)