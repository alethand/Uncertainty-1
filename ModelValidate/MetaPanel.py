# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
from __future__ import print_function
from __future__ import print_function



import wx
import wx.xrc
import wx.lib.newevent
from wx import grid

import commonTag
from ModelValidate.ValidateBuildMetaModel import importData
from ShowNotebook import *
import ValidateBuildMetaModel as  build_meta
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# 右侧主面板的内容

class MetaPanel(wx.Panel):

    def __init__(self, parent,n_id):

        """ 导入数据 """
        importData(None, n_id, 1)
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

        self.m_radioBtn2 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"曼哈顿距离验证", wx.DefaultPosition, wx.DefaultSize,
                                          0)
        self.m_radioBtn2.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t2a)
        distance_sizer.Add(self.m_radioBtn2, 0, wx.ALL, 6)

        self.m_radioBtn3 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"马氏距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn3.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t3a)
        distance_sizer.Add(self.m_radioBtn3, 0, wx.ALL, 6)

        self.m_radioBtn4 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"切比雪夫距离验证", wx.DefaultPosition, wx.DefaultSize,
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

    def initFigure(self,flag = 1):
        show_panel = self.show_panel

        for child in show_panel.GetChildren():
            child.Destroy()

        sizer = self.show_panel.GetSizer()

        self.result_table = wx.grid.Grid(show_panel)
        if(flag == 1):
            self.figure1 = Figure()
            self.axes1 = self.figure1.add_subplot(111)
            self.figure2 = Figure()
            self.axes2 = self.figure2.add_subplot(111)

            self.canvas1 = FigureCanvas(show_panel, -1, self.figure1)
            self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

            self.canvas1.SetMinSize((460, 250))
            self.canvas1.SetMaxSize((460, 250))

            self.canvas2.SetMinSize((460, 250))
            self.canvas2.SetMaxSize((460, 250))

            sizer.Add(self.canvas1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
            sizer.Add(self.canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        sizer.Add(self.result_table, wx.GBPosition(1, 4), wx.GBSpan(1, 2), wx.ALL, 5)

    def onClick_button_t1a(self, event):
        self.initFigure()
        build_meta.buildoushidistance(self, build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)  # , cus_C, cus_epsilon, cus_kernel)

    def onClick_button_t2a(self, event):
        self.initFigure()
        build_meta.buildmanhadundistance(self, build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                         build_meta.input_v1)

    def onClick_button_t3a(self, event):
        self.initFigure()
        build_meta.buildmshidistance(self, build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                     build_meta.input_v1)

    def onClick_button_t4a(self, event):
        self.initFigure()
        build_meta.buildqiebixuefudistance(self, build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                           build_meta.input_v1)

    def onClick_button_t5a(self, event):
        self.initFigure(-1)
        build_meta.buildKLdistance(self, build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                   build_meta.input_v1)

