# encoding=utf8 
import math
import numpy
import scipy.integrate as integrate
import numpy as np
import random
# import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf8')


KN = 1.852

def function(x, a):
    xNum1 = 1
    xNum2 = 9
    xNum3 = 8
    xNum4 = 9
    aNum1 = 4
    aNum2 = 0
    aNum3 = 7
    aNum4 = 3

    x2 = [x[i] for i in range(xNum1, xNum1+xNum2)]
    a2 = []
    model2result = function2_MotionElement(x2, a2)
    vm = model2result[1]

    x1 = [x[i] for i in range(0, xNum1)]
    x3 = [vm, x[0+xNum1+xNum2], x[1+xNum1+xNum2], x[2+xNum1+xNum2], x[3+xNum1+xNum2], x[4+xNum1+xNum2], x[5+xNum1+xNum2], x[6+xNum1+xNum2], x[7+xNum1+xNum2]]
    x4 = [x[0+xNum1+xNum2+xNum3], x[1+xNum1+xNum2+xNum3], x[2+xNum1+xNum2+xNum3], x[3+xNum1+xNum2+xNum3], x[4+xNum1+xNum2+xNum3],vm, x[5+xNum1+xNum2+xNum3], x[6+xNum1+xNum2+xNum3], x[7+xNum1+xNum2+xNum3], x[8+xNum1+xNum2+xNum3]]

    a1 = [a[0],a[1],a[2],a[3],vm]
    a3 = [a[i] for i in range(aNum1+aNum2, aNum1+aNum2+aNum3)]
    a4 = [a[i] for i in range(aNum1+aNum2+aNum3, aNum1+aNum2+aNum3+aNum4)]

    model1result = function1_targetDetect(x1, a1)
    model3result = function3_TorpedoDetect(x3, a3)
    model4result = function4_torpedoTrack(x4, a4)

    result = model1result[0],model2result[0],model2result[1],model2result[2],model3result[0],model4result[0][0],
# x = [theX[i] for i in range(len(theX))]

    # presult=solve(n=n, r=r, d=d, v=v, p=p, t=t)
    # presult = solve()
    return result


# a参数：是指公式中的参数，类似于高斯分布中的segma
# a model,number = 1,4+1 = 5; 2,0; 3,7; 4,3
def description():
    param = []
    # model1_targetDetct
    # 1 海里=1.852 km
    # n 浮标个数
    # r 浮标半径 单位为海里
    # d 浮标相隔距离 单位为海里 4*r/3<d<根号3*r
    # v 敌方速率 单位为节数
    # p 声纳识别概率 [0.2, 0.6]
    # t 总搜索时间 单位为小时
    param.append(['潜标数量', 'n', '正整数'])
    param.append(['潜标半径', 'r', '单位：海里'])
    param.append(['两个潜标之间间隔', 'd', '单位：海里'])
    param.append(['单个潜标探测概率', 'p', '0-1'])
    # param.append(['敌方潜艇速度', 'v', '单位：海里/小时'])

    # model2_motionElement
    # null

    # model3_TorpedoDetct
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

    # model4_torpedoTrack
    param.append(['追踪段航程', 'lt', '无量纲'])
    param.append(['鱼雷自导作用距离', 'l3', '无量纲'])
    param.append(['最小弹道曲率半径', 'rmin', '无量纲'])
    return param

# x变量，是指模型的输入
# x model,number = 1,1; 2,9; 3,8+1 = 9; 4,9+1 = 10 
# v x 3,0 4,5
def descr_var():
    var = []
    # model1_targetDetct
    var.append(['时间', 't', '单位：小时'])

    # model2_motionElement
    var.append(['采样间隔时间', 't', '无量纲'])
    var.append(['我方航向', 'Hw', '无量纲'])
    var.append(['我方航速', 'Vw', '无量纲'])
    var.append(['变向后我方航向', 'Hwc', '无量纲'])
    var.append(['变向后我方航速', 'Vwc', '无量纲'])
    var.append(['第一次采样敌方方位', 'f0', '无量纲'])
    var.append(['第二次采样敌方方位', 'f1', '无量纲'])
    var.append(['第三次采样敌方方位', 'f2', '无量纲'])
    var.append(['第四次采样敌方方位', 'f3', '无量纲'])

    # model3_TorpedoDetct
    # vm             目标速度            x[0]
    # vt             鱼雷静水速度        x[1]
    # qm             敌舷角              x[2]
    # ds             射距                x[3]
    # lam            水平半扇面角λ       x[4]
    # Di             自导接收指向性指数      x[5]
    # Dt             检测阈                  x[6]
    # h              鱼雷航深(m)             x[7]
    # f              鱼雷声呐声波频率(kHz)   x[8]
    # var.append(['目标速度', 'vm', '无量纲'])
    var.append(['鱼雷静水速度', 'vt', '无量纲'])
    var.append(['敌舷角', 'qm', '无量纲'])
    var.append(['射距', 'ds', '无量纲'])
    var.append(['水平半扇面角λ', 'lam', '无量纲'])
    var.append(['自导接收指向性指数', 'Di', '无量纲'])
    var.append(['检测阈', 'Dt', '无量纲'])
    var.append(['鱼雷航深', 'h', '无量纲'])
    var.append(['鱼雷声呐声波频率', 'f', '无量纲'])

    # model4_torpedoTrack
    var.append(['鱼雷追踪过程中自导装置与目标保持可靠声接触的概率', 'pat', '0.95-1.0'])
    var.append(['鱼雷总（动力）航程', 'lT', '20.0'])
    var.append(['鱼雷回旋半径', 'rt', '0.1'])
    var.append(['再搜索在攻击能力系数', 'cr', '0.8-0.95'])
    var.append(['鱼雷固定提前角', 'fait', '20-80'])
    var.append(['目标速度', 'Vm', '50'])
    var.append(['鱼雷实际速度', 'Vt', '55'])
    var.append(['直航搜索段航程', 'lz', '16-17'])
    var.append(['鱼雷发现目标角', 'qa', '30-60'])
    var.append(['鱼雷自导作用距离', 'r', '1.5-3'])
    return var

def formula():
    var = []
    var.append(['声速不同导致目标方位探测精度公式1', 'Vs*sin(B0-B)=V0*sin(C0-B0)'])
    var.append(['声速不同导致目标方位探测精度公式2', 'Vs*sin(pi-c0-B)=D0*sin(C0-B0)'])
    var.append(['速度合成模型', 'V=sqrt(v1**2+v2**2+2*V1**2*v2**2*cos(theata))'])
    var.append(['方向影响模型', 'C=arctan(V1*sin(theata)/(V2+V1*cos(theata)))'])
    var.append(['X方向位置坐标影响模型', 'Xi=X(i-1)+V*(ti-t(i-1))*cos(Ct)'])
    var.append(['Y方向位置坐标影响模型', 'Yi=Y(i-1)+V*(ti-t(i-1))*sin(Ct)'])
    var.append(['声呐捕获半径模型', 'TL=20*log(r)+B*r*10**(-3)'])
    var.append(['影响模型提取公式1', 'y1=sqrt(x1**2+k1*x1*cos(x2)+k2)'])
    var.append(['影响模型提取公式2', 'y2=k3*arctan(x1*sin(x2)/(k4+x1*cos(x2)))'])
    var.append(['影响模型提取公式3', 'y3=y2+k5'])
    var.append(['x轴位置上的投影', 'Xi=X(i-1)+y1*t*cos(y3)'])
    var.append(['y轴位置上的投影', 'Yi=X(i-1)+y1*t*sin(y3)'])
    var.append(['被动声呐方程', 'SL-TL=NL-DI+DT'])
    var.append(['噪声掩盖下的主动声呐方程', 'SL-2TL+TS=NL-DI+DT'])
    var.append(['水面舰艇的辐射噪声', 'Pc=56*Vm**3*T**0.45/fr'])
    var.append(['辐射噪声谱级', 'SL=60*log(Vm)+9*log(T)-20*log(f)+35.8'])
    var.append(['潜艇的辐射噪声(Vm<=12)', 'SL=25*log(Vm)+77'])
    var.append(['潜艇的辐射噪声(Vm>=12)', '104+1.5*(Vm-12)'])
    var.append(['传播损失', 'TL=20*log(r)+B*r*10**(-3)'])
    var.append(['数吸声系数估算公式', 'B=2pi*T*S*f/(fp/f+f/fp)*10**-5+K*f**2'])
    var.append(['目标反射强度', 'TS = 10*lg(sigma/4*pi)'])
    var.append(['目标的声反射能力', 'Va=4*pi/S*10**(TS/10)'])
    var.append(['潜艇目标强度的近似模型', 'Va=1.1+2.1*a**3.8+3.35*a*sin(3.94*sqrt(a))'])
    var.append(['鱼雷干扰噪声级', 'NL=20*lg(PN)'])
    var.append(['鱼雷航行自噪声声压', 'Pn=A*exp(B*Ht)+C'])
    var.append(['水文环境对声音传播损失的影响', 'k1-k2=y-k3+k4'])
    var.append(['声音传播损失', 'y=20*log(r)+y1*r*10**(-3)'])
    var.append(['声对数吸收系数模型', 'y1=k5*x1*x2+k6'])
    return var

# return perhaps:a number
def function1_targetDetect(x, a):
    t=x[0]
    n=a[0]
    r=a[1]
    d=a[2]
    p=a[3]
    v=a[4]

    if(x[0]==0.0 and a[0]==0.0 and a[1]==0.0 and a[2]==0.0 and a[3]==0.0):
        presult = solve()
    else:
        presult=solve(n, r, d, v, p, t)

    return presult,

# return distance D0,speed Vm,way Hm:three numbers
def function2_MotionElement(x, a):

    if(x[0]==0 and x[1]==0 and x[2]==0 and x[3]==0 and x[4]==0 and x[5]==0 and x[6]==0 and x[7]==0 and x[8]==0):
        x[0] = 0.083
        x[1] = 0.872
        x[2] = 4
        x[3] = 1.046
        x[4] = 5
        x[5] = 0
        x[6] = 20
        x[7] = 40
        x[8] = 50


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

# return torpedoDetect:a number
def function3_TorpedoDetect(x, a):
    if(x[1]==0 and x[2]==0 and x[3]==0 and x[4]==0 and x[5]==0 and x[6]==0 and x[7]==0 and x[8]==0 and a[0]==0 and a[1]==0 and a[2]==0 and a[3]==0 and a[4]==0  and a[5]==0  and a[6]==0):
        a[0] = 3
        a[1] = 1/360*2*np.pi
        a[2] = 5
        a[3] = 280
        a[4] = 30/100
        a[5] = 0
        a[6] = 0
        x[0] = 15
        x[1] = 30
        x[2] = np.pi/3
        x[3] = 500
        x[4] = np.pi/6
        x[5] = 150
        x[6] = 80
        x[7] = 2000
        x[8] = 10
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



# return torpedoTrack:a number
def function4_torpedoTrack(x, a):

    pat = x[0]
    lT = x[1]
    rt = x[2]
    cr = x[3]
    fait = x[4]
    m = x[5]
    lz = x[6]
    qa = x[7]
    r = x[8]

    if(x[0]==0 and x[1]==0 and x[2]==0 and x[3]==0 and x[4]==0 and x[6]==0 and x[7]==0 and x[8]==0):
        result = fun4_solve()
    else:
        result = fun4_solve(pat,lT,rt,cr,fait,m,lz,qa,r)
    
    return result, #返回一次仿真鱼雷击中目标概率

def fun4_solve(pat = 0.95,lT = 20.0,rt = 0.1,cr = 0.8,fait = 20,m = 50,lz = 16,qa = 30,r = 1.5):
    result = 0 #鱼雷能否追踪到目标的结果
    lr = 2 * math.pi * rt / (1-m)  #计算再搜索再攻击航程lr
    x = (4*m) / ((4*m**2)-1) * (((2*m-1)/(((4*m**2)-1)**(1/2)))**(1/m))
    qa = qa / 180 * math.pi #角度转化（发现目标角）
    fait = fait / 180 * math.pi 
    lt = r * (1 - m*math.cos(qa-fait)) / ((1 - m**2)*math.cos(fait)) #计算追踪航程lt
    C = r * pow(math.fabs(math.tan(qa/2)), 1/m) * math.sin(qa)
    #rmin = C * x #计算最小弹道曲率半径rmin

    #对鱼雷再搜索在攻击能力进行处理
    ran = random.random()
    if ran < cr:
        cr = 1
    else:
        cr = 0

    #对鱼雷在总动力航程中追击目标进行评估
    if lT - lz >= lt:
        result = 1
    elif lT - lz - lt >= lr:
        result = cr
    else:
        result = 0


    #对鱼雷追踪过程中自导装置与目标保持声接触概率进行处理
    ran = random.random()
    if ran < pat:
        pat = 1
    else:
        pat = 0
    
    result = result * pat + (1-pat) * cr
    
    return result, #返回一次仿真鱼雷击中目标概率
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


#单个区域计算概率
def fi(x, t, v, s, p,):

    return 1 - np.exp(-v * t * x * p * t / s)

#方便记录区域边界
class Pair:
    pass


def solve(n=5, r=8/KN, d=11/KN, v=15, p=0.7, t=6):
    m = 2 * n - 1  # 区域个数
    W = 2 * r
    lenEnd = d
    lenOdd = 2 * r - d
    lenEven = 2 * (d - r)
    LD = 2 * r + (n - 1) * lenEnd
    tmax = float(W) / v
    # 每个区域的面积
    slenEnd = 2 * integrate.quad(
        lambda x, r: (r**2 - (x - r)**2)**0.5, 0, lenEnd, args=(r))[0]
    slenOdd = 2 * (np.pi * r**2 - slenEnd) - 4 * integrate.quad(
        lambda x, r: (r**2 - (x - r)**2)**0.5, r + d / 2, 2 * r, args=(r))[0]
    slenEven = 2 * integrate.quad(
        lambda x, r: (r**2 - (x - r)**2)**0.5,
        lenOdd,
        2 * r - lenOdd,
        args=(r))[0]

    def pf1(x): return p/r*x

    def pf0(x): return -p/r*x

    area = []
    sarea = []
    parea = []
    for i in range(int(m)):
        pair = Pair()
        if i == 0:
            pair.a = 0
            pair.b = pair.a + lenEnd
            sarea.append(slenEnd)

            def pf(x, pair): return pf1(x) if x <= r else pf0(x-2*r)
            parea.append(pf)
        elif i == m - 1:
            pair.b = 2 * r + (n - 1) * lenEnd
            pair.a = pair.b - lenEnd
            sarea.append(slenEnd)

            def pf(x, pair): return pf1(
                x-(n-1)*lenEnd) if x <= (pair.b-r) else pf0(x-pair.b)
            parea.append(pf)
        elif i == 2:
            pair.a = 2 * r
            pair.b = pair.a + lenEven
            sarea.append(slenEven)

            def pf(x, pair): return pf1(x-d) if x <= lenEnd + \
                r else pf0(x-(2*r+lenEnd))
            parea.append(pf)
        elif i == 1:
            pair.a = lenEnd
            pair.b = pair.a + lenOdd
            sarea.append(slenOdd)

            def pf(x, pair): return pf1(x-lenEnd)+pf0(x-2*r)
            parea.append(pf)
        elif i % 2 == 0:
            pair.a = area[i - 2].a + lenEven + lenOdd
            pair.b = pair.a + lenEven
            sarea.append(slenEven)

            def pf(x, pair): return pf1(
                x-pair.a+lenOdd) if x <= (pair.a+pair.b)/2 else pf0(x-pair.b-lenOdd)
            parea.append(pf)
        else:
            pair.a = area[i - 2].a + lenEven + lenOdd
            pair.b = pair.a + lenOdd
            sarea.append(slenOdd)
            tempf = parea[i-2]

            def pf(x, pair): return pf1(x-pair.a)+pf0(x-pair.b)
            parea.append(pf)
        area.append(pair)

    pmax = 0
    presult=0

    result = []
    for i in range(int(m)):
        s = sarea[i]  # 这里的面积是圆形面积
        pf = parea[i]  # 第i个区域对应的潜标搜索概率
        pair = area[i]  # 第i个区域的坐标
        if t<tmax:
            tmp = integrate.quad(
            lambda x, t, v, s, pair: 1 - np.exp(-v * t * x * pf(x, pair) * t / s), pair.a, pair.b, args=(t, v, s, pair))[0]
        else :
             tmp = integrate.quad(
            lambda x, t, v, s, pair: 1 - np.exp(-v * t * x * pf(x, pair) * t / s), pair.a, pair.b, args=(tmax, v, s, pair))[0]
        result.append(tmp)
    presult = np.sum(result) / LD

    return presult
