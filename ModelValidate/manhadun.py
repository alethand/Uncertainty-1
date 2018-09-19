# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import zhi as zi
import pandas as pd

def manhadundistance(ddd2,nn1,mm2):
#方法一：根据公式求解
  dd1 = []
  y = ddd2
  m = mm2
  n = nn1

  print "sd"
  print n

  print "曼哈顿距离"
  for i in range(0,n):
    d = np.sum(np.abs(y-m[i]))
    print d
    dd1.append(d)

  return dd1


def figure_mh(y,n,m):
 plt.figure("6")
 ax3=plt.subplot(221)#在图表2中创建子图1
 d2 = manhadundistance(y,n,m)   #调用曼哈顿距离公式y 是仿真数据  m样本数据 n 样本数据个数
 s3 = pd.Series(np.array(d2))
 data2 = pd.DataFrame({"Simulation of Manhattan distance": s3})
 plt.title("Manhattan distance")
 data2.boxplot()
 ax4=plt.subplot(222)
# make a histogram of the data array
 num_list2 = zi.Orang(d2,len(d2))
 name_list = ['sum','std','1/4','3/4','median']
 plt.title("data")
 plt.bar(range(len(num_list2)), num_list2,color='black',tick_label=name_list)
 plt.show()