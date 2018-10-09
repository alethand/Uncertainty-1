# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
import distance as dis

sns.set()

np.set_printoptions(2, suppress=True)
pd.set_option('display.max_colwidth', 100)


np.random.seed(0)

# # 暂时用不到
# # 得到一个cog和sim之间的字典
# def get_cog_sim_dict():
#     cog_sim_dict={}
#     cog_sim_euc=model_simiarity(cog_p, inh_p, input_X, real_d, dis.euclidean)
#     cog_sim_man = model_simiarity(cog_p, inh_p, input_X, real_d, dis.manhattan)
#     cog_sim_che= model_simiarity(cog_p, inh_p, input_X, real_d, dis.chebyshev)
#     n=cog_sim_euc.shape[0]
#     for i in np.arange(n):
#         name='cog_{}'.format(i)
#         cog_sim_dict[name]={}
#         cog_sim_dict[name]['euc']=cog_sim_euc[i]
#         cog_sim_dict[name]['man']=cog_sim_man[i]
#         cog_sim_dict[name]['che']=cog_sim_che[i]
#
#     # print cog_sim_dict
#     return cog_sim_dict
# # 暂时用不到
# # 得到一个cog与输出、sim之间的关系的字典
# def get_cog_dict(model_d,cog_sim_dict):
#     cog_dict={}
#     n=model_d.shape[0]
#     for i in np.arange(n):
#         name='cog_{}'.format(i)
#         cog_dict[name]={}
#         cog_dict[name]['output_avg']=model_d[i]
#         cog_dict[name]['simlarity']=cog_sim_dict[name]
#     print cog_dict

# 这里是模型输出
def f1(theta, eps, x):
    return np.random.normal(theta[0], np.abs(eps[0])) * 0.5 * x,np.random.normal(theta[1], np.abs(eps[1])) * x
    # return np.cos(x+theta[0])+eps[0],np.sin(theta[1]**x)+eps[1]
    # return np.exp(x*theta[0])+eps[0],np.sin(theta[1]*x)*x+eps[1]


def f2(theta, eps, x):
    return np.cos(0.25 * np.pi * x) * theta + 0.2 * x + eps, eps


# 输出和input_X一致的输出矩阵
def run_model(cog_p_r, inh_p_r, input_X, cal_func):
    res = cal_func(cog_p_r, inh_p_r, input_X[0])
    for i in np.arange(len(input_X)):
        if i == 0:
            continue
        tmp = cal_func(cog_p_r, inh_p_r, input_X[i])
        res = np.row_stack((res, tmp))
    return np.mat(res)


# 生成真实数据和input_X维度要一致
def real_data(cog_p, inh_p, input_X, cal_func):
    global cog_real
    cog = (cog_p[0] + cog_p[1]) / 2
    cog_real = cog
    res = run_model(cog, inh_p[0], input_X, cal_func)
    for i in np.arange(len(inh_p)):
        if i == 0:
            continue
        tmp = run_model(cog, inh_p[i], input_X, cal_func)
        res = res + tmp
    res = res / len(inh_p)
    return res


# 消除固有参数影响
def eliminate_inh_p(cog_p_r, inh_p, input_X, cal_func):
    cog = cog_p_r
    res = run_model(cog, inh_p[0], input_X, cal_func)
    for i in np.arange(len(inh_p)):
        if i == 0:
            continue
        tmp = run_model(cog, inh_p[i], input_X, cal_func)
        res = res + tmp
    res = res / len(inh_p)
    return res


# 用不同的相似性函数计算认知参数对应的相似度
def model_simiarity(cog_p, inh_p, input_X, real_data, simlarity_func):
    cog_simlarity = []
    for i in np.arange(len(cog_p)):  # 每一组认知不确定参数
        cog_pi_output = eliminate_inh_p(cog_p[i], inh_p, input_X, f1)
        simlarity = simlarity_func(cog_pi_output, real_data)
        cog_simlarity.append(simlarity)
    return np.array(cog_simlarity)

# 计算模型数据和真实数据的相似度
def cal_simiarity(model_d, real_d, simlarity_func):
    cog_simlarity = []
    for i in np.arange(model_d.shape[0]):  # 每一组认知不确定参数
        simlarity = simlarity_func(model_d[i], real_d)
        cog_simlarity.append(simlarity)
    return np.array(cog_simlarity)

# 生成模型数据，每个认知参数对应一个输出
def model_data(cog_p, inh_p, input_X, cal_func):
    data = []
    for i in np.arange(len(cog_p)):  # 每一组认知不确定参数
        cog_pi_output = eliminate_inh_p(cog_p[i], inh_p, input_X, cal_func)
        data.append(cog_pi_output)
    return np.array(data)


# 返回相似性字典，为了生成dataframe
def get_cog_sim_fordf():
    cog_sim = {}
    cog_sim_euc = model_simiarity(cog_p, inh_p, input_X, real_d, dis.euclidean)
    cog_sim_man = model_simiarity(cog_p, inh_p, input_X, real_d, dis.manhattan)
    cog_sim_che = model_simiarity(cog_p, inh_p, input_X, real_d, dis.chebyshev)
    cog_sim['euc'] = cog_sim_euc
    cog_sim['man'] = cog_sim_man
    cog_sim['che'] = cog_sim_che
    # print cog_sim
    return cog_sim


def get_dataframe(model_d, sim_dict):
    model_d_list = []
    cog_names = []
    for i in np.arange(model_d.shape[0]):
        model_d_list.append([model_d[i]])
        cog_names.append('cog_{}'.format(i))
    cog_dataframe = pd.DataFrame(cog_names, columns=['cog_name'])
    cog_dataframe['output_avg'] = model_d_list
    sim_names = sim_dict.keys()
    for sim_na in sim_names:
        cog_dataframe[sim_na] = sim_dict[sim_na]

    # print cog_dataframe.head()
    return cog_dataframe


# 比较不同距离对认知输出和真实差异的显示程度
def draw_distance_box(cog_dataframe, sim_names,axes):
    """
    专门用来画盒状图
    :param cog_dataframe:
    :param sim_names:
    :return:
    """
    if set(sim_names) <= set(cog_dataframe.columns.values):
        pass
    else:
        print 'cog_dataframe 里面并没有相对应的相似性度量'
        return None
    # plt.figure()
    a = cog_dataframe
    ax = cog_dataframe.plot(y=sim_names, kind='box',ax=axes)
    # ----------------------------------------

    # tips = sns.load_dataset("tips")

    # ax = sns.violinplot(x = cog_dataframe[sim_names],ax=axes)

    # data = pd.DataFrame(dict(d1=cog_dataframe[sim_names]))
    #
    # ax = sns.violinplot(data)
    # ax = cog_dataframe.plot(y=sim_names, kind='violin', ax=axes)

    # -----------------------------------------

    ax.set_ylabel('distance')
    # plt.show()
    return ax

# 比较不同距离对认知输出和真实差异的显示程度
def draw_distance_violin(cog_dataframe, sim_names,axes):
    """
    专门用来画盒状图
    :param cog_dataframe:
    :param sim_names:
    :return:
    """
    if set(sim_names) <= set(cog_dataframe.columns.values):
        pass
    else:
        print 'cog_dataframe 里面并没有相对应的相似性度量'
        return None
    # plt.figure()
    a = cog_dataframe
    # ax = cog_dataframe.plot(y=sim_names, kind='box',ax=axes)
    # ----------------------------------------

    # tips = sns.load_dataset("tips")

    ax = sns.violinplot(y = cog_dataframe[sim_names],alpha=0.4,ax=axes)
    # , color = "#6890F0"

    # ax.set_ylim(0,8)

    # data = pd.DataFrame(dict(d1=cog_dataframe[sim_names]))
    #
    # ax = sns.violinplot(data)
    # ax = cog_dataframe.plot(y=sim_names, kind='violin', ax=axes)

    # -----------------------------------------

    ax.set_ylabel('distance')
    ax.set_xlabel(sim_names[0])

    # plt.show()
    return ax


def draw_dis_distri(cog_dataframe, sim_name,axes):
    if sim_name in set(cog_dataframe.columns.values):
        pass
    else:
        print 'cog_dataframe 里面并没有相对应的相似性度量'
        return None
    # plt.figure()
    ax = sns.distplot(cog_dataframe[sim_name], rug=True,ax=axes)
    # ------------------------------------------
    # ax = sns.pairplot(cog_dataframe[sim_name], vars=["sepal width", "sepal length"],hue='class',palette="husl")
    # a = cog_dataframe
    # ax = sns.pointplot(x = range(len(cog_dataframe['cog_name'])), y = cog_dataframe[sim_name], alpha=0.8,ax=axes)
    # ax = sns.lineplot(np.arange(self.data_panel.num_rows), y=0, data=real_df, ax=ax)

    # ------------------------------------

    ax.set_xlabel(sim_name)
    ax.set_ylabel('pdf')
    return ax


def draw_dis_point(cog_dataframe, sim_name,axes):
    if sim_name in set(cog_dataframe.columns.values):
        pass
    else:
        print 'cog_dataframe 里面并没有相对应的相似性度量'
        return None
    # plt.figure()
    # ax = sns.distplot(cog_dataframe[sim_name], rug=True,ax=axes)
    # ------------------------------------------
    # ax = sns.pairplot(cog_dataframe[sim_name], vars=["sepal width", "sepal length"],hue='class',palette="husl")
    # a = cog_dataframe
    ax = sns.pointplot(x = range(len(cog_dataframe['cog_name'])), y = cog_dataframe[sim_name], alpha=0.8,ax=axes)
    # ax = sns.lineplot(np.arange(self.data_panel.num_rows), y=0, data=real_df, ax=ax)

    # ------------------------------------

    ax.set_xlabel(sim_name)
    ax.set_ylabel('pdf')
    return ax


def myPCA(data, n_components=2):
    pca = PCA(n_components)
    new_data = pca.fit_transform(data)
    # print new_data
    return new_data


# 用来外面执行生成数据操作
# ---------------------------------------------------------------------------------


cog_p = np.random.uniform(1, 10, (10, 2))
inh_p = np.random.normal(0, 1, (5, 2))
input_X = np.random.rand(10)
cog_real = 0
#
# 选定一组特定的认知，生成真实数据
real_d = real_data(cog_p, inh_p, input_X, f1)
print 'real_d: {} shape:{}'.format(real_d, real_d.shape)
# 遍历认知，生成模型数据
model_d = model_data(cog_p, inh_p, input_X, f1)
print 'model_d: {} shape:{}'.format(model_d, model_d.shape)