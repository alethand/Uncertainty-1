# -*- coding: utf-8 -*-
import DoubleLoop
import numpy
import wx
import BuildMetaModel

avg_dif = list()
max_dif = list()
min_dif = list()
cmp_dif = list()
best_mat = 1
sym = 0
cross_num = 0
mut_num = 0

def Get_prol(cog_p, svr):
    shape_v = cog_p.shape
    population_num = shape_v[0]
    output_l = list()
    pro_l = list()
    sum_o = 0
    tot_dis = 0
    for i in range(population_num):
        cog_p_r = cog_p[i]
        output_t = svr.predict(cog_p_r)
        output_l.append(output_t[0])
        sum_o = sum_o + 1 / output_t[0]
        tot_dis = tot_dis + output_t[0]

    sum_p = 0
    max_p = 0
    min_p = 2
    max_p_index = 0
    min_p_index = 0

    for i in range(population_num):
        pro_temp = 1 / output_l[i] / sum_o
        if max_p < pro_temp:
            max_p = pro_temp
            max_p_index = i
        if min_p > pro_temp:
            min_p = pro_temp
            min_p_index = i
        sum_p = pro_temp + sum_p
        pro_l.append(sum_p)

    global sym
    global best_mat
    if sym == 0:
        sym=1
        best_mat = cog_p[max_p_index]
    else:
        best_mat = numpy.row_stack((best_mat, cog_p[max_p_index]))

    avg_dif.append(tot_dis / population_num)
    min_dif.append(output_l[max_p_index])
    max_dif.append(output_l[min_p_index])

    y_v = DoubleLoop.outer_level_loop(cog_p[max_p_index], BuildMetaModel.inh_p, BuildMetaModel.output2, BuildMetaModel.input_v2)
    cmp_dif.append(y_v[0])
    return pro_l

def Get_index(pro_l, len, r_v):  # 随机选取一个个体的下标  按照概率的大小
    i = 0
    for i in range(len):
        if pro_l[i] >= r_v:
            return i
    return i

def Cross_op(individual_1, individual_2):
    global cross_num
    cross_num = cross_num+1
    shape_v = individual_1.shape
    len = shape_v[1]
    cross_point = numpy.random.randint(1, len)
    ret_indi = individual_1
    for i in range(shape_v[1]):
        if i <= cross_point:
            ret_indi[0, i] = individual_1[0, i]
        else:
            ret_indi[0, i] = individual_2[0, i]
    return ret_indi

def Mut_op(indi):
    global mut_num
    mut_num = mut_num+1
    shape_v = indi.shape
    r_v = numpy.random.randint(1, shape_v[1])
    r_v_a = numpy.random.rand()
    if r_v_a >= 0.5:
        indi[0, r_v] = indi[0, r_v] + 1
    else:
        indi[0, r_v] = indi[0, r_v] - 1
    return indi

def New_pop(pro_l, cog_p, cross_p, mut_p):  # 产生新种群
    shape_v = cog_p.shape
    num_iter = shape_v[0]
    row_t = cog_p[Get_index(pro_l, num_iter, numpy.random.rand())]
    new_cog_p = row_t
    i = 1
    while i <= num_iter - 1:
        rand_c = numpy.random.rand()
        if rand_c >= 0 and rand_c < cross_p:  # 交叉成立
            r_1 = numpy.random.rand()
            r_2 = numpy.random.rand()
            index_1 = Get_index(pro_l, num_iter, r_1)
            index_2 = Get_index(pro_l, num_iter, r_2)
            while index_2 == index_1:
                r_2 = numpy.random.rand()
                index_2 = Get_index(pro_l, num_iter, r_2)
            individual_1 = cog_p[index_1]
            individual_2 = cog_p[index_2]
            new_indi = Cross_op(individual_1, individual_2)
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                new_indi = Mut_op(new_indi)
            new_cog_p = numpy.row_stack((new_cog_p, new_indi))
            i = i + 1
        else:
            r = numpy.random.rand()
            index = Get_index(pro_l, num_iter, r)
            new_indi = cog_p[index]
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                new_indi = Mut_op(new_indi)
            new_cog_p = numpy.row_stack((new_cog_p, new_indi))
            i = i + 1
    return new_cog_p

def GA(snb, meta_model, pn=100, itn=50, cp=0.3, mp=0.05):
    #show_panel = snb.show_panel
    #csw = snb.sw
    # log = ''
    global max_dif
    global min_dif
    global avg_dif
    global cmp_dif
    max_dif = list()
    min_dif = list()
    avg_dif = list()
    cmp_dif = list()
    population_num = pn  # 种群大小
    iter_num = itn  # 迭代次数
    cross_p = cp  # 交叉概率
    mut_p = mp  # 变异概率
    cog_p = BuildMetaModel.cog_p_all[:population_num, :]

    #log = log+'期望最佳预测'+'\n'
    #log = log + '%f'%(meta_model.predict([[4,1,8]])) + '\n'
    for i in range(iter_num):
        pro_l = Get_prol(cog_p, meta_model)
        cog_p = New_pop(pro_l, cog_p, cross_p, mut_p)
    print "++++++++++++++++++++++++++++++++++++++++"
    print min_dif
    print numpy.min(min_dif)
    minIndex = min_dif.index(numpy.min(min_dif))
    print minIndex
    print best_mat[minIndex]
    print "+++++++++++++++++++++++++++++++++++++++++"

    #log = log + '交叉次数: %d'%(cross_num) + '\n'
    #log = log + '变异次数: %d'%(mut_num) + '\n'

    # log = log + '%d次迭代优化中每次的最大差异度量为\n%r' % (iter_num, max_dif) + '\n'
    # log = log + '%d次迭代优化中每次的最小差异度量为\n%r' % (iter_num, min_dif) + '\n'
    # log = log + '%d次迭代优化中每次的平均差异度量为\n%r' % (iter_num, avg_dif) + '\n'
    # log = log + '%d次迭代优化中每次的比较差异度量为\n%r' % (iter_num, cmp_dif) + '\n'
    # log = log + '%d次迭代优化中每次的最佳参数取值为\n%r' % (iter_num, best_mat) + '\n'

    #csw.text_ctrl.SetValue(log)
    #show_panel.Layout()

    shape_1, shape_2 = cog_p.shape

    grid1 = snb.grid1
    grid2 = snb.grid2

    if iter_num > 17:
        grid1.CreateGrid(iter_num, 4)
    elif iter_num <= 17:
        grid1.CreateGrid(17, 4)

    if shape_2 > 4 and iter_num > 17:
        grid2.CreateGrid(iter_num, shape_2)
    elif shape_2 <= 4 and iter_num > 17:
        grid2.CreateGrid(iter_num, 4)
    elif shape_2 > 4 and iter_num <= 17:
        grid2.CreateGrid(17, shape_2)
    elif shape_2 <= 4 and iter_num <= 17:
        grid2.CreateGrid(17, 4)

    grid1.SetColLabelValue(0, '最大差异度量')
    grid1.SetColSize(0, 80)
    grid1.SetColLabelValue(1, '平均差异度量')
    grid1.SetColSize(1, 80)
    grid1.SetColLabelValue(2, '最小差异度量')
    grid1.SetColSize(2, 80)
    grid1.SetColLabelValue(3, '比较差异度量')
    grid1.SetColSize(3, 80)



    for i in range(iter_num):
        grid1.SetRowLabelValue(i, '第%d次迭代'%(i+1))
        for j in range(4):
            if j == 0:
                grid1.SetCellValue(i, j, str(round(max_dif[i],3)))
            elif j == 1:
                grid1.SetCellValue(i, j, str(round(avg_dif[i],3)))
            elif j==2:
                grid1.SetCellValue(i, j, str(round(min_dif[i],3)))
            else:
                grid1.SetCellValue(i, j, str(round(cmp_dif[i],3)))

    for i in range(shape_2):
        grid2.SetColLabelValue(i, '认知参数_%d'%(i))
        grid2.SetColSize(i, 80)
    if shape_2 < 4:
        for i in range(shape_2,4):
            grid2.SetColLabelValue(i,"")
    for i in range(iter_num):
        grid2.SetRowLabelValue(i, '第%d次迭代'%(i+1))
        for j in range(shape_2):
            grid2.SetCellValue(i, j, str(round(best_mat[i, j],3)))
    if iter_num < 18:
        for i in range(iter_num,18):
            grid1.SetRowLabelValue(i, "")
            grid2.SetRowLabelValue(i,"")


    show_panel = snb.scrolledWindow
    axes = snb.axes
    axes2 = snb.axes2
    canvas = snb.canvas
    canvas2 = snb.canvas2
    x = len(avg_dif)
    x = range(x)
    axes.clear()
    lavg, = axes.plot(x, avg_dif)
    lmax, = axes.plot(x, max_dif)
    lmin, = axes.plot(x, min_dif)
    axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
    axes.legend(handles=[lavg, lmax, lmin], labels=['average measurement', 'max measurement', 'min measurement'])
    lcmp, = axes2.plot(x, cmp_dif)
    axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
    axes2.legend(handles=[lcmp,], labels=['compare difference'])
    canvas.draw()
    canvas2.draw()
    show_panel.SetupScrolling()
    show_panel.Layout()

    # dlg = wx.MessageDialog(None, message='优化迭代已经完成')
    # dlg.ShowModal()

    # plt.figure(num=1, figsize=(6, 3))
    # x = len(avg_dif)
    # x= range(x)
    # plt.plot(x, avg_dif, 'r')
    # plt.plot(x, max_dif, 'g')
    # plt.plot(x, min_dif, 'b')
    # plt.xlabel('Number of iterations')
    # plt.ylabel('Difference measurement')
    # plt.title('Optimization of iterative trend diagram')
    # plt.figure(num=2, figsize=(6, 3))
    # plt.plot(x, cmp_dif)
    # plt.xlabel('Number of iterations')
    # plt.ylabel('Difference measurement')
    # plt.title('Verification trend diagram')
    # plt.show()