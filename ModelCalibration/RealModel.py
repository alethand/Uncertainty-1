import numpy
import CalculateMethod as ca
import CalibrationPanel as cp
import arg_order as ao
from compiler.ast import flatten
import numpy as np
import ShowNotebook as SNB
def run_real_model_inner(inh_p_r, input_Xi):
    shape_v = input_Xi.shape
    l = [4, 1, 8]
    s = 0
    sa = 0
    for i in range(shape_v[1]):
        s = s+l[i]*input_Xi[0, i]
        sa = sa+l[i]*input_Xi[0, i]**2

    shape_va = inh_p_r.shape
    ts = 0
    for i in range(shape_va[1]):
        ts = ts+inh_p_r[0, i]

    s = s+ts
    sa = sa+ts
    return s, sa

def run_real_model(inh_p, input_X):
    shape_v = input_X.shape
    ret = run_real_model_inner(inh_p[0], input_X[0])
    for i in range(shape_v[0]):
        if i == 0:
            continue
        tret = run_real_model_inner(inh_p[0], input_X[i])
        ret = numpy.row_stack((ret, tret))

    shape_v1 = inh_p.shape
    ret = numpy.mat(ret)

    for i in range(shape_v1[0]):
        if i == 0:
            continue
        shape_v = input_X.shape
        ret_a = run_real_model_inner(inh_p[i], input_X[0])
        for ia in range(shape_v[0]):
            if ia == 0:
                continue
            tret = run_real_model_inner(inh_p[i], input_X[ia])
            ret_a = numpy.row_stack((ret_a, tret))
        ret_a = numpy.mat(ret_a)
        ret = ret+ret_a

    ret = ret/shape_v1[0]
    return ret

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
