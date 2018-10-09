# -*- coding: utf-8 -*-
import numpy as np
import sklearn
import scipy.spatial.distance as dis
import data_related as dr
import CalculateMethod as clm
# data_model,data_observation都得是矩阵mat
def euclidean(data_model, data_observation):
    data_model,data_observation=np.mat(data_model),np.mat(data_observation)
    num_cols=data_observation.shape[1]
    res=0
    if num_cols==1:
        res=dis.euclidean(data_model,data_observation)
    else:
        distance=dis.cdist(data_model,data_observation,'euclidean')
        res=np.mean(np.diag(distance))
    return res


def manhattan(data_model, data_observation):
    data_model,data_observation=np.mat(data_model),np.mat(data_observation)
    num_cols=data_observation.shape[1]
    res=0
    if num_cols==1:
        res=dis.cityblock(data_model,data_observation)
    else:
        distance=dis.cdist(data_model,data_observation,'cityblock')
        res=np.mean(np.diag(distance))
    return res


def chebyshev(data_model, data_observation):
    data_model,data_observation=np.mat(data_model),np.mat(data_observation)
    num_cols=data_observation.shape[1]
    res=0
    if num_cols==1:
        res=dis.chebyshev(data_model,data_observation)
    else:
        distance = dis.cdist(data_model, data_observation, 'chebyshev')
        res = np.mean(np.diag(distance))
    return res


def mahalanobis(data_model, data_observation):
    # data_model,data_observation=np.mat(data_model),np.mat(data_observation)
    # clm.mahalanobis(data_model,data_observation)
    pass


def KL(data_model, data_observation):
    return 2


if __name__ == '__main__':
    # a=np.random.normal(10,20,10)
    # b=np.random.rand(10)
    # a=np.array([[1,0,0])
    # b=np.array([0,1,0])

    # a = np.array([[10,2],
    #               [8,4],
    #               [3,8]])
    #
    #
    # b = np.array([[1,2],
    #                [2,5],
    #                [3,7]])

    # a=np.mat([[1,2],[2,2],[3,4]])
    # b=np.mat([[7,2],[8,1],[9,6]])
    model_d=dr.model_d
    real_d=dr.real_d
    print model_d.shape
    print real_d.shape
    for i in np.arange(model_d.shape[0]):
        print euclidean(model_d[i], real_d)
        print manhattan(model_d[i], real_d)
        print '----'
    # print mahalanobis(model_d[0],real_d)
