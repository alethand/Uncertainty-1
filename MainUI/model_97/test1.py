# -*- coding: utf-8 -*-
import math
import numpy as np
# 主函数，其中x是指变量的数组，a是指参数的数组
def function(x, a):
    t = x[0]
    dt1 = t
    dt2 = 2 * t
    dt3 = 3 * t
    Hw = x[1]
    vw = x[2]
    vc = x[4]
    Hwc = x[3]
    dy1 = dt1 * vw * math.sin(Hw)
    dy2 = dt2 * vw * math.sin(Hw)
    dy3 = dy2 + dt1 * vc * math.sin(Hwc)
    dx1 = dt1 * vc * math.cos(Hw)
    dx2 = dt2 * vc * math.cos(Hw)
    dx3 = dx2 + dt1 * vc * math.cos(Hwc)
    f0 = x[5]
    f1 = x[6]
    f2 = x[7]
    f3 = x[8]
    elem41 = (np.sin(f1) * dx1 - np.cos(f1) * dy1)
    elem42 = (np.sin(f2) * dx2 - np.cos(f2) * dy2)
    elem43 = (np.sin(f3) * dx3 - np.cos(f3) * dy3)
    elem11 = (np.sin(f1 - f0))
    elem12 = (np.sin(f2 - f0))
    elem13 = (np.sin(f3 - f0))
    elem21 = (np.sin(f1) * dt1)
    elem22 = (np.sin(f2) * dt2)
    elem23 = (np.sin(f3) * dt3)
    elem31 = (-np.cos(f1) * dt1)
    elem32 = (-np.cos(f2) * dt2)
    elem33 = (-np.cos(f3) * dt3)
    det = elem11 * elem22 * elem33 + elem21 * elem32 * elem13 + elem31 * elem12 * elem23 - elem11 * elem23 * elem32 - elem12 * elem21 * elem33 - elem31 * elem22 * elem13
    det1 = elem41 * elem22 * elem33 + elem21 * elem32 * elem43 + elem31 * elem42 * elem23 - elem41 * elem23 * elem32 - elem42 * elem21 * elem33 - elem31 * elem22 * elem43
    det2 = elem11 * elem42 * elem33 + elem41 * elem32 * elem13 + elem31 * elem12 * elem43 - elem11 * elem43 * elem32 - elem12 * elem41 * elem33 - elem31 * elem42 * elem13
    det3 = elem11 * elem22 * elem43 + elem21 * elem42 * elem13 + elem41 * elem12 * elem23 - elem11 * elem23 * elem42 - elem12 * elem21 * elem43 - elem41 * elem22 * elem13
    realD0 = det1 / det
    realVx = det2 / det
    realVy = det3 / det
    realVm = np.sqrt(realVx ** 2 + realVy ** 2)
    realHm = np.arctan(realVy / realVx)
    realHm = realHm * 180 / math.pi
    return realD0, realVm, realHm


# 参数：是指公式中的参数，类似于高斯分布中的segma
def description():
    param = []
    return param

def formula():
    param = []
    return param

# 变量，是指模型的输入
def descr_var():
    var = []
    var.append(['采样间隔时间', 't', '无量纲'])
    var.append(['我方航向', 'Hw', '无量纲'])
    var.append(['我方航速', 'Vw', '无量纲'])
    var.append(['变向后我方航向', 'Hwc', '无量纲'])
    var.append(['变向后我方航速', 'Vwc', '无量纲'])
    var.append(['第一次采样敌方方位', 'f0', '无量纲'])
    var.append(['第二次采样敌方方位', 'f1', '无量纲'])
    var.append(['第三次采样敌方方位', 'f2', '无量纲'])
    var.append(['第四次采样敌方方位', 'f3', '无量纲'])
    return var

