# -*- coding: utf-8 -*-

import numpy as np

#求 中位数 平均数 1/4  3/4 方差
def Orang(dd,nn):
  array = dd
  n = nn
  for i in range(0,n):
    for j in range(i):
        if array[j] > array[j + 1]:
            array[j], array[j + 1] = array[j + 1], array[j]

  narray=np.array(array)
  sum1=narray.sum()
  narray2=narray*narray
  sum2=narray2.sum()
  mean=sum1/n
  sumo = sum(array)/n##
  varo = np.std(dd, ddof=1)
#求中位数
  if n % 2 == 0:
    ozw = (array[n/2]+array[n/2-1])/2
  else:
    ozw = array[(n-1)/2]


#求上四分之一位
  fouro1,four2,fouro3 = np.percentile(array,(25,50,75))
  #
  # if n%4 == 0:
  #   fouro1 = (array[n/4]+array[n/4-1])/2
  #   fouro3 = (array[(n/2+n)/2] + array[(n/2+n)/2-1]) / 2
  #
  #
  # if n%4 == 1:
  #   fouro1 = (array[((n+1)/2+1)/2-1])
  #   fouro3 = (array[((n+1)/2+n)/2-1])
  #
  # ###
  # if n%4 == 2:
  #   fouro1 = (array[(n/2+1)/2-1])
  #   fouro3 = (array[(n/2+1+n)/2-1]+array[(n/2+1+n)/2])/2
  # if n%4 == 3:
  #   fouro1 = array[(n+1)/4-1]
  #   fouro3 = array[3*(n + 1)/4-1]
  print "均值："
  print sumo
  print "方差："
  print varo
  print "四分之一位数："
  print fouro1
  print "四分之三位数："
  print fouro3
  print "中位数："
  print ozw

  return sumo,varo,fouro1,fouro3,ozw
