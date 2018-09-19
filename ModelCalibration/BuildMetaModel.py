# -*- coding: utf-8 -*-
import numpy
import sys
from wx.lib.mixins.listctrl import TextEditMixin

import RealModel as rm
import RealModel_NEW as rm_new
import DoubleLoop
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.kernel_ridge import KernelRidge as KRR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic, DotProduct,ConstantKernel)
import GetSample as gs
import wx
import CalibrationPanel as cp
import Sql

real_cog_p_r = 0
cog_p_all = 0
cog_p = 0
inh_p = 0
input_v = 0
input_v1 = 0
input_v2 = 0
output1 = 0
output2 = 0

# choice = 0时显示表 否则只导入数据
def importData(snb, n_id, choice = 0):
    global real_cog_p_r
    global cog_p_all
    global cog_p
    global inh_p
    global input_v
    global input_v1
    global input_v2
    global output1
    global output2

    #real_cog_p_r = snb.real_cog_p_r

    cog_p_all = gs.get_samp(nid = n_id, arg_type=2)   # 根据你选择的模型导入相应的数据
    inh_p = gs.get_samp(nid = n_id, arg_type=1)
    input_v = gs.get_samp(nid = n_id, arg_type=0)

    cog_p = cog_p_all[0:200, :]

    shape = input_v.shape
    d1 = shape[0]/3
    input_v1 = input_v[0:d1*2, :]
    input_v2 = input_v[d1*2:, :]

    output1 = rm_new.run_real_model(inh_p, input_v1)
    output2 = rm_new.run_real_model(inh_p, input_v2)

    # show_log = ''
    #
    # show_log = show_log + str(cog_p_all.shape) + '\n'
    # show_log = show_log + '认知不确定参数' + '\n'
    # show_log = show_log + str(cog_p.shape) + '\n'
    # show_log = show_log + '%r'%(cog_p) + '\n'
    # show_log = show_log + '固有不确定参数:' + '\n'
    # show_log = show_log + str(inh_p.shape) + '\n'
    # show_log = show_log + '%r'%(inh_p) + '\n'
    # show_log = show_log + '计算一致性度量输入:' + '\n'
    # show_log = show_log + str(input_v1.shape) + '\n'
    # show_log = show_log + '%r'%(input_v1) + '\n'
    # show_log = show_log + '对比验证输入:' + '\n'
    # show_log = show_log + str(input_v2.shape) + '\n'
    # show_log = show_log + '%r'%(input_v2) + '\n'
    # show_log = show_log + '计算一致性度量输出:' + '\n'
    # show_log = show_log + str(output1.shape) + '\n'
    # show_log = show_log + '%r'%(output1) + '\n'
    # show_log = show_log + '对比验证输出:' + '\n'
    # show_log = show_log + str(output2.shape) + '\n'
    # show_log = show_log + '%r'%(output2) + '\n'
    if(choice == 0):

        show_panel = snb.show_panel

        Cal_grid = snb.Cal_Grid

        draw_grid(inh_p,input_v2, output2,  input_v1 ,output1, Cal_grid)


    # shape_cog_r, shape_cog_c = cog_p.shape
    # grid1.CreateGrid(shape_cog_r, shape_cog_c)
    # for i in range(shape_cog_r):
    #     grid1.SetRowLabelValue(i, '%dth抽样'%(i+1))
    #     for j in range(shape_cog_c):
    #         if i==0:
    #             grid1.SetColLabelValue(j, '认知参数_%d'%(j+1))
    #             grid1.SetColSize(j, -1)
    #         grid1.SetCellValue(i, j, str(round(cog_p[i, j], 3)))
    #
    # shape_inh_r, shape_inh_c = inh_p.shape
    # grid2.CreateGrid(shape_inh_r, shape_inh_c)
    # for i in range(shape_inh_r):
    #     grid2.SetRowLabelValue(i, '%dth抽样'%(i+1))
    #     for j in range(shape_inh_c):
    #         if i==0:
    #             grid2.SetColLabelValue(j, '固有参数_%d'%(j+1))
    #             grid2.SetColSize(j, -1)
    #         grid2.SetCellValue(i, j, str(round(inh_p[i, j], 3)))
    #
    # shape_inp1_r, shape_inp1_c = input_v1.shape
    # grid3.CreateGrid(shape_inp1_r, shape_inp1_c)
    # for i in range(shape_inp1_r):
    #     grid3.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(shape_inp1_c):
    #         if i == 0:
    #             grid3.SetColLabelValue(j, '计算输入_%d' % (j + 1))
    #             grid3.SetColSize(j, -1)
    #         grid3.SetCellValue(i, j, str(round(input_v1[i, j], 3)))
    #
    # shape_inp2_r, shape_inp2_c = input_v2.shape
    # grid4.CreateGrid(shape_inp2_r, shape_inp2_c)
    # for i in range(shape_inp2_r):
    #     grid4.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(shape_inp2_c):
    #         if i == 0:
    #             grid4.SetColLabelValue(j, '比较输入_%d' % (j + 1))
    #             grid4.SetColSize(j, -1)
    #         grid4.SetCellValue(i, j, str(round(input_v2[i, j], 3)))
    #
    # shape_out1_r, shape_out1_c = output1.shape
    # grid5.CreateGrid(shape_out1_r, shape_out1_c)
    # for i in range(shape_out1_r):
    #     grid5.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(shape_out1_c):
    #         if i == 0:
    #             grid5.SetColLabelValue(j, '计算输出_%d' % (j + 1))
    #             grid5.SetColSize(j, -1)
    #         grid5.SetCellValue(i, j, str(round(output1[i, j], 3)))
    #
    # shape_out2_r, shape_out2_c = output2.shape
    # grid6.CreateGrid(shape_out2_r, shape_out2_c)
    # for i in range(shape_out2_r):
    #     grid6.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(shape_out2_c):
    #         if i == 0:
    #             grid6.SetColLabelValue(j, '对比输出_%d' % (j + 1))
    #             grid6.SetColSize(j, -1)
    #         grid6.SetCellValue(i, j, str(round(output2[i, j], 3)))

        show_panel.SetupScrolling()
        show_panel.Layout()

    cp.sym1 = 1
    # dlg = wx.MessageDialog(None, '数据导入已经完成', u' ')
    # dlg.ShowModal()

def importDataSource( n_id):
    print n_id
    global real_cog_p_r
    global cog_p_all
    global cog_p
    global inh_p
    global input_v
    global input_v1
    global input_v2
    global output1
    global output2

    #real_cog_p_r = snb.real_cog_p_r

    cog_p_all = gs.get_samp(nid = n_id, arg_type=2)   # 根据你选择的模型导入相应的数据
    inh_p = gs.get_samp(nid = n_id, arg_type=1)
    input_v = gs.get_samp(nid = n_id, arg_type=0)

    cog_p = cog_p_all[0:200, :]

    shape = input_v.shape
    d1 = shape[0]/3
    input_v1 = input_v[0:d1*2, :]
    input_v2 = input_v[d1*2:, :]

    output1 = rm_new.run_real_model(inh_p, input_v1)
    output2 = rm_new.run_real_model(inh_p, input_v2)

def buildSVR(snb, cog_p, inh_p, output1, input_v1, n_id):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                         'gamma': ['auto', 0.1, 0.001, 0.0001],
                         'C': [1, 10, 100, 1000],
                         'epsilon': [0.1, 0.001, 1],
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
    showlog = ''
    showlog = showlog + '建立超参数搜索模型' + '\n'
    clf = GridSearchCV(svm.SVR(), tuned_parameters)

    showlog = showlog + '开始搜索' + '\n'
    clf.fit(X_train, y_train)
    showlog = showlog + '搜索结束' + '\n'

    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
    #print '在参数集上搜索得到的最佳参数组合为'
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
    #print clf.best_params_
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        showlog = showlog + "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params) + '\n'

    """改"""
    #show_panel = snb.show_panel
    show_panel = snb.scrolledWindow

    grid = snb.grid_out
    grid.CreateGrid(1, len(y_v))
    grid.SetRowLabelValue(0, '一致性')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(y_v)):
        grid.SetColLabelValue(i, '%d'%(i+1))
        grid.SetCellValue(0, i, str(round(y_v[i], 3)))

    # csw = snb.sw
    # csw.text_ctrl.SetValue(showlog)

    best_p = rm_new.cog_p_r
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)

    #保存元模型到数据库
    Sql.insert_metamodel(n_id, "svr", clf)

    axes = snb.axes
    canvas = snb.canvas
    lpred, = axes.plot(y_pred, 'r', label='predict value')
    ltest, = axes.plot(y_test, 'g', label='real value')
    axes.plot(best_pred, 'b.')
    axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    #show_panel.SetupScrolling()
    show_panel.Layout()

    cp.sym2 = 1
    # dlg = wx.MessageDialog(None, message='元模型建模已经完成')
    # dlg.ShowModal()


    # plt.plot(y_pred, 'r')
    # plt.plot(y_test, 'g')
    # plt.plot(best_pred, 'b.')
    # plt.title('Prediction accuracy diagram')
    # plt.show()
    return clf

def buildGPR(snb, cog_p, inh_p, output1, input_v1, n_id):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': [1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)),
                                    1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1),
                                    ConstantKernel(0.1, (0.01, 10.0))
                                    * (DotProduct(sigma_0=1.0, sigma_0_bounds=(0.0, 10.0)) ** 2),
                                    1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0), nu=1.5)],
                         'alpha': [1E-10, 0.1, 1]
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
    showlog = ''
    showlog = showlog + '建立超参数搜索模型' + '\n'
    clf = GridSearchCV(GPR(), tuned_parameters)

    showlog = showlog + '开始搜索' + '\n'
    clf.fit(X_train, y_train)
    showlog = showlog + '搜索结束' + '\n'

    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
    #print '在参数集上搜索得到的最佳参数组合为'
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
    #print clf.best_params_
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        showlog = showlog + "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params) + '\n'

    show_panel = snb.scrolledWindow
    grid = snb.grid_out
    grid.CreateGrid(1, len(y_v))
    grid.SetRowLabelValue(0, '一致性')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(y_v)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(y_v[i], 3)))

    # csw = snb.sw
    # csw.text_ctrl.SetValue(showlog)

    best_p = rm_new.cog_p_r
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)

    #保存到数据库
    Sql.insert_metamodel(n_id, "gpr", clf)

    axes = snb.axes
    canvas = snb.canvas
    lpred, = axes.plot(y_pred, 'r', label='predict value')
    ltest, = axes.plot(y_test, 'g', label='real value')
    axes.plot(best_pred, 'b.')
    axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
#    show_panel.SetupScrolling()
    show_panel.Layout()

    cp.sym2 = 1
    dlg = wx.MessageDialog(None, message='元模型建模已经完成')
    dlg.ShowModal()
    # plt.plot(y_pred, 'r')
    # plt.plot(y_test, 'g')
    # plt.plot(best_pred, 'b.')
    # plt.title('Prediction accuracy diagram')
    # plt.show()
    return clf

def buildKRR(snb, cog_p, inh_p, output1, input_v1, n_id):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': ['linear', 'rbf', 'laplacian', 'sigmoid'],
                         'alpha': [1, 0.0001, 0.00001, 1E-6, 1E-7, 1E-8, 0],
                         "gamma": numpy.logspace(-2, 2, 5)
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
    showlog = ''
    showlog = showlog + '建立超参数搜索模型' + '\n'
    clf = GridSearchCV(KRR(), tuned_parameters)

    showlog = showlog + '开始搜索' + '\n'
    clf.fit(X_train, y_train)
    showlog = showlog + '搜索结束' + '\n'

    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
   # print '在参数集上搜索得到的最佳参数组合为'
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
   # print clf.best_params_
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        showlog = showlog + "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params) + '\n'

    show_panel = snb.scrolledWindow
    grid = snb.grid_out
    grid.CreateGrid(1, len(y_v))
    grid.SetRowLabelValue(0, '一致性')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(y_v)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(y_v[i], 3)))

    # csw = snb.sw
    # csw.text_ctrl.SetValue(showlog)

    best_p = rm_new.cog_p_r
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)

    # 保存到数据库
    Sql.insert_metamodel(n_id, "bayes", clf)

    axes = snb.axes
    canvas = snb.canvas
    lpred, = axes.plot(y_pred, 'r', label='predict value')
    ltest, = axes.plot(y_test, 'g', label='real value')
    axes.plot(best_pred, 'b.')
    axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    #show_panel.SetupScrolling()
    show_panel.Layout()

    cp.sym2 = 1
    dlg = wx.MessageDialog(None, message='元模型建模已经完成')
    dlg.ShowModal()
    # plt.plot(y_pred, 'r')
    # plt.plot(y_test, 'g')
    # plt.plot(best_pred, 'b.')
    # plt.title('Prediction accuracy diagram')
    # plt.show()
    return clf

def draw_grid(inh_p, input2, output2, input,output,cal_grid):
    # Grid
    rowinh, cloumninh = inh_p.shape

    row1, cloumn1 = output.shape
    rowi, cloumni = input.shape

    row2, cloumn2 = output2.shape
    rowi2, cloumni2 = input2.shape

    cloumn = cloumn1 + cloumni + cloumninh + 1
    #    cloumn2 = cloumn2 + cloumni2

    row = row2 + row1

    cal_grid.CreateGrid(28, 12)
    cal_grid.EnableEditing(True)
    cal_grid.EnableGridLines(True)
    cal_grid.EnableDragGridSize(False)
    cal_grid.SetMargins(0, 0)

    # Columns
    cal_grid.EnableDragColMove(False)
    cal_grid.EnableDragColSize(True)
    cal_grid.SetColLabelSize(30)
    cal_grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    for i in range(cloumn ):
        if (i < cloumninh ):
            cal_grid.SetColLabelValue(i, u"固有参数_%d" % (i+1))
        else:
            if (i < cloumninh + cloumni ):
                cal_grid.SetColLabelValue(i, u"输入_%d" % (i - cloumninh + 1))
            else:
                if (i == cloumn):
                    cal_grid.SetColLabelValue(i, u"输入输出类型")
                else:
                    cal_grid.SetColLabelValue(i, u"输出_%d" % (i - cloumninh - cloumni + 1))

    # Rows
    cal_grid.EnableDragRowSize(True)
    cal_grid.SetRowLabelSize(80)
    cal_grid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

    # Label Appearance

    # Cell Defaults
    cal_grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

    """"设置内容"""
    i = 0

    for i in range(cloumn):
        if (i < cloumninh):
            for j in range(row):
                # 截段输出 numpy 抽样结果过长
                cal_grid.SetCellValue(j, i, str(round(inh_p[j, i - 1], 3)))
        else:
            if (i < cloumninh + cloumni):
                for j in range(row):
                    # 截段输出 numpy 抽样结果过长
                    if (j < row1):
                        cal_grid.SetCellValue(j, i, str(round(input[j, i - cloumninh], 3)))
                    else:
                        cal_grid.SetCellValue(j, i, str(round(input2[j - row1, i - cloumninh ], 3)))
            else:
                for j in range(row):
                    # 截段输出 numpy 抽样结果过长
                    if (j < row1):
                        cal_grid.SetCellValue(j, i, str(round(output[j, i - cloumninh - cloumni - 1], 3)))
                        if (i == cloumn):
                            cal_grid.SetCellValue(j, i, '计算一致性')
                    else:
                        if (i == cloumn):
                            cal_grid.SetCellValue(j, i, '对比验证')
                        else:
                            cal_grid.SetCellValue(j, i, str(round(output2[j - row1, i - cloumninh - cloumni - 1], 3)))


    # grid.CreateGrid(row, cloumn)
    # for i in range(row):
    #     grid.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(cloumn):
    #         if i == 0:
    #             grid.SetColLabelValue(j, )
    #             grid.SetColSize(j, -1)
    #         grid.SetCellValue(i, j, str(round(show[i, j], 3)))

# def draw_table(inh_p, input2, output2, input,output, form):
#
#     rowinh, cloumninh = inh_p.shape
#
#     row1, cloumn1 = output.shape
#     rowi,cloumni = input.shape
#
#     row2, cloumn2 = output2.shape
#     rowi2,cloumni2 = input2.shape
#
#     cloumn = cloumn1 + cloumni + cloumninh + 1
# #    cloumn2 = cloumn2 + cloumni2
#
#     row = row2 + row1
#     # grid.CreateGrid(row, cloumn)
#     # for i in range(row):
#     #     grid.SetRowLabelValue(i, '%dth抽样' % (i + 1))
#     #     for j in range(cloumn):
#     #         if i == 0:
#     #             grid.SetColLabelValue(j, )
#     #             grid.SetColSize(j, -1)
#     #         grid.SetCellValue(i, j, str(round(show[i, j], 3)))
#
#     for i in range(cloumn+1):
#         if(i == 0):
#             form.InsertColumn(i, "", width=160)
#         else:
#             if (i < cloumninh + 1):
#                 form.InsertColumn(i, '固有参数_%d' % (i), width=160)
#             else:
#                 if (i < cloumninh + cloumni+1):
#                     form.InsertColumn(i, '输入_%d' % (i - cloumninh), width=160)
#                 else:
#                     if(i == cloumn):
#                         form.InsertColumn(i, '输入输出类型' , width=160)
#                     else:
#                         form.InsertColumn(i, '输出_%d' % (i - cloumninh -cloumni), width=160)
#     # 初始化表格
#     for i in range(row):
#          index = form.InsertItem(sys.maxint, 0)
#          print(str(i)+":"+str(index))
#
#     # 设置内容
#     for i in range(cloumn+1):
#          if(i == 0):
#              for j in range(row):
#                  # 截段输出 numpy 抽样结果过长
#                  form.SetItem(j, i, str(j+1)+"th抽样")
#          else:
#              if (i < cloumninh + 1):
#                  for j in range(row):
#                      # 截段输出 numpy 抽样结果过长
#                     form.SetItem(j, i, str(round(inh_p[j, i-1], 3)))
#              else:
#                  if (i < cloumninh + cloumni + 1):
#                      for j in range(row):
#                          # 截段输出 numpy 抽样结果过长
#                          if (j < row1):
#                              form.SetItem(j, i, str(round(input[j, i - cloumninh - 1], 3)))
#                          else:
#                              form.SetItem(j, i, str(round(input2[j - row1, i - cloumninh -1], 3)))
#                  else:
#                      for j in range(row):
#                          # 截段输出 numpy 抽样结果过长
#                          if (j < row1):
#                              form.SetItem(j, i, str(round(output[j, i - cloumninh - cloumni - 2], 3)))
#                              if (i == cloumn):
#                                  form.SetItem(j, i, '计算一致性')
#                          else:
#                              if (i == cloumn):
#                                  form.SetItem(j, i, '对比验证')
#                              else:
#                                  form.SetItem(j, i, str(round(output2[j - row1, i -cloumninh - cloumni - 2], 3)))