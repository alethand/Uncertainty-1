import numpy as np
import matplotlib.pyplot as plt

def a(a,b):
    return a+b

def b(a,b):
    return a*b

def add(a,b,cal_fun):
    res=cal_fun(a,b)
    print res

add(2,5,a)
add(2,5,b)