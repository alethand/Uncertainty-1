# -*- coding: utf-8 -*-

import wx
import numpy
from wx import grid
import Sql
from ModelCalibration import DoubleLoop as DL
from ModelCalibration import arg_order as ao
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
import matplotlib.pyplot as plt

'''将绘图操作嵌入到wxpython'''
class MPL_Panel_base(wx.Panel):
    '''''    # MPL_Panel_base面板,可以继承或者创建实例'''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

        self.Figure = matplotlib.figure.Figure(figsize=(4, 3))
        self.axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)

        self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)

        self.StaticText = wx.StaticText(self, -1, label='Show Help String')

        self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SubBoxSizer.Add(self.NavigationToolbar, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        self.SubBoxSizer.Add(self.StaticText, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.SubBoxSizer, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.TopBoxSizer)

        ###方便调用
        self.pylab = pylab
        self.pl = pylab
        self.pyplot = plt
        self.numpy = numpy
        self.numpy = numpy
        self.plt = plt

    def UpdatePlot(self):
        '''''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()

    def plot(self, *args, **kwargs):
        '''''#最常用的绘图命令plot '''
        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()

    def semilogx(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def grid(self, flag=True):
        ''''' ##显示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)

    def title_MPL(self, TitleString="wxMatPlotLib Example In wxPython"):
        ''''' # 给图像添加一个标题   '''
        self.axes.set_title(TitleString)

    def xlabel(self, XabelString="X"):
        ''''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)

    def ylabel(self, YabelString="Y"):
        ''''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)

    def xticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置X轴的刻度大小 '''
        self.axes.xaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.xaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def yticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置Y轴的刻度大小 '''
        self.axes.yaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.yaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def legend(self, *args, **kwargs):
        ''''' #图例legend for the plotting  '''
        self.axes.legend(*args, **kwargs)

    def xlim(self, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        ''' # 设置y轴的显示范围   '''
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        ''' # 再次画图前,必须调用该命令清空原来的图形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()

    def ShowHelpString(self, HelpString="Show Help String"):
        ''''' #可以用它来显示一些帮助信息,如鼠标位置等 '''
        self.StaticText.SetLabel(HelpString)

'''Ends of 将绘图操作嵌入到wxpython'''


class ShowPanel(wx.Panel):

    def __init__(self, parent=None):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        """"""
        self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
                                                wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = self.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer = wx.GridBagSizer(5, 5)
        self.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_grid4 = wx.grid.Grid(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid4.CreateGrid(5, 4)
        self.m_grid4.EnableEditing(True)
        self.m_grid4.EnableGridLines(True)
        self.m_grid4.EnableDragGridSize(False)
        self.m_grid4.SetMargins(0, 0)

        # Columns
        self.m_grid4.EnableDragColMove(False)
        self.m_grid4.EnableDragColSize(True)
        self.m_grid4.SetColLabelSize(30)
        self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.m_grid4.SetColLabelValue(0, "模型名称")
        self.m_grid4.SetColLabelValue(1, "参数名称")
        self.m_grid4.SetColLabelValue(2, "分布类型")
        self.m_grid4.SetColLabelValue(3, "分布参数")

        # Rows
        self.m_grid4.EnableDragRowSize(True)
        self.m_grid4.SetRowLabelSize(80)
        self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        self.gbSizer.Add(self.m_grid4, wx.GBPosition(3, 4),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        self.SetSizer(bSizer8)
        self.Layout()
        self.Centre(wx.BOTH)
        # bSizer8.Fit(self)



class TestPanel(wx.Panel):

    # para 为UPNavPanel中定义的用于传参的类的对象
    def __init__(self, parent = None, para=None, id = 0):
        self.model_id = id
        global a_mat
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        self.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        """实验 Start"""



        # 查询表确定参数是 认知2、固有1还是输入0
        # 根据参数名获取相应的抽样数据
        input_X = []
        Er_p = []
        Es_p = []

        results = input_X, Er_p, Es_p
        Es_p_name = []

        # FIXME: 需要选定参数变化 其它参数不变进行传播分析

        i = 0
        for type in para.partype:
            result = []
            record = Sql.show_sampling_result_with_type(type, self.model_id,para.parid[i])
            for r in record:
                result.append(r[0])
            results[type].append(result)
            if(type == 2):
                Es_p_name.append(str(record[0][1]))
            i += 1
        # 设置默认值
        self.esp = []
        for s in Es_p:
            self.esp.append(s[0])

        # 设置默认值
        self.erp = []
        for r in Er_p:
            self.erp.append(r[0])

        # 设置默认值
        self.input = []
        for ix in input_X:
            self.input.append(ix[0])

        order = ao.get_order(self.model_id)
        i = 0
        mark = 0
        x = []
        y = []
        for es in Es_p:  # 对每一组认知不确定参数 进行实验得出仿真输出
            j = 0
            for esp in es:
                test_esp = self.Esp_set(i,esp)
                re = ao.get_result(self.model_id, order, self.input, test_esp, self.erp)
                j += 1
                y.append(re)
                x.append(j)
                print('获得的仿真输出:')
                print(re)
            i += 1

            MPL = MPL_Panel_base(self)
            self.BoxSizer.Add(MPL, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)
            MPL.plot(x, y)
            MPL.xticker(100, 1)
            MPL.yticker(600, 200)
            print(Es_p_name[mark])

            MPL.title_MPL(u"ESP :"+Es_p_name[mark])
            MPL.grid()
            MPL.UpdatePlot()  # 必须刷新才能显示
            mark += 1
        """实验 End"""

        self.RightPanel = wx.Panel(self, -1)
        self.BoxSizer.Add(self.RightPanel, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.BoxSizer)

        # 创建FlexGridSizer
        self.FlexGridSizer = wx.FlexGridSizer(rows=9, cols=1, vgap=5, hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)


        self.RightPanel.SetSizer(self.FlexGridSizer)


        # MPL2_Frame界面居中显示
        self.Centre(wx.BOTH)


    # 替换实验值
    def Esp_set(self,esp_position,value):
        temp = self.esp
        temp[esp_position] = value
        return temp

    def set_name(self,name):
        self.name = name