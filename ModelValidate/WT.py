# -*- coding: utf-8 -*-
# movieRatings = [
#     [2, 5, 3, 2, 7, 8, 9, 1],
#     [1, 2, 1, 2, 4, 5, 1, 12],
#     [4, 1, 1, 9, 1, 12, 2, 7],
#     [3, 5, 2, 4, 1, 4, 5, 5],
#     [5, 3, 1, 7, 7, 9, 1, 4],
#     [4, 5, 5, 9, 1, 3, 3, 6],
#     [2, 4, 2, 8, 4, 3, 2, 8],
#     [2, 2, 5, 4, 6, 8, 1, 7],
# ]

import matplotlib.pyplot as plt
import numpy as np
import pywt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

movieRatings = [2, 5, 3, 2, 7, 8, 9, 1]
data = movieRatings
t = [1, 2, 3, 4, 5, 6, 7, 8]
t1 = [1, 2, 3, 4, 5]

# chinese_font = FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
# sampling_rate = 1024
# t = np.arange(0, 1.0, 1.0 / sampling_rate)
# f1 = 100
# f2 = 200
# f3 = 300
# data = np.piecewise(t, [t < 1, t < 0.8, t < 0.3],
#                     [lambda t: np.sin(2 * np.pi * f1 * t), lambda t: np.sin(2 * np.pi * f2 * t),
#                      lambda t: np.sin(2 * np.pi * f3 * t)])
# wavename = 'cgau8'
# totalscal = 256
# fc = pywt.central_frequency(wavename)
# cparam = 2 * fc * totalscal
# scales = cparam / np.arange(totalscal, 1, -1)
# [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)
[cwtmatr, frequencies] = pywt.dwt(data, 'db2',mode = 'sym')
w = pywt.Wavelet('db2')
print(pywt.dwt_coeff_len(data_len=len(data), filter_len=w.dec_len, mode='sym'))
# [cwtmatr, frequencies] = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
plt.figure(figsize=(8, 4))
plt.subplot(211)
plt.plot(t, data)
plt.xlabel(u"时间(秒)")
plt.title(u"时频谱", fontsize=20)
plt.subplot(212)
plt.plot(t1,cwtmatr)
plt.plot(t1,frequencies)
# plt.contourf(t, frequencies, abs(cwtmatr))
plt.ylabel(u"频率(Hz)")
plt.xlabel(u"时间(秒)")
plt.subplots_adjust(hspace=0.4)
plt.show()