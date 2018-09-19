# coding=utf-8
# from http://www.doc88.com/p-215945997508.html

import numpy as np

# 计算概率密度函数最大值时的分割数
# 在给定区间内等距离取cfeji个数计算概率密度函数的最大值
cfeji = 1000


def interpret(expression, x):
    y = eval(expression)
    return y


# 计算概率密度函数在给定区间内的最大值
def get_probability_density_function_max(expression, x_low, x_high):
    if x_low >= x_high:
        return -1
    interval = (x_high - x_low)/cfeji
    max_ = -1.0
    for i in range(cfeji):
        temp = interpret(expression, x_low)
        if max_ < temp:
            max_ = temp
        x_low += interval
    return max_


# :param x_low: 样本的下界
# :param x_high: 样本的上界
# :param expression: 样本的概率密度函数
# :param size: 样本大小
# :return: 样本数据
def getSample(expression, x_low, x_high, size):
    # 求样本概率密度函数在[x_low, x_high]上的最大值
    y_max = get_probability_density_function_max(expression, x_low, x_high)
    result = np.empty([size])
    if y_max < 0:
        return result
    while size > 0:
        temp1 = np.random.uniform(x_low, x_high, 1)
        temp2 = np.random.uniform(0, y_max, 1)
        if temp2 < interpret(expression, temp1):
            result[size-1] = temp1
            size -= 1
    return result

'''
if __name__ == '__main__':
    expr = '1.0/(np.sqrt(2.0*np.pi*1.0))*np.e**(-(x-0.0)**2.0/(2.0*1.0))'
    low = -3.0
    high = 3.0
    size = 20
    s = getSample(expr, low, high, size)
    print s
'''