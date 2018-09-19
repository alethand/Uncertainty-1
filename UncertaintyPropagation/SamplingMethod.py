# -*- coding:utf-8 -*-
import numpy as np

import LHS
import MenteCarloMethod

# 分布名称转对应的编号
kind_dict = {'normal': 1,
             'uniform': 2,
             'exponential': 3,
             'other': 0
             }

# 分布对应的可用抽样方法
available_method = {'normal': ('random', 'MC'),
                    'uniform': ('random', 'LHS'),
                    'exponential': ('random', 'MC'),
                    'other': ('MC',)
                    }


# 抽样方法抽象类
class SamplingMethod(object):
    normal = 1
    uniform = 2
    exponential = 3
    other = 0

    def get_sampling(self, size, type, *parm):
        pass


# 随机抽样方法子类
class RandomSampling(SamplingMethod):
    def get_sampling(self, size, type, *parm):
        if type == self.normal:
            return np.random.normal(parm[0], parm[1], size)
        elif type == self.uniform:
            return np.random.uniform(parm[0], parm[1], size)
        elif type == self.exponential:
            # 指数分布中的参数为 theta 而不是 lambda
            return np.random.exponential(parm[0], size)


# 拉丁超立方抽样方法子类
class LHSampling(SamplingMethod):
    def get_sampling(self, size, type, *parm):
        if type == self.uniform:
            return LHS.getSample(parm[0], parm[1], size)


# 基于 Monte Carlo 方法的任意概率密度抽样方法子类
class MonteCarloSampling(SamplingMethod):
    def get_sampling(self, size, type, *parm):
        if type == self.other:
            # print parm[0]
            return MenteCarloMethod.getSample(parm[0], parm[1], parm[2], size)
        elif type == self.normal:
            expression = '1.0/(np.sqrt(2.0*np.pi*' + str(parm[1]) + '))*np.e**(-(x-' \
                   + str(parm[0]) + ')**2.0/(2.0*' + str(parm[1]) + '))'
            # print expression
            # 利用3σ准则确定上下界
            return MenteCarloMethod.getSample(expression, parm[0]-3*parm[1], parm[0]+3*parm[1], size)
        elif type == self.exponential:
            expression = '1.0/' + str(parm[0]) + '*np.e**(-1.0*x/' + str(parm[0]) + ')'
            # print expression
            # x落入(0, 5θ)的概率为1-e**(-5) (0.9933)
            return MenteCarloMethod.getSample(expression, 0, 5*parm[0], size)

# 具体策略类
class Context(object):

    def __init__(self, csuper):
        self.csuper = csuper

    def GetResult(self, size, type, *parm):
        return self.csuper.get_sampling(size, type, *parm)

strategy = {}
strategy['random'] = Context(RandomSampling())
strategy['LHS'] = Context(LHSampling())
strategy['MC'] = Context(MonteCarloSampling())

'''
if __name__ == '__main__':
    choose = 1

    oursql.clear_sampling_result()
    while choose != 0:
        choose = input("1.正态分布的随机抽样\n2.均匀分布的LHS抽样\n3.指数分布的随机抽样\n4.均匀分布的随机抽样\n(再次选择请关掉弹出的窗口)退出请按0:\n")

        # test RS for normal
        if choose == 1:
            mu, sigma = 0, 0.1  # mean and standard deviation
            type = SamplingMethod.normal
            size = 20
            s = strategy[1].GetResult(size, type, mu, sigma)
            oursql.insert_sampling_result(s)
            count, bins, ignored = plt.hist(s, 30, normed=True)
            plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)),linewidth = 2, color = 'r')
            plt.show()

        # test LHS for uniform
        if choose == 2:
            D = 2
            size = 30
            bounds = [[0, 90], [0, 90]]
            xs = (bounds[0][1] - bounds[0][0]) / size
            ys = (bounds[1][1] - bounds[1][0]) / size
            ax = plt.gca()
            plt.ylim(bounds[1][0] - ys, bounds[1][1] + ys)
            plt.xlim(bounds[0][0] - xs, bounds[0][1] + xs)
            plt.grid()
            ax.xaxis.set_major_locator(MultipleLocator(xs))
            ax.yaxis.set_major_locator(MultipleLocator(ys))
            type2 = SamplingMethod.uniform
            samples = strategy[2].GetResult(size, type2, D, bounds)
            oursql.insert_sampling_result(samples)
            XY = np.array(samples)
            X = XY[:, 0]
            Y = XY[:, 1]
            plt.scatter(X, Y)
            plt.show()

        # test RS for Exponential
        if choose == 3:
            theta = 2.0
            lamb = 1.0 / theta
            type = SamplingMethod.exponential
            size = 20
            s = strategy[1].GetResult(size, type, theta)
            oursql.insert_sampling_result(s)
            count, bins, ignored = plt.hist(s, 30, normed=True)
            plt.plot(bins, lamb * np.exp(-bins * lamb), linewidth=2, color='r')
            plt.show()
'''