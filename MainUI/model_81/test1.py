# -*- coding: utf-8 -*-
import math
import numpy as np

import math
import numpy as np


class Torpedo:
    def __init__(self):
        # 不确定因素
        self.Vm = 0  # 目标速度
        self.Qm = 0  # 敌舷角
        self.Ds = 0  # 射距
        self.detaVm = 0  # 目标速度不确定量
        self.detaQm = 0  # 敌舷角不确定量
        self.detaDs = 0  # 射距不确定量

        self.T = 0  # 海水温度
        self.S = 0  # 海水盐度
        self.VO = 0  # 海流速度
        self.setaO = 0  # 海流速度方向与鱼雷速度方向夹角

        # 不确定因素影响的因素
        self.r = 0  # 鱼雷捕获半径
        self.faiA = 0  # 有利提前角
        self.fait = 0  # 鱼雷航向
        self.Vt = 0  # 鱼雷静水速度
        self.V = 0  # 鱼雷速度
        self.Q = 0  # 实时舷角

        # 确定参数
        self.Lambda = 0  # 水平半扇面角λ
        self.Xt = 0  # 鱼雷水平面坐标X
        self.Yt = 0  # 鱼雷水平面坐标Y
        self.Xm = 0  # 目标水平面坐标X
        self.Ym = 0  # 目标水平面坐标Y

        # 声呐方程 SL-2TL+TS=NL-DI+DT
        self.SL = 0  # 舰船、潜艇的辐射噪声SL
        self.TL = 0  # 传播损失TL
        self.TS = 0  # 目标反射强度TS
        self.NL = 0  # 鱼雷干扰噪声级NL
        self.DI = 0  # 自导接收指向性指数
        self.DT = 0  # 检测阈

        self.H = 0  # 鱼雷航深
        self.f = 0  # 鱼雷声呐声波频率
        self.beta = 0  # 对数声吸收系数

        # 输出
        self.success = 0  # 仿真结果（捕获成功1，捕获失败0）

    def setupDeta(self, detaV, detaQ, detaD):
        self.detaVm = detaV  # 目标速度不确定量
        self.detaQm = detaQ  # 敌舷角不确定量
        self.detaDs = detaD  # 射距不确定量

    def setupUncertain(self, T, S, VO, setaO):
        self.T = T  # 海水温度
        self.S = S  # 海水盐度
        self.VO = VO  # 海流速度
        self.setaO = setaO  # 海流速度方向鱼雷速度方向夹角

    def Initialization(self):
        # 初始化声呐方程并获取探测半径r
        self.setR()
        # 初始化发射角（有利提前角）
        m = self.Vm / self.Vt
        k = 2 * np.sin(self.Lambda) / (3 * self.Lambda)
        b = np.arctan(k * m * self.r * np.sin(self.Qm) / (self.Ds + k * m * self.r * np.cos(self.Qm)))
        self.faiA = np.arctan(m * np.sin(self.Qm - b)) - b
        # 航向
        self.fait = np.pi - self.faiA - self.Qm
        # 实时舷角
        self.Q = self.Qm
        # 误差
        self.Vm += self.detaVm  # 目标速度
        self.Qm += self.detaQm  # 敌舷角
        self.Ds += self.detaDs  # 射距
        # 目标初始水平面坐标X
        self.Xm = -self.Ds * (np.cos(self.Qm))
        # 目标初始水平面坐标Y
        self.Ym = self.Ds * (np.sin(self.Qm))
        # 方向合成
        self.fait += np.arctan(self.VO * np.sin(self.setaO) / (self.Vt + self.VO * np.cos(self.setaO)))
        # 速度合成
        self.V = np.sqrt(self.Vt ** 2 + self.VO ** 2 + 2 * np.cos(self.setaO) * (self.Vt * self.VO))

    def setup(self, vm, vt, qm, ds, lam, Di, Dt, h, f):
        self.Vm = vm  # 目标速度
        self.Vt = vt  # 鱼雷静水速度
        self.Qm = qm  # 敌舷角
        self.Ds = ds  # 射距
        self.Lambda = lam  # 水平半扇面角λ
        self.DI = Di  # 自导接收指向性指数
        self.DT = Dt  # 检测阈
        self.H = h  # 鱼雷航深
        self.f = f  # 鱼雷声呐声波频率
        self.Xt = 0  # 鱼雷初始水平面坐标X
        self.Yt = 0  # 鱼雷初始水平面坐标Y

    def update(self, t):
        # 目标水平面坐标X
        self.Xm = self.Xm + t * self.Vm
        # 鱼雷水平面坐标X
        self.Xt += t * np.cos(self.fait) * self.V
        # 鱼雷水平面坐标Y
        self.Yt += t * np.sin(self.fait) * self.V

    def simulation(self, t):
        self.success = 0
        d = (self.Xm - self.Xt) ** 2 + (self.Ym - self.Yt) ** 2 - self.r ** 2
        # print("Xm =",self.Xm)
        # print("Ym =",self.Ym,'\n')

        while (self.Yt <= self.Ym and self.success == 0):
            self.setR()
            self.update(t)
            d = (self.Xm - self.Xt) ** 2 + (self.Ym - self.Yt) ** 2 - self.r ** 2
            # print( "d =",d )
            # print( "r =",self.r )

            dotmetrix = (self.Xm - self.Xt) * self.Xt + (self.Ym - self.Yt) * self.Yt
            d1 = np.sqrt((self.Xm - self.Xt) ** 2 + (self.Ym - self.Yt) ** 2)
            d2 = np.sqrt(self.Xt ** 2 + self.Yt ** 2)
            fai = np.arccos(np.abs(dotmetrix) / (d1 * d2))
            # print("Xm =",self.Xm)
            # print("Xt =",self.Xt)
            # print("Yt =",self.Yt)
            # print("V =",self.V)
            # print("fait =",self.fait)
            # print("fai =",fai/np.pi/2*360,'\n')

            if (d <= 0 and fai <= self.Lambda):
                self.success = 1

    def setSL(self):
        if (self.Vm < 1.852 * 12 / 3.6):
            self.SL = 25 * np.log(self.Vm) + 77
        else:
            self.SL = 104 + 1.8 * (self.Vm - 12)

    def setbeta(self):
        fp = 263 * self.T * 1000 * (10 ** (-1722 / self.T))
        K = 1.42 * (10 ** (-8)) * (10 ** (1240 / self.T))
        self.beta = 2 * np.pi * self.T * self.S * self.f * (10 ** (-5)) / (fp / self.f + self.f / fp) + K * (
                    self.f ** 2)

    def setTL(self):
        self.setSL()
        self.setTS()
        self.setNL()
        self.TL = (self.SL + self.TS - self.NL + self.DI - self.DT) / 2

    def setQ(self):
        # 实时舷角
        if (self.Xm == self.Xt):
            self.Q = np.pi / 2
        else:
            a = np.arctan((self.Ym - self.Yt) / (self.Xm - self.Xt))
            if (a > 0):
                self.Q = a + np.pi / 2
            else:
                self.Q = -a

    def setTS(self):
        self.setQ()
        S = np.pi * np.sqrt((50 * np.sin(self.Q)) ** 2 + (5 * np.cos(self.Q)) ** 2)
        Va = 1.1 + 2.1 * (self.Q ** 3.8) + 3.35 * self.Q * np.sin(3.94 * np.sqrt(self.Q))
        self.TS = 10 * np.log10((S * Va) / (4 * np.pi))

    def setNL(self):
        PN = 34037 * np.exp(-0.0766526 * self.H) + 398  # 鱼雷航行自噪声声压
        self.NL = 20 * np.log10(PN)

    def setR(self):
        self.setbeta()
        self.setTL()
        a = 1.0
        b = 500.0
        temp = 0.0
        mr = 1.0
        for i in range(1, 100):
            mr = (a + b) / 2
            temp = 20 * np.log(mr) + self.beta * mr * 0.001 - self.TL
            if (temp > 0):
                b = mr
            else:
                a = mr
        self.r = mr


# 主函数，其中x是指变量的数组，a是指参数的数组
def function(x, a):
    nn = Torpedo()

    #detaVm目标速度不确定量     a[0]
    #detaQm敌舷角不确定量       a[1]
    #detaDs射距不确定量         a[2]
    #nn.setupDeta(3,1/360*2*np.pi,5)
    nn.setupDeta(a[0],a[1],a[2])
    #vm             目标速度            x[0]    
    #vt             鱼雷静水速度        x[1]     
    #qm             敌舷角              x[2]    
    #ds             射距                x[3]   
    #lam            水平半扇面角λ       x[4]    
    #Di             自导接收指向性指数      x[5]
    #Dt             检测阈                  x[6]
    #h              鱼雷航深(m)             x[7]
    #f              鱼雷声呐声波频率(kHz)   x[8]
    #nn.setup(15,30,np.pi/3,500,np.pi/6,150,80,2000,10)

    nn.setup(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
    #海水温度T      a[3]
    #海水盐度S      a[4]
    #海流速度VO     a[5]
    #海流速度方向与鱼雷速度方向夹角setaO    a[6]
    # nn.setupUncertain(280,30/100,0,0)
    nn.setupUncertain(a[3],a[4],a[5],a[6])

    nn.Initialization()

    nn.simulation(0.1)

    return nn.success,



# 参数：是指公式中的参数，类似于高斯分布中的segma
def description():
    param = []
    # detaVm目标速度不确定量     a[0]
    # detaQm敌舷角不确定量       a[1]
    # detaDs射距不确定量         a[2]
    # 海水温度T      a[3]
    # 海水盐度S      a[4]
    # 海流速度VO     a[5]
    # 海流速度方向与鱼雷速度方向夹角setaO    a[6]
    param.append(['目标速度不确定量', 'detaVm', '无量纲'])
    param.append(['敌舷角不确定量', 'detaQm', '无量纲'])
    param.append(['射距不确定量', 'detaDs', '无量纲'])
    param.append(['海水温度', 'T', '无量纲'])
    param.append(['海水盐度', 'S', '无量纲'])
    param.append(['海流速度', 'VO', '无量纲'])
    param.append(['海流速度方向与鱼雷速度方向夹角', 'setaO', '无量纲'])
    return param

# 变量，是指模型的输入
def descr_var():
    var = []
    # vm             目标速度            x[0]
    # vt             鱼雷静水速度        x[1]
    # qm             敌舷角              x[2]
    # ds             射距                x[3]
    # lam            水平半扇面角λ       x[4]
    # Di             自导接收指向性指数      x[5]
    # Dt             检测阈                  x[6]
    # h              鱼雷航深(m)             x[7]
    # f              鱼雷声呐声波频率(kHz)   x[8]
    var.append(['目标速度', 'vm', '无量纲'])
    var.append(['鱼雷静水速度', 'vt', '无量纲'])
    var.append(['敌舷角', 'qm', '无量纲'])
    var.append(['射距', 'ds', '无量纲'])
    var.append(['水平半扇面角λ', 'lam', '无量纲'])
    var.append(['自导接收指向性指数', 'Di', '无量纲'])
    var.append(['检测阈', 'Dt', '无量纲'])
    var.append(['鱼雷航深', 'h', '无量纲'])
    var.append(['鱼雷声呐声波频率', 'f', '无量纲'])


    return var

def run_simu_model(cog_p_1, input_x1):
    theX = cog_p_1 + input_x1 + 40000
    # shape_v = input_X.shape
    # n = shape_v[0]
    # rans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[0])
    # for i in range(n):
    #     if i == 0:
    #         continue
    #     tans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[i])
    #     rans = numpy.row_stack((rans, tans))
    # return numpy.mat(rans)
    return theX
