# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import print_function
import thread

import time

import sys
import wx
import wx.xrc
import wx.lib.newevent
from wx import grid
from wx.lib.mixins.listctrl import TextEditMixin

import ProcessBar as pb
from ModelCalibration.BuildMetaModel import importData
import commonTag

from ShowNotebook import *
import Sql
import cPickle

sym1=1
class OptPanel(wx.Panel):
    count = 0
    def __init__(self, parent,n_id=None):
        """ 导入数据 """
        importData(None, n_id, 1)
        """ 初始化 """
        wx.Panel.__init__(self, parent, n_id * 2, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.n_id = n_id
        self.sym = 1
        # self 的布局，有 scrollPanel 和input_panel两个元素
        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        # 为实现滚动条加入 scrollPanel
        # self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
        #                                               wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        # self.scrolledWindow.SetScrollRate(5, 5)

        self.scrolledWindow = scrolled.ScrolledPanel(self, 3,
                                                     style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.scrolledWindow.SetAutoLayout(1)
        self.scrolledWindow.SetupScrolling()

        scrollPanel = self.scrolledWindow
        # input_panel 的布局，元素为显示的控件
        self.gbSizer = wx.GridBagSizer(5, 5)
        self.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)



        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer_show = wx.GridBagSizer(5, 5)
        self.gbSizer_show.SetFlexibleDirection(wx.BOTH)
        self.gbSizer_show.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 上部modelInfo_Panel
        self.modelInfo_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.modelInfo_panel.SetMaxSize(wx.Size(-1,100))
        # modelInfo_panel 的布局，元素为显示的控件
        self.modelInfo_panel.gbSizer = wx.GridBagSizer(5, 5)
        self.modelInfo_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.modelInfo_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 上部input_Panel
        self.input_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                       (-1, 120), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1,160))

        first_positon = 0
        next_positon = 1 + first_positon
        

        #模型名称
        # modelinfo = Sql.selectSql(args=(cp.n_id,), sql=Sql.selectModel)
        # self.static_text_name = wx.StaticText(self.input_panel, -1, label="模型名称:")
        # self.text_ctrl_name = wx.TextCtrl(self.input_panel, -1, size=(280, -1), value=modelinfo[0][0])
        # self.text_ctrl_name.Disable()

        self.m_staticText_b = wx.StaticText(self.input_panel, wx.ID_ANY, u"建模方法：",
                                            wx.DefaultPosition, wx.DefaultSize, 0)

        self.methods = ['SVR', 'GPR', 'KRR']
        self.combobox_b = wx.ComboBox(self.input_panel, -1, size=wx.Size(425, -1), choices=self.methods)
        self.combobox_b.SetSelection(0)
        self.combobox_b.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox_b)


        self.static_text_1 = wx.StaticText(self.input_panel, -1, label="群体总数:")
        self.text_ctrl_1 = wx.TextCtrl(self.input_panel, -1,size=(425,-1), value='2000')
        self.static_text_2 = wx.StaticText(self.input_panel, -1, label="交叉概率:")
        self.text_ctrl_2 = wx.TextCtrl(self.input_panel, -1,size=(425,-1), value='0.5')
        self.static_text_3 = wx.StaticText(self.input_panel, -1, label="变异概率:")
        self.text_ctrl_3 = wx.TextCtrl(self.input_panel, -1,size=(425,-1), value='0.05')
        self.static_text_4 = wx.StaticText(self.input_panel, -1, label="迭代次数:")
        self.text_ctrl_4 = wx.TextCtrl(self.input_panel, -1, size=(425,-1), value='15')


        self.gbSizer.Add(self.m_staticText_b, wx.GBPosition(0, 4),
                         wx.GBSpan(1, 1), wx.ALL, 0)
        self.gbSizer.Add(self.combobox_b, wx.GBPosition(0, 5),
                         wx.GBSpan(1, 3), wx.ALL, 0)

        self.gbSizer.Add(self.static_text_1, wx.GBPosition(0, 11),
                               wx.GBSpan(1, 1), wx.ALL, 0)
        self.gbSizer.Add(self.text_ctrl_1, wx.GBPosition(0, 12),
                               wx.GBSpan(1, 3), wx.ALL, 0)
        self.gbSizer.Add(self.static_text_2, wx.GBPosition(1, 4),
                         wx.GBSpan(1, 1), wx.ALL, 0)
        self.gbSizer.Add(self.text_ctrl_2, wx.GBPosition(1, 5),
                         wx.GBSpan(1, 3), wx.ALL, 0)
        self.gbSizer.Add(self.static_text_3, wx.GBPosition(1, 11),
                         wx.GBSpan(1, 1), wx.ALL, 0)
        self.gbSizer.Add(self.text_ctrl_3, wx.GBPosition(1, 12),
                         wx.GBSpan(1, 3), wx.ALL, 0)
        self.gbSizer.Add(self.static_text_4, wx.GBPosition(2, 4),
                         wx.GBSpan(1, 1), wx.ALL, 0)
        self.gbSizer.Add(self.text_ctrl_4, wx.GBPosition(2, 5),
                         wx.GBSpan(1, 3), wx.ALL, 0)

        ''' 元模型建模按钮的panel begins '''
        self.m_button_ok = wx.Button(self.input_panel, wx.ID_ANY, u"校准", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.SetBitmap(wx.Bitmap('icon/run.ico'))
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.cal_button)
        self.gbSizer.Add(self.m_button_ok, wx.GBPosition(3, 14),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        # self.m_button_reset = wx.Button(self.input_panel, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.Size(80, -1), 0)
        # self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)
        # self.gbSizer.Add(self.m_button_reset, wx.GBPosition(next_positon, 13),
        #                  wx.GBSpan(1, 1), wx.ALL, 5)

        # self.m_button_show = wx.Button(self.input_panel, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.Size(80, -1), 0)
        # self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)
        # self.m_button_show.Show(False)
        # self.gbSizer.Add(self.m_button_show, wx.GBPosition(next_positon, 15),
        #                  wx.GBSpan(1, 1), wx.ALL, 5)
        ''' 元模型建模按钮的panel ends '''

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                              wx.DefaultSize, wx.LI_HORIZONTAL)
        # 提示信息
        # modelinfo = Sql.selectSql(args=(cp.n_id,), sql=Sql.selectModel)
        #
        # self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"参数设置：",
        #                                              wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_staticText_set.SetLabelText(u'模型：' + modelinfo[0][0])

        #self.m_staticText_set.SetMaxSize(wx.Size(-1, 18))

        self.m_staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
                                          wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText_show.SetMaxSize(wx.Size(-1, 20))

        # n_id = self.GetParent().GetParent().navTree.GetItemData( self.GetParent().GetParent().navTree.GetSelection())
        # 上方提示信息Panel
        commonTag.setModeltag(self.modelInfo_panel, cp.n_id)
        
        # 提示信息
        self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"参数设置：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_set.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))

        self.m_staticText_set.SetMaxSize(wx.Size(-1, 18))

        # self.m_staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
        #                                   wx.DefaultPosition, wx.DefaultSize, 0)
        #
        # self.m_staticText_show.SetMaxSize(wx.Size(-1, 20))
        # show_panel布局设置
        self.input_panel.SetSizer(self.gbSizer)
        self.modelInfo_panel.SetSizer(self.modelInfo_panel.gbSizer)
        scrollPanel.SetSizer(self.gbSizer_show)
        scrollPanel.Layout()
        # 布局
        self.bSizer.Add(self.modelInfo_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.bSizer.Add(self.m_staticText_set, 1, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.bSizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        #self.bSizer.Add(self.m_staticText_show, 0, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.bSizer)

        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def onSelect_combobox_b(self, event):
        pos = self.combobox_b.GetSelection()
        method_name = self.methods[pos]
        if method_name == "SVR":
            print ("SVR")
            self.sym = 1
        elif method_name == "GPR":
            print ("GPR")
            self.sym = 2
        else:
            print ("KRR")
            self.sym = 3

    def cal_button(self, event):
        self.loadFunction(self.cal_Function,"校准中", "优化迭代已经完成！")
    
    def cal_Function(self):
        show_panel = self.scrolledWindow

        for child in show_panel.Children:
            child.Destroy()

        show_panel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        sizer = self.gbSizer_show

        self.m_notebook1 = wx.Notebook(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_notebook1.Hide()
        self.m_panel1 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_panel3 = wx.Panel(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer2.Add(self.m_panel3, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer2_1 = wx.GridBagSizer(0, 0)
        gbSizer2_1.SetFlexibleDirection(wx.BOTH)
        gbSizer2_1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        #text
        self.static_text_v1 = wx.StaticText(self.m_panel3, label='')
        self.static_text_v1.SetMinSize((416,12))
        self.static_text_v1.SetMaxSize((416, 12))
        gbSizer2_1.Add(self.static_text_v1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.static_text_v2 = wx.StaticText(self.m_panel3, label='度量结果',size=(416,-1),style=wx.ALIGN_CENTER)
        self.static_text_v2.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))
        gbSizer2_1.Add(self.static_text_v2, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        # Grid
        self.grid1 = wx.grid.Grid(self.m_panel3)
        self.grid1.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.grid1.SetMinSize((416, 410))
        self.grid1.SetMaxSize((416, 410))

        gbSizer2_1.Add(self.grid1, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_panel3.SetSizer(gbSizer2_1)
        self.m_panel3.Layout()
        gbSizer2_1.Fit(self.m_panel3)

        #Figure
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(self.m_panel1, -1, self.figure)
        self.canvas.SetMaxSize((640, 440))
        self.canvas.SetMinSize((640, 440))
        gbSizer2.Add(self.canvas, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_panel1.SetSizer(gbSizer2)
        self.m_panel1.Layout()
        gbSizer2.Fit(self.m_panel1)
        self.m_notebook1.AddPage(self.m_panel1, u"校准过程", True)

        self.m_panel2 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer3 = wx.GridBagSizer(0, 0)
        gbSizer3.SetFlexibleDirection(wx.BOTH)
        gbSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_panel4 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer3.Add(self.m_panel4, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer2_2 = wx.GridBagSizer(0, 0)
        gbSizer2_2.SetFlexibleDirection(wx.BOTH)
        gbSizer2_2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        # text
        self.static_text_v3 = wx.StaticText(self.m_panel4, label='')
        self.static_text_v3.SetMinSize((416, 12))
        self.static_text_v3.SetMaxSize((416, 12))
        gbSizer2_2.Add(self.static_text_v3, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.static_text_v4 = wx.StaticText(self.m_panel4, label='最佳认知参数', size=(416, -1), style=wx.ALIGN_CENTER)
        self.static_text_v4.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体"))
        gbSizer2_2.Add(self.static_text_v4, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        # Grid
        self.grid2 = wx.grid.Grid(self.m_panel4)
        self.grid2.SetMinSize((416, 410))
        self.grid2.SetMaxSize((416, 410))
        self.grid2.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        gbSizer2_2.Add(self.grid2, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_panel4.SetSizer(gbSizer2_2)
        self.m_panel4.Layout()
        gbSizer2_2.Fit(self.m_panel4)

        #Figure
        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(self.m_panel2, -1, self.figure2)
        self.canvas2.SetMaxSize((640,440))
        self.canvas2.SetMinSize((640, 440))
        gbSizer3.Add(self.canvas2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_panel2.SetSizer(gbSizer3)
        self.m_panel2.Layout()
        gbSizer3.Fit(self.m_panel2)
        self.m_notebook1.AddPage(self.m_panel2, u"校准结果", False)

        sizer.Add(self.m_notebook1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        """"""
        # sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        # self.grid1 = wx.grid.Grid(show_panel)
        # self.grid1.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        # self.grid1.SetMinSize((400, 480))
        # self.grid1.SetMaxSize((400, 480))
        # sizer_v1 = wx.BoxSizer(orient=wx.VERTICAL)
        # static_text_v1 = wx.StaticText(show_panel, label='每次迭代的度量取值结果')
        # sizer_v1.Add(static_text_v1)
        # sizer_v1.Add(self.grid1)
        #
        # self.grid2 = wx.grid.Grid(show_panel)
        # self.grid2.SetMinSize((400, 480))
        # self.grid2.SetMaxSize((400, 480))
        # self.grid2.SetLabelBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        # sizer_v2 = wx.BoxSizer(orient=wx.VERTICAL)
        # static_text_v2 = wx.StaticText(show_panel, label='每次迭代的最佳认知参数取值结果')
        # sizer_v2.Add(static_text_v2)
        # sizer_v2.Add(self.grid2)
        #
        # sizer.Add(sizer_v1,wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(sizer_v2,wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        #
        # sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        # self.figure = Figure()
        # self.axes = self.figure.add_subplot(111)
        # # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        # self.canvas = FigureCanvas(show_panel, -1, self.figure)
        # sizer_v3 = wx.BoxSizer(orient=wx.VERTICAL)
        # static_text_v3 = wx.StaticText(show_panel, label='度量值比较图')
        # sizer_v3.Add(static_text_v3)
        # sizer_v3.Add(self.canvas)
        #
        # self.figure2 = Figure()
        # self.axes2 = self.figure2.add_subplot(111)
        # # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        # self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)
        # sizer_v4 = wx.BoxSizer(orient=wx.VERTICAL)
        # static_text_v4 = wx.StaticText(show_panel, label='度量值差异图')
        # sizer_v4.Add(static_text_v4)
        # sizer_v4.Add(self.canvas2)
        #
        # sizer.Add(sizer_v3,wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Add(sizer_v4,wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        """"""

        show_panel.Layout()
        # print(self.text_ctrl_1.GetLineText(0))
        pn = int(self.text_ctrl_1.GetLineText(0))
        itn = int(self.text_ctrl_4.GetLineText(0))
        cp = float(self.text_ctrl_2.GetLineText(0))
        mp = float(self.text_ctrl_3.GetLineText(0))
        if self.sym == 1:
            print(self.n_id)
            metamodel = Sql.selectMetaModel(self.n_id,"svr")
            GenericAlgorithm.GA(self,metamodel, pn, itn, cp, mp)
            print("------")
        elif self.sym == 2:
            metamodel = Sql.selectMetaModel(self.n_id, "gpr")
            GenericAlgorithm.GA(self, metamodel, pn, itn, cp, mp)
        elif self.sym == 3:
            metamodel = Sql.selectMetaModel(self.n_id, "bayes")
            GenericAlgorithm.GA(self, metamodel, pn, itn, cp, mp)
        self.m_notebook1.Show()
        show_panel.Layout()

    def loadFunction(self,function,tag, endInfo):
        self.xpb = pb.ProcessBar(None, tag, 1000)
        self.xpb.loadFunction(function, endInfo)

class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)