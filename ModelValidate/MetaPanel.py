# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
import wx.xrc
import wx.lib.newevent

import numpy as np

import commonTag
from ShowNotebook import *
import ValidateBuildMetaModel as  build_meta
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# 右侧主面板的内容
import data_related as dr
import ValidateUi as cp

import SVD as svdArg

class MetaPanel(wx.Panel):

    def __init__(self, parent,n_id):

        """ 初始化 """
        wx.Panel.__init__(self, parent, n_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self 的布局，有 show_panel 和input_panel两个元素
        self.meta_sizer = wx.BoxSizer(wx.VERTICAL)

        # 上部info_panel
        self.info_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)

        # info_panel 的布局，元素为显示的控件
        self.info_sizer = wx.GridBagSizer(5, 5)
        self.info_sizer.SetFlexibleDirection(wx.BOTH)
        self.info_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.info_panel.SetSizer(self.info_sizer)
        self.info_panel.gbSizer = self.info_sizer
        # 下方显示图像
        self.scrolledWindow = scrolled.ScrolledPanel(self, -1,
                                                     style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="scrolled")
        self.scrolledWindow.SetAutoLayout(1)
        self.scrolledWindow.SetupScrolling()
        self.show_panel = self.scrolledWindow

        # scrollPanel 的布局，元素为显示的控件
        self.show_sizer = wx.GridBagSizer(5, 5)
        self.show_sizer.SetFlexibleDirection(wx.BOTH)
        self.show_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.show_panel.SetSizer(self.show_sizer)

        # 上部input_Panel
        self.input_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                    (-1, 80), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1, 80))

        distance_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_radioBtn1 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"欧式距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn1.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        self.m_radioBtn1.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t1a)
        distance_sizer.Add(self.m_radioBtn1, 0, wx.ALL, 6)

        self.m_radioBtn2 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"马氏距离验证", wx.DefaultPosition, wx.DefaultSize,
                                          0)
        self.m_radioBtn2.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t2a)
        distance_sizer.Add(self.m_radioBtn2, 0, wx.ALL, 6)

        self.m_radioBtn3 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"切比雪夫距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn3.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t3a)
        distance_sizer.Add(self.m_radioBtn3, 0, wx.ALL, 6)

        self.m_radioBtn4 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"曼哈顿距离验证", wx.DefaultPosition, wx.DefaultSize,
                                          0)
        self.m_radioBtn4.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t4a)
        distance_sizer.Add(self.m_radioBtn4, 0, wx.ALL, 6)

        self.m_radioBtn5 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"KL散度验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn5.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t5a)
        distance_sizer.Add(self.m_radioBtn5, 0, wx.ALL, 6)

        self.input_panel.SetSizer(distance_sizer)

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.LI_HORIZONTAL)

        # 上方提示信息Panel
        commonTag.setModeltag(self.info_panel, n_id)

        # 提示信息
        self.static_text = wx.StaticText(self, wx.ID_ANY, u"验证方式：",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体"))

        self.static_text.SetMaxSize(wx.Size(-1, 18))

        self.staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
                                             wx.DefaultPosition, wx.DefaultSize, 0)

        self.staticText_show.SetMaxSize(wx.Size(-1, 20))

        # show_panel布局设置

        # 布局
        self.meta_sizer.Add(self.info_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.meta_sizer.Add(self.static_text, 1, wx.EXPAND | wx.ALL, 2)
        self.meta_sizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.meta_sizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        self.meta_sizer.Add(self.show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.meta_sizer)

        self.show_panel.Layout()
        self.Layout()
        self.Centre(wx.BOTH)

    def initFigure(self):
        show_panel = self.show_panel
        for child in show_panel.GetChildren():
            # print child
            child.Destroy()

    def onClick_button_t1a(self, event):
        self.initFigure()
        sizer = self.show_panel.GetSizer()
        cog_df=build_meta.build_euc_dis(cp.model_d,cp.real_d)

        mod_d = cp.model_d
        rea_d = cp.real_d

        SVD_result_model_d = []
        i = 0
        for index in cp.model_d:
            lala = svdArg.svdAlg(cp.model_d[i])
            SVD_result_model_d.append([svdArg.svdAlg(cp.model_d[i]).tolist()])
            i += 1

        # SVD_result_model_d = svdArg.svdAlg(cp.model_d)
        SVD_result_real_d = svdArg.svdAlg(cp.real_d)

        # cog_df_U = build_meta.build_euc_dis2(SVD_result_model_d[0],SVD_result_real_d[0])
        # cog_df_sigma = build_meta.build_euc_dis(SVD_result_model_d[1], SVD_result_real_d[1])
        # cog_df_V = build_meta.build_euc_dis2(SVD_result_model_d[2], SVD_result_real_d[2])

        cog_df_sigma = svdArg.svdAlg(cp.real_d.tolist())

        # cog_df_thefun_mod = np.array([[[37.124935639]],
        #                               [[36.6334149712]],
        #                               [[36.5780938949]],
        #                               [[36.9210554687]],
        #                               [[36.9948088198]],
        #                               [[37.4217945572]],
        #                               [[37.8204007778]],
        #                               [[36.7774746279]],
        #                               [[36.1485002394]],
        #                               [[37.1160381995]],
        #                               [[36.3231069291]],
        #                               [[37.1251814868]],
        #                               [[36.8795515708]]])
        cog_df_thefun_mod = np.array(SVD_result_model_d)

        # cog_df_thefun_real = np.matrix([[38.67286742942914]])
        cog_df_thefun_real = np.matrix([SVD_result_real_d])

        cog_df = build_meta.build_euc_dis(cog_df_thefun_mod, cog_df_thefun_real)

        figure1 = Figure()
        ax1= figure1.add_subplot(111)
        figure2 = Figure()
        ax2 =figure2.add_subplot(111)

        dr.draw_dis_distri(cog_df, 'euc',ax1)
        dr.draw_distance_violin(cog_df, ['euc'],ax2)

        canvas1 = FigureCanvas(self.show_panel, -1, figure1)
        canvas2 = FigureCanvas(self.show_panel, -1, figure2)

        canvas1.SetMinSize((460, 300))
        canvas1.SetMaxSize((460, 300))

        canvas2.SetMinSize((460, 300))
        canvas2.SetMaxSize((460, 300))

        canvas1.draw()
        canvas2.draw()

        sizer.Add(canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # # ---------------------------------
        # # figure3 = Figure()
        # # ax3 = figure3.add_subplot(111)
        # figure4 = Figure()
        # ax4 = figure4.add_subplot(111)
        #
        # dr.draw_distance_violin(cog_df, ['euc'], ax4)
        # # dr.draw_dis_point(cog_df, 'euc', ax3)
        #
        # # canvas3 = FigureCanvas(self.show_panel, -1, figure3)
        # canvas4 = FigureCanvas(self.show_panel, -1, figure4)
        #
        # # canvas3.SetMinSize((460, 300))
        # # canvas3.SetMaxSize((460, 300))
        #
        # canvas4.SetMinSize((460, 300))
        # canvas4.SetMaxSize((460, 300))
        #
        # # canvas3.draw()
        # canvas4.draw()
        #
        # # sizer.Add(canvas3, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(canvas4, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # # ----------------------------------------------

        self.show_panel.SetupScrolling()
        self.show_panel.Layout()

    def onClick_button_t2a(self, event):
        self.initFigure()

        sizer = self.show_panel.GetSizer()
        cog_df=build_meta.build_mah_dis(cp.model_d,cp.real_d)

        SVD_result_model_d = []
        i = 0
        for index in cp.model_d:
            lala = svdArg.svdAlg(cp.model_d[i])
            SVD_result_model_d.append([svdArg.svdAlg(cp.model_d[i]).tolist()])
            i += 1

        # SVD_result_model_d = svdArg.svdAlg(cp.model_d)
        SVD_result_real_d = svdArg.svdAlg(cp.real_d)


        cog_df_sigma = svdArg.svdAlg(cp.real_d.tolist())

        cog_df_thefun_mod = np.array(SVD_result_model_d)

        cog_df_thefun_real = np.matrix([SVD_result_real_d])

        # cog_df_thefun_mod = np.array([[[37.124935639], [37.124935639]],
        #                               [[36.6334149712], [36.6334149712]],
        #                               [[36.5780938949], [36.5780938949]],
        #                               [[36.9210554687], [36.9210554687]],
        #                               [[36.9948088198], [36.9948088198]],
        #                               [[37.4217945572], [37.4217945572]],
        #                               [[37.8204007778], [37.8204007778]],
        #                               [[36.7774746279], [36.7774746279]],
        #                               [[36.1485002394], [36.1485002394]],
        #                               [[37.1160381995], [37.1160381995]],
        #                               [[36.3231069291], [36.3231069291]],
        #                               [[37.1251814868], [37.1251814868]],
        #                               [[36.8795515708], [36.8795515708]]])
        #
        # cog_df_thefun_real = np.matrix([[38.67286742942914], [38.67286742942914]])

        # cog_df = build_meta.build_mah_dis(cog_df_thefun_mod, cog_df_thefun_real)

        figure1 = Figure()
        ax1= figure1.add_subplot(111)
        figure2 = Figure()
        ax2 =figure2.add_subplot(111)

        # dr.draw_dis_distri(cog_df, 'mah',ax1)
        # dr.draw_distance_box(cog_df, ['mah'],ax2)

        canvas1 = FigureCanvas(self.show_panel, -1, figure1)
        canvas2 = FigureCanvas(self.show_panel, -1, figure2)

        canvas1.SetMinSize((460, 300))
        canvas1.SetMaxSize((460, 300))

        canvas2.SetMinSize((460, 300))
        canvas2.SetMaxSize((460, 300))

        canvas1.draw()
        canvas2.draw()

        sizer.Add(canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # # ---------------------------------
        # # figure3 = Figure()
        # # ax3 = figure3.add_subplot(111)
        # figure4 = Figure()
        # ax4 = figure4.add_subplot(111)
        #
        # dr.draw_distance_violin(cog_df, ['euc'], ax4)
        # # dr.draw_dis_point(cog_df, 'euc', ax3)
        #
        # # canvas3 = FigureCanvas(self.show_panel, -1, figure3)
        # canvas4 = FigureCanvas(self.show_panel, -1, figure4)
        #
        # # canvas3.SetMinSize((460, 300))
        # # canvas3.SetMaxSize((460, 300))
        #
        # canvas4.SetMinSize((460, 300))
        # canvas4.SetMaxSize((460, 300))
        #
        # # canvas3.draw()
        # canvas4.draw()
        #
        # # sizer.Add(canvas3, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(canvas4, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # # ----------------------------------------------

        self.show_panel.SetupScrolling()
        self.show_panel.Layout()

    def onClick_button_t3a(self, event):
        self.initFigure()
        sizer = self.show_panel.GetSizer()
        cog_df=build_meta.build_che_dis(cp.model_d,cp.real_d)

        SVD_result_model_d = []
        i = 0
        for index in cp.model_d:
            lala = svdArg.svdAlg(cp.model_d[i])
            SVD_result_model_d.append([svdArg.svdAlg(cp.model_d[i]).tolist()])
            i += 1

        # SVD_result_model_d = svdArg.svdAlg(cp.model_d)
        SVD_result_real_d = svdArg.svdAlg(cp.real_d)

        cog_df_sigma = svdArg.svdAlg(cp.real_d.tolist())

        cog_df_thefun_mod = np.array(SVD_result_model_d)

        cog_df_thefun_real = np.matrix([SVD_result_real_d])

        # cog_df_thefun_mod = np.array([[[37.124935639], [1]],
        #                               [[36.6334149712], [1]],
        #                               [[36.5780938949], [1]],
        #                               [[36.9210554687], [1]],
        #                               [[36.9948088198], [1]],
        #                               [[37.4217945572], [1]],
        #                               [[37.8204007778], [1]],
        #                               [[36.7774746279], [1]],
        #                               [[36.1485002394], [1]],
        #                               [[37.1160381995], [1]],
        #                               [[36.3231069291], [1]],
        #                               [[37.1251814868], [1]],
        #                               [[36.8795515708], [1]]])
        #
        # cog_df_thefun_real = np.matrix([[38.67286742942914], [1]])

        cog_df = build_meta.build_che_dis(cog_df_thefun_mod, cog_df_thefun_real)

        figure1 = Figure()
        ax1= figure1.add_subplot(111)
        figure2 = Figure()
        ax2 =figure2.add_subplot(111)

        dr.draw_dis_distri(cog_df, 'che',ax1)
        dr.draw_distance_violin(cog_df, ['che'],ax2)

        canvas1 = FigureCanvas(self.show_panel, -1, figure1)
        canvas2 = FigureCanvas(self.show_panel, -1, figure2)

        canvas1.SetMinSize((460, 300))
        canvas1.SetMaxSize((460, 300))

        canvas2.SetMinSize((460, 300))
        canvas2.SetMaxSize((460, 300))

        canvas1.draw()
        canvas2.draw()


        sizer.Add(canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # # ---------------------------------
        # # figure3 = Figure()
        # # ax3 = figure3.add_subplot(111)
        # figure4 = Figure()
        # ax4 = figure4.add_subplot(111)
        #
        # dr.draw_distance_violin(cog_df, ['euc'], ax4)
        # # dr.draw_dis_point(cog_df, 'euc', ax3)
        #
        # # canvas3 = FigureCanvas(self.show_panel, -1, figure3)
        # canvas4 = FigureCanvas(self.show_panel, -1, figure4)
        #
        # # canvas3.SetMinSize((460, 300))
        # # canvas3.SetMaxSize((460, 300))
        #
        # canvas4.SetMinSize((460, 300))
        # canvas4.SetMaxSize((460, 300))
        #
        # # canvas3.draw()
        # canvas4.draw()
        #
        # # sizer.Add(canvas3, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(canvas4, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # # ----------------------------------------------

        self.show_panel.SetupScrolling()
        self.show_panel.Layout()


    def onClick_button_t4a(self, event):
        self.initFigure()
        sizer = self.show_panel.GetSizer()
        cog_df=build_meta.build_man_dis(cp.model_d,cp.real_d)

        # cog_df_thefun_mod = np.array([[[37.124935639]],
        #                               [[36.6334149712]],
        #                               [[36.5780938949]],
        #                               [[36.9210554687]],
        #                               [[36.9948088198]],
        #                               [[37.4217945572]],
        #                               [[37.8204007778]],
        #                               [[36.7774746279]],
        #                               [[36.1485002394]],
        #                               [[37.1160381995]],
        #                               [[36.3231069291]],
        #                               [[37.1251814868]],
        #                               [[36.8795515708]]])
        #
        # cog_df_thefun_real = np.matrix([38.67286742942914, ])

        SVD_result_model_d = []
        i = 0
        for index in cp.model_d:
            lala = svdArg.svdAlg(cp.model_d[i])
            SVD_result_model_d.append([svdArg.svdAlg(cp.model_d[i]).tolist()])
            i += 1

        # SVD_result_model_d = svdArg.svdAlg(cp.model_d)
        SVD_result_real_d = svdArg.svdAlg(cp.real_d)

        cog_df_sigma = svdArg.svdAlg(cp.real_d.tolist())

        cog_df_thefun_mod = np.array(SVD_result_model_d)

        cog_df_thefun_real = np.matrix([SVD_result_real_d])

        cog_df = build_meta.build_man_dis(cog_df_thefun_mod, cog_df_thefun_real)

        figure1 = Figure()
        ax1= figure1.add_subplot(111)
        figure2 = Figure()
        ax2 =figure2.add_subplot(111)

        dr.draw_dis_distri(cog_df, 'man',ax1)
        dr.draw_distance_violin(cog_df, ['man'],ax2)

        canvas1 = FigureCanvas(self.show_panel, -1, figure1)
        canvas2 = FigureCanvas(self.show_panel, -1, figure2)

        canvas1.SetMinSize((460, 300))
        canvas1.SetMaxSize((460, 300))

        canvas2.SetMinSize((460, 300))
        canvas2.SetMaxSize((460, 300))

        canvas1.draw()
        canvas2.draw()


        sizer.Add(canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # # ---------------------------------
        # # figure3 = Figure()
        # # ax3 = figure3.add_subplot(111)
        # figure4 = Figure()
        # ax4 = figure4.add_subplot(111)
        #
        # dr.draw_distance_violin(cog_df, ['euc'], ax4)
        # # dr.draw_dis_point(cog_df, 'euc', ax3)
        #
        # # canvas3 = FigureCanvas(self.show_panel, -1, figure3)
        # canvas4 = FigureCanvas(self.show_panel, -1, figure4)
        #
        # # canvas3.SetMinSize((460, 300))
        # # canvas3.SetMaxSize((460, 300))
        #
        # canvas4.SetMinSize((460, 300))
        # canvas4.SetMaxSize((460, 300))
        #
        # # canvas3.draw()
        # canvas4.draw()
        #
        # # sizer.Add(canvas3, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(canvas4, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # # ----------------------------------------------

        self.show_panel.SetupScrolling()
        self.show_panel.Layout()


    def onClick_button_t5a(self, event):
        self.initFigure()
        sizer = self.show_panel.GetSizer()
        cog_df=build_meta.build_KL_dis(cp.model_d,cp.real_d)

        # cog_df_thefun_mod = np.array([[[37.124935639]],
        #                               [[36.6334149712]],
        #                               [[36.5780938949]],
        #                               [[36.9210554687]],
        #                               [[36.9948088198]],
        #                               [[37.4217945572]],
        #                               [[37.8204007778]],
        #                               [[36.7774746279]],
        #                               [[36.1485002394]],
        #                               [[37.1160381995]],
        #                               [[36.3231069291]],
        #                               [[37.1251814868]],
        #                               [[36.8795515708]]])
        #
        # cog_df_thefun_real = np.matrix([38.67286742942914, ])

        SVD_result_model_d = []
        i = 0
        for index in cp.model_d:
            lala = svdArg.svdAlg(cp.model_d[i])
            SVD_result_model_d.append([svdArg.svdAlg(cp.model_d[i]).tolist()])
            i += 1

        # SVD_result_model_d = svdArg.svdAlg(cp.model_d)
        SVD_result_real_d = svdArg.svdAlg(cp.real_d)

        cog_df_sigma = svdArg.svdAlg(cp.real_d.tolist())

        cog_df_thefun_mod = np.array(SVD_result_model_d)

        cog_df_thefun_real = np.matrix([SVD_result_real_d])

        cog_df = build_meta.build_KL_dis(cog_df_thefun_mod, cog_df_thefun_real)

        figure1 = Figure()
        ax1= figure1.add_subplot(111)
        figure2 = Figure()
        ax2 =figure2.add_subplot(111)

        dr.draw_dis_distri(cog_df, 'KL',ax1)
        dr.draw_distance_violin(cog_df, ['KL'],ax2)

        canvas1 = FigureCanvas(self.show_panel, -1, figure1)
        canvas2 = FigureCanvas(self.show_panel, -1, figure2)

        canvas1.SetMinSize((460, 300))
        canvas1.SetMaxSize((460, 300))

        canvas2.SetMinSize((460, 300))
        canvas2.SetMaxSize((460, 300))

        canvas1.draw()
        canvas2.draw()


        sizer.Add(canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # # ---------------------------------
        # # figure3 = Figure()
        # # ax3 = figure3.add_subplot(111)
        # figure4 = Figure()
        # ax4 = figure4.add_subplot(111)
        #
        # dr.draw_distance_violin(cog_df, ['euc'], ax4)
        # # dr.draw_dis_point(cog_df, 'euc', ax3)
        #
        # # canvas3 = FigureCanvas(self.show_panel, -1, figure3)
        # canvas4 = FigureCanvas(self.show_panel, -1, figure4)
        #
        # # canvas3.SetMinSize((460, 300))
        # # canvas3.SetMaxSize((460, 300))
        #
        # canvas4.SetMinSize((460, 300))
        # canvas4.SetMaxSize((460, 300))
        #
        # # canvas3.draw()
        # canvas4.draw()
        #
        # # sizer.Add(canvas3, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(canvas4, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)
        # # ----------------------------------------------

        self.show_panel.SetupScrolling()
        self.show_panel.Layout()


