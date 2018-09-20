# -*- coding: utf-8 -*-
import numpy
def function(x, a):
    s = 0
    sa = 0
    for i in range(3):
        s = s + a[i]*x[i]**1
        sa = sa + a[i]*x[i]**2
    ts = 0
    for i in range(3):
        ts = ts + a[i+3]

    s = s + ts
    sa = sa + ts
    return s, sa


def description():
    param = [];
    param.append(['参数1', 'cog_p1', '无量纲']);
    param.append(['参数2', 'cog_p2', '无量纲']);
    param.append(['参数3', 'cog_p3', '无量纲']);
    param.append(['参数4', 'inh_p1', '无量纲']);
    param.append(['参数5', 'inh_p2', '无量纲']);
    param.append(['参数6', 'inh_p3', '无量纲']);
    return param;

def descr_var():
    var = [];
    var.append(['变量1', 'input_x1', '无量纲']);
    var.append(['变量2', 'input_x2', '无量纲']);
    var.append(['变量3', 'input_x3', '无量纲']);
    return var;

def run_simu_model(cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    n = shape_v[0]
    rans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[0])
    for i in range(n):
        if i == 0:
            continue
        tans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[i])
        rans = numpy.row_stack((rans, tans))
    return numpy.mat(rans)
