# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
import wx.xrc
import wx.lib.newevent
import wx.dataview
import commonTag
from ShowNotebook import *
import ValidateBuildMetaModel as  build_meta
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# 右侧主面板的内容
import data_related as dr
import ValidateUi as cp
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#有中文出现的情况，需要u'内容'

class DataPanel(wx.Panel):

    def __init__(self, parent, n_id):

        #记录真实数据的维度信息
        self.num_rows=cp.real_d.shape[0]
        self.num_cols=cp.real_d.shape[1]

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
        # 上方提示信息Panel
        commonTag.setModeltag(self.info_panel, n_id)

        # 上部input_Panel
        self.input_panel = MyInputPanel(self)
        self.input_panel.SetMaxSize(wx.Size(-1, 80))

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

        # self.show_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.show_panel.SetSizer(self.show_sizer)

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.LI_HORIZONTAL)

        # 布局
        self.meta_sizer.Add(self.info_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.meta_sizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.meta_sizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        self.meta_sizer.Add(self.show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.meta_sizer)

        self.show_panel.Layout()
        self.Layout()
        self.Centre(wx.BOTH)


# DataPanel->MyInputPanel
class MyInputPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(576, 105), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        # 得到真实数据的维度
        self.data_panel=self.GetParent()
        str_num_rows='{}'.format(self.data_panel.num_rows)
        str_num_cols='{}'.format(self.data_panel.num_cols)


        gbSizer = wx.GridBagSizer(5, 5)
        gbSizer.SetFlexibleDirection(wx.BOTH)
        gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.real_text = wx.StaticText(self, wx.ID_ANY, u"真实数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.real_text.Wrap(-1)

        gbSizer.Add(self.real_text, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.row_text = wx.StaticText(self, wx.ID_ANY, u"数据条数：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.row_text.Wrap(-1)

        gbSizer.Add(self.row_text, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.rows_text = wx.StaticText(self, wx.ID_ANY, str_num_rows, wx.DefaultPosition, wx.DefaultSize, 0)
        self.rows_text.Wrap(-1)

        gbSizer.Add(self.rows_text, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cols_text = wx.StaticText(self, wx.ID_ANY, u"维度：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cols_text.Wrap(-1)

        gbSizer.Add(self.cols_text, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cols_text = wx.StaticText(self, wx.ID_ANY, str_num_cols, wx.DefaultPosition, wx.DefaultSize, 0)
        self.cols_text.Wrap(-1)

        gbSizer.Add(self.cols_text, wx.GBPosition(0, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        # self.data_show = wx.Button(self, wx.ID_ANY, u"显示前五条数据", wx.DefaultPosition, wx.DefaultSize, 0)
        # gbSizer.Add(self.data_show, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.data_visual = wx.Button(self, wx.ID_ANY, u"数据可视化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer.Add(self.data_visual, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.SetSizer(gbSizer)
        self.Layout()

        # Connect Events
        # self.data_show.Bind(wx.EVT_BUTTON, self.draw_table)
        self.data_visual.Bind(wx.EVT_BUTTON, self.draw_data_figure)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    # 把真实数据用表格展示出来
    def draw_table(self):
        show_panel = self.data_panel.show_panel
        sizer = show_panel.GetSizer()
        # 一维数据
        grid = wx.grid.Grid(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        grid.EnableEditing(False)
        grid.EnableGridLines(True)
        grid.EnableDragGridSize(False)
        grid.SetMargins(0, 0)

        if self.data_panel.num_cols==1:
            min_num=np.min((self.data_panel.num_rows,10))

            grid.CreateGrid(1, min_num)
            grid.SetRowLabelValue(0, '真实数据输出')
            grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)

            for i in np.arange(min_num):
                grid.SetColLabelValue(i, '第{}条'.format(i+1))
                grid.SetCellValue(0, i, str(round(cp.real_d[i], 3)))

        # 多维数据
        else:
            min_num_col=np.min((self.data_panel.num_cols,10))
            min_num_row=np.min((self.data_panel.num_rows,10))
            grid.CreateGrid(min_num_row, min_num_col)
            for i in np.arange(min_num_row):
                grid.SetRowLabelValue(i, '第{}条'.format(i+1))
                for j in np.arange(min_num_col):
                    grid.SetColLabelValue(j, '第{}维'.format(j+1))
                    grid.SetCellValue(i,j,str(round(cp.real_d[i][j], 3)))
        sizer.Add(grid, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        # sizer.Fit(show_panel)

    def draw_data_figure(self, event):
        show_panel=self.data_panel.show_panel
        sizer = show_panel.GetSizer()

        real_df=pd.DataFrame(cp.real_d)
        #一位数据
        if self.data_panel.num_cols==1:
            figure = Figure()
            ax = figure.add_subplot(111)
            sns.lineplot(np.arange(self.data_panel.num_rows),y=0,data=real_df,ax=ax)
            ax.set_xlabel(u'采样次序')
            ax.set_ylabel(u'y值')
            canvas = FigureCanvas(show_panel, -1, figure)
            canvas.SetMinSize((500, 450))
            canvas.draw()
            sizer.Add(canvas, wx.GBPosition(2, 1), wx.GBSpan(1, 2), wx.ALL, 5)
        # 2维数据
        elif self.data_panel.num_cols==2:
            figure = Figure()
            ax = figure.add_subplot(111)
            sns.scatterplot(x=real_df[0], y=real_df[1], data=real_df, ax=ax)
            ax.set_xlabel(u'y1：第一维')
            ax.set_ylabel(u'y2: 第二维')
            canvas = FigureCanvas(show_panel, -1, figure)
            canvas.SetMinSize((500, 450))
            canvas.draw()
            sizer.Add(canvas, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        elif self.data_panel.num_cols==3:
            pass
        # 只显示表不显示图
        else:
            pass

        self.draw_table()

        show_panel.SetupScrolling()
        show_panel.Layout()
