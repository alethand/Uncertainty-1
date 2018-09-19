# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.stats
import zhi as zi
import pandas as pd
def KLdistanse(y,m):
 yyy = np.array(y)
 mmm = np.array(m)
 n = len(yyy)
 nn = len(mmm)
 yy = []
 mm = []
 if n > nn and n == nn:
  for i in range(0, nn):
   mm.append(mmm[i])
  yy = yyy

 if n < nn:
  for i in range(0, n):
   yy.append(yyy[i])
   mm = mmm
 print y
 print m
#print(py)
 KL = scipy.stats.entropy(y, m)
 print KL
 return KL

def figure_kl(y,m):
 plt.figure("4")
 KL = KLdistanse(y,m)
 if len(KL) == 1:
  x = [1]
  plt.title("KL")
  plt.bar(x, KL, color='black', tick_label=x)
  plt.show()

 if len(KL) == 2:
  x = [1,2]
  plt.title("KL")
  plt.bar(x, KL,0.1,color='black', tick_label=x)
  plt.xlabel("X-output")
  plt.ylabel("Y-kl")
  plt.show()

 if len(KL) == 3:
  x = [1,2,3]
  plt.title("KL")
  plt.bar(x, KL, 0.1, color='black', tick_label=x)
  plt.xlabel("X-output")
  plt.ylabel("Y-kl")
  plt.xlabel("X-output")
  plt.ylabel("Y-kl")
  plt.show()

 if len(KL) == 4:
  x = [1,2,3,4]
  plt.title("KL")
  plt.bar(x, KL, 0.1, color='black', tick_label=x)
  plt.xlabel("X-output")
  plt.ylabel("Y-kl")
  plt.show()

 if len(KL) > 4:
  ax9=plt.subplot(221)#在图表2中创建子图1
  s2 = pd.Series(np.array(KL))
  data1 = pd.DataFrame({"KL": s2})
  plt.title("KL")
  num_list5 = zi.Orang(KL,len(KL))
  data1.boxplot()  # 这里，pandas自己有处理的过程，很方便哦。
  ax10=plt.subplot(222)
  name_list = ['sum','var','1/4','3/4','median']
  plt.title("data")
  plt.bar(range(len(num_list5)), num_list5,color='black',tick_label=name_list)
  plt.show()

