import numpy
import ModelManage.Run as Run
from compiler.ast import flatten

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

def run_real_model(inh_p, cog_p, input_X):
    shape_v = input_X.shape
    print "----------------------------"
    print flatten(inh_p[0].tolist())
    print flatten(cog_p[0].tolist())
    print numpy.r_[flatten(inh_p[0].tolist()), flatten(cog_p[0].tolist())]
    print flatten(input_X[0].tolist())
    print Run.tryrun(76,flatten(input_X[0].tolist()),numpy.r_[flatten(cog_p[0].tolist()), flatten(inh_p[0].tolist())])
        #float(str(round(inh_p[0],8)))
    print "----------------------------"

    ret = Run.tryrun(76,flatten(input_X[0].tolist()),numpy.r_[flatten(inh_p[0].tolist()), flatten(cog_p[0].tolist())])
    for i in range(shape_v[0]):
        if i == 0:
            continue
        tret = Run.tryrun(76,flatten(input_X[i].tolist()),numpy.r_[flatten(inh_p[0].tolist()), flatten(cog_p[0].tolist())])
        ret = numpy.row_stack((ret, tret))

    shape_v1 = inh_p.shape
    ret = numpy.mat(ret)

    for i in range(shape_v1[0]):
        if i == 0:
            continue
        shape_v = input_X.shape
        ret_a = Run.tryrun(76,flatten(input_X[0].tolist()),numpy.r_[flatten(inh_p[i].tolist()), flatten(cog_p[0].tolist())])
        for ia in range(shape_v[0]):
            if ia == 0:
                continue
            tret = Run.tryrun(76,flatten(input_X[ia].tolist()),numpy.r_[flatten(inh_p[i].tolist()), flatten(cog_p[0].tolist())])
            ret_a = numpy.row_stack((ret_a, tret))
        ret_a = numpy.mat(ret_a)
        ret = ret + ret_a

    # ret = run_real_model_inner(inh_p[0], input_X[0])
    # for i in range(shape_v[0]):
    #     if i == 0:
    #         continue
    #     tret = run_real_model_inner(inh_p[0], input_X[i])
    #     ret = numpy.row_stack((ret, tret))
    #
    # shape_v1 = inh_p.shape
    # ret = numpy.mat(ret)
    #
    # for i in range(shape_v1[0]):
    #     if i == 0:
    #         continue
    #     shape_v = input_X.shape
    #     ret_a = run_real_model_inner(inh_p[i], input_X[0])
    #     for ia in range(shape_v[0]):
    #         if ia == 0:
    #             continue
    #         tret = run_real_model_inner(inh_p[i], input_X[ia])
    #         ret_a = numpy.row_stack((ret_a, tret))
    #     ret_a = numpy.mat(ret_a)
    #     ret = ret+ret_a

    ret = ret/shape_v1[0]
    return ret
