# -*- coding: utf-8 -*
from __future__ import division
import numpy as np
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

def mahalanobis(cog_output, output):  #两个矩阵的计算马氏距离
    print 'cog_output=====output'
    print cog_output, output
    avg_vi = cal_avg_vi(output)
    cov_mat = cal_cov_mat(output)
    shape_v = cog_output.shape
    di = 0
    for i in range(shape_v[0]):
        cog_output_k = cog_output[i].T
        di_k = Mahalanobis_1(cog_output_k, avg_vi, cov_mat)
        di = di + di_k
    md1 = mahal_vector(cog_output.A1, output.A1)  # mat to array
    print 'di========', di[0, 0], md1
    return di[0, 0]

def euclidean(cog_output, output):
    dif_arr = numpy.array(cog_output-output)
    dif_arr = dif_arr**2
    return numpy.sqrt(dif_arr.sum())

def mahal(obs, pred):  # input two arrays of m dimension
    print obs, pred
    if obs.shape[1] != pred.shape[1]:
        print 'the dimension of matrices can not match'
        return
    mu = np.mean(pred, axis=0)
    sigma = np.cov(pred.T)
    row = obs.shape[0]
    result = []
    for i in range(0, row):
        delta = obs[i] - mu
        d = np.sqrt(np.dot(np.dot(delta, np.linalg.inv(sigma)), delta.T))
        result.append(d)
    result = np.mat(result)
    return result.T  # return a column vector


def mahal_vector(vec1, vec2):  # input data must be array
    npvec = np.vstack([vec1, vec2])
    sub = npvec.T[0] - npvec.T[1]
    inv_sub = np.linalg.inv(np.cov(npvec))
    return np.sqrt(np.dot(inv_sub, sub).dot(sub.T))


def mahalanobis1(obs, pred):  # input data must be mat form
    if obs.shape[1] < 2 or obs.shape[0] < 2:  # input vector
        md1 = mahal_vector(obs.A1, pred.A1)  # mat to array
    else:  # input matrix
        obs = np.array(obs)
        pred = np.array(pred)
        md1 = mahal(obs, pred)
    return np.sum(md1)
