# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
from __future__ import print_function
from __future__ import print_function


import time

import sys
import wx
import wx.xrc
import wx.lib.newevent
from wx import grid
from wx.lib.mixins.listctrl import TextEditMixin

import commonTag
from ModelValidate.ValidateBuildMetaModel import importData
from ShowNotebook import *
import Sql

sym1=1
class MetaPanel(wx.Panel):
    count = 0
    def __init__(self, parent,n_id,sym = 1):
        """ 导入数据 """
        importData(None, n_id, 1)
        """ 初始化 """
        wx.Panel.__init__(self, parent, n_id*2 - 1, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.sym = sym
        print(sym)
        # self 的布局，有 scrollPanel 和input_panel两个元素
        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        # 上部modelInfo_Panel
        self.modelInfo_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.modelInfo_panel.SetMaxSize(wx.Size(-1,100))
        # modelInfo_panel 的布局，元素为显示的控件
        self.modelInfo_panel.gbSizer = wx.GridBagSizer(5, 5)
        self.modelInfo_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.modelInfo_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        

        # 为实现滚动条加入 scrollPanel
        # self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
        #                                               wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        # self.scrolledWindow.SetScrollRate(5, 5)

        self.scrolledWindow = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.scrolledWindow.SetAutoLayout(1)
        self.scrolledWindow.SetupScrolling()

        self.show_panel = self.scrolledWindow
        # input_panel 的布局，元素为显示的控件
        self.gbSizer = wx.GridBagSizer(5, 5)
        self.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)



        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer_show = wx.GridBagSizer(5, 5)
        self.gbSizer_show.SetFlexibleDirection(wx.BOTH)
        self.gbSizer_show.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 上部input_Panel
        self.input_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                       (-1, 80), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1,80))

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_radioBtn1 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"欧式距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn1.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        self.m_radioBtn1.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t1a)
        bSizer1.Add(self.m_radioBtn1, 0, wx.ALL, 6)

        self.m_radioBtn2 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"曼哈顿距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn2.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t2a)
        bSizer1.Add(self.m_radioBtn2, 0, wx.ALL, 6)

        self.m_radioBtn3 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"马氏距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn3.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t3a)
        bSizer1.Add(self.m_radioBtn3, 0, wx.ALL, 6)

        self.m_radioBtn4 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"切比雪夫距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn4.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t4a)
        bSizer1.Add(self.m_radioBtn4, 0, wx.ALL, 6)

        self.m_radioBtn5 = wx.RadioButton(self.input_panel, wx.ID_ANY, u"KL散度验证", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_radioBtn5.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t5a)
        bSizer1.Add(self.m_radioBtn5, 0, wx.ALL, 6)

        ''' 元模型建模按钮的panel ends '''

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                              wx.DefaultSize, wx.LI_HORIZONTAL)

        # 上方提示信息Panel
        commonTag.setModeltag(self.modelInfo_panel, n_id)
        
        # 提示信息
        self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"验证方式：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_set.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))

        self.m_staticText_set.SetMaxSize(wx.Size(-1, 18))

        self.m_staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
                                          wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText_show.SetMaxSize(wx.Size(-1, 20))


        # show_panel布局设置
        self.input_panel.SetSizer(bSizer1)
        # self.gbSizer.Add(bSizer1)
        
        self.modelInfo_panel.SetSizer(self.modelInfo_panel.gbSizer)
        self.show_panel.SetSizer(self.gbSizer_show)
        self.show_panel.Layout()
        # 布局
        self.bSizer.Add(self.modelInfo_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.bSizer.Add(self.m_staticText_set, 1, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.bSizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        #self.bSizer.Add(self.m_staticText_show, 0, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(self.show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.bSizer)

        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def initFigure(self,flag = 1):
        # self.button_1a.Disable()
        global sym1
        # print 'self.sym: '%(self.sym)
        # print 'sym1: %d'%(sym1)
        show_panel = self.show_panel

        # 清空panel
        for child in show_panel.GetChildren():
            child.Destroy()

        sizer = self.show_panel.GetSizer()

#        sizer.Remove(self.grid_out)
        self.grid_out = wx.grid.Grid(show_panel)
        # self.sw = csw(show_panel)
        if(flag == 1):
            self.figure = Figure()
            self.axes = self.figure.add_subplot(111)
            self.figure2 = Figure()
            self.axes2 = self.figure2.add_subplot(111)
            # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
            self.canvas = FigureCanvas(show_panel, -1, self.figure)
            self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

            self.canvas.SetMinSize((460, 250))
            self.canvas.SetMaxSize((460, 250))

            self.canvas2.SetMinSize((460, 250))
            self.canvas2.SetMaxSize((460, 250))

            sizer.Add(self.canvas, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)
            sizer.Add(self.canvas2, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        sizer.Add(self.grid_out, wx.GBPosition(1, 4), wx.GBSpan(1, 2), wx.ALL, 5)

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


class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)
