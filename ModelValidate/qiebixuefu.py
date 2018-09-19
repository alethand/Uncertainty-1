# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import zhi as zi
import pandas as pd
def qiebixuefudistance(ddd3,nn3,mm3):
  print "切比雪夫距离"
  dd1 = []
  y = ddd3
  m = mm3
  n = nn3
  for i in range(0,n):
     d=np.max(np.abs(y-m[i]))
     dd1.append(d)
     print d
  return dd1


def figure_qbxf(y,n,m):
 plt.figure("7")
 ax5=plt.subplot(221)#在图表2中创建子图1
 d3 = qiebixuefudistance(y,n,m)
 s5 = pd.Series(np.array(d3))
 data3 = pd.DataFrame({"Simulation of Chebyshev distance": s5})
 plt.title("Chebyshev distance")
 data3.boxplot()
 ax6=plt.subplot(222)
# make a histogram of the data array
 num_list3 = zi.Orang(d3,len(d3))
 name_list = ['sum','var','1/4','3/4','median']
 plt.title("data")
 plt.bar(range(len(num_list3)), num_list3,color='black',tick_label=name_list)
 plt.show()