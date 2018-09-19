# -*- coding: utf-8 -*
from __future__ import division
import numpy
def cal_avg_vi(Esi):  #计算均值向量
    ans = numpy.mean(Esi, axis=0)
    return ans.T

def cal_cov_mat(Esi):  #计算协方差矩阵
    avg_vi = cal_avg_vi(Esi)
    shape_v = Esi.shape
    m = shape_v[0]
    em = numpy.mat(numpy.full((m, 1), 1))
    ret_mat = 1 / (m - 1) * (Esi - em * avg_vi.T).T * (Esi - em * avg_vi.T)
    return ret_mat

def Mahalanobis_1(output_k, avg_vi, cov_mat):  #由矩阵中的一行， 均值向量 和协方差矩阵 计算距离值
    ret = (output_k - avg_vi).T * cov_mat.I * (output_k - avg_vi)
    return ret

def Mahalanobis_2(cog_output, output):  #两个矩阵的计算马氏距离
    avg_vi = cal_avg_vi(output)
    cov_mat = cal_cov_mat(output)
    shape_v = cog_output.shape
    di = 0
    for i in range(shape_v[0]):
        cog_output_k = cog_output[i].T
        di_k = Mahalanobis_1(cog_output_k, avg_vi, cov_mat)
        di = di + di_k

    #retv = numpy.sqrt(di)
    return di[0, 0]

def Euclid_distance(cog_output, output):
    dif_arr = numpy.array(cog_output-output)
    dif_arr = dif_arr**2
    return numpy.sqrt(dif_arr.sum())
