# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import zhi as zi
import pandas as pd

def oushidistance(ddd1,nn,mm1):
  print "欧式距离"
  dd1 = []
  y = ddd1
  m = mm1
  n = nn
  for i in range(0,n):
    d=np.sqrt(np.sum(np.square(y-m[i])))
    #dd =  1 / (1 + np.sqrt(abs(d-sumx)))
    print d
    dd1.append(d)


  return dd1


def figure_ou(y,n,m):
 plt.figure("5")
#plt.figure(2)#创建图表2
 d1 = oushidistance(y,n,m)


 ax1=plt.subplot(221)#在图表2中创建子图1
 s1 = pd.Series(np.array(d1))
 data1 = pd.DataFrame({"Simulation of Euclidean distance": s1})
#plt.ylabel("ylabel")
#plt.xlabel("xlabel")
 plt.title("Euclidean distance")
 data1.boxplot()  # 这里，pandas自己有处理的过程，很方便哦
 ax2=plt.subplot(222)
# make a histogram of the data array
 num_list1 = zi.Orang(d1,len(d1))
 name_list = ['sum','std','1/4','3/4','median']
 plt.title("data")
 plt.bar(range(len(num_list1)), num_list1,color='black',tick_label=name_list)
 plt.show()
 return d1