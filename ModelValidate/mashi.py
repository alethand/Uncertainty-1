# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import zhi as zi
import pandas as pd

def mashidistance(ddd4,nn4,mm4):
 dd1 = []
 y = ddd4
 m = mm4
 n = nn4
 X = np.vstack(map(list,zip(*m)))#逆转矩阵  变为 100 个维度为5 的矩阵
#Y = np.vstack(y)
 XT = X.T

# 方法一：根据公式求解
 print "-----------------"
 print X
 print "-----------------"
 S = np.cov(X)  # 两个维度之间协方差矩阵
 S = np.mat(S)
 print "+++++++++++++++++"
 print S
 print "+++++++++++++++++"
 print "+++++++++++++++++"
 print np.linalg.pinv(S)
 print "+++++++++++++++++"
 SI = np.linalg.pinv(S)  # 协方差矩阵的逆矩阵
# 马氏距离计算两个样本之间的距离，此处共有10个样本，两两组合，共有45个距离。
 n = XT.shape[0]
 print "马氏距离"
 for i in range(0, n):
    #for j in range(i + 1, n):
        delta = y - XT[i]
        d = np.sqrt(np.dot(np.dot(delta, SI), delta.T))
        print d
        dd1.append(d)
 return dd1
#print("马氏距离")
#print(d4)
def figure_ms(y,n,m):
 plt.figure("8")
 d4 = mashidistance(y,n,m)
 ax7=plt.subplot(221)#在图表2中创建子图1
 s7 = pd.Series(np.array(d4))
 data4 = pd.DataFrame({"Simulation of Markov distance": s7 })
 plt.title("Markov distance")
 data4.boxplot()
 ax8=plt.subplot(222)
# make a histogram of the data array
 num_list4 = zi.Orang(d4,len(d4))
 name_list = ['sum','var','1/4','3/4','median']
 plt.title("data")
 plt.bar(range(len(num_list4)), num_list4,color='black',tick_label=name_list)
 plt.show()