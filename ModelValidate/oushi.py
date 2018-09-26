# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import zhi as zi
import pandas as pd

def oushidistance(ddd1,nn,mm1):
  print "欧式距离"
  # 模型数据
  dd1 = []
  y = ddd1
  #真实
  m = mm1

  print 'oushi model:%s' % y
  print 'oushi true:%s' % m

  n = nn
  for i in range(0,n):
    d=np.sqrt(np.sum(np.square(y-m[i])))
    #dd =  1 / (1 + np.sqrt(abs(d-sumx)))
    print d
    dd1.append(d)


  return dd1
