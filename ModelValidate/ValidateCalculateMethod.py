# -*- coding: utf-8 -*
from __future__ import division
import numpy
def cal_avg_vi(Esi):
    ans = numpy.mean(Esi, axis=0)
    return ans.T

def cal_cov_mat(Esi):
    avg_vi = cal_avg_vi(Esi)
    shape_v = Esi.shape
    m = shape_v[0]
    em = numpy.mat(numpy.full((m, 1), 1))

    print (Esi - em * avg_vi.T).T
    print Esi - em * avg_vi.T
    print (Esi - em * avg_vi.T).T * (Esi - em * avg_vi.T)

    ret_mat = 1 / (m - 1) * (Esi - em * avg_vi.T).T * (Esi - em * avg_vi.T)

    # print "自己计算"
    # print ret_mat
    # print "机器计算"
    # print numpy.cov(Esi.T)

    return ret_mat

def Mahalanobis_1(output_k, avg_vi, cov_mat):
    ret = (output_k - avg_vi).T * cov_mat.I * (output_k - avg_vi)
    return ret

def Mahalanobis_2(cog_output, output):
    avg_vi = cal_avg_vi(output)
    print ('均值向量为:')
    print (avg_vi)
    cov_mat = cal_cov_mat(output)
    print ('协方差矩阵为:')
    print (cov_mat)
    print ('协方差矩阵的逆为:')
    print (cov_mat.I)
    shape_v = cog_output.shape
    di = 0
    for i in range(shape_v[0]):
        cog_output_k = cog_output[i].T
        di_k = Mahalanobis_1(cog_output_k, avg_vi, cov_mat)
        # print ('di_k为:')
        # print (di_k)
        di = di + di_k
    return numpy.sqrt(di)

def Euclid_distance(cog_output, output):
    dif_arr = numpy.array(cog_output-output)
    dif_arr = dif_arr**2
    return numpy.sqrt(dif_arr.sum())
