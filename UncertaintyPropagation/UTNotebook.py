# -*- coding: utf-8 -*-
from functools import wraps
import SamplingMethod as SM
import wx
from wx import aui, grid
import UPShowPanel
import UPSelectMethodPanel
import Sql
import commonTag

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

""""装饰器实现单例模式 方便传参"""
def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance

@singleton
class UTNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    # 以表格的形式显示参数信息
    # 参数的抽样方法为可选下拉框
    def ShowArg(self, record,n_id):
        """ 显示参数信息 Notebook """
        self.n_id = n_id
        pageId = n_id * 2 - 1
        flag = 0
        pageFocus = None
        for x in range(self.GetPageCount()):
            if pageId == self.GetPage(x).GetId():
                pageFocus = self.GetPage(x)
                flag = 1
            # if self.GetPage(x).GetId() > pageId:
            #     self.DeletePage(self.GetPageIndex(self.GetPage(x)))

        if flag != 0:

            pageFocus.SetFocus()
            self.Refresh()
        else:
            self.show_panel = wx.Panel(self, pageId, wx.DefaultPosition,
                                       wx.DefaultSize, wx.TAB_TRAVERSAL)
            title = u"设置抽样方法"
            self.AddPage(self.show_panel, title, True, wx.NullBitmap)

            show_panel = self.show_panel
            # show_panel 的布局，只有 scrollPanel 一个元素
            show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)

            # 为实现滚动条加入 scrollPanel
            show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY,
                                                          wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
            show_panel.scrolledWindow.SetScrollRate(5, 5)
            scrollPanel = show_panel.scrolledWindow
            # scrollPanel 的布局，元素为显示的控件
            show_panel.gbSizer = wx.GridBagSizer(5, 5)
            show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
            show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

            show_panel.show_table_grid = grid.Grid(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

            # Grid
            self.tablelen = len(record)
            show_panel.show_table_grid.CreateGrid(24, 13)
            # show_panel.show_table_grid.EnableEditing(True)
            # show_panel.show_table_grid.EnableGridLines(True)
            # # .show_table_grid.EnableDragGridSize(False)
            # show_panel.show_table_grid.SetMargins(0, 0)

            # Columns
            # show_panel.show_table_grid.EnableDragColMove(False)
            # show_panel.show_table_grid.EnableDragColSize(True)
            show_panel.show_table_grid.SetColLabelSize(30)
            show_panel.show_table_grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            show_panel.show_table_grid.SetColLabelValue(0, u"模型名称")
            show_panel.show_table_grid.SetColLabelValue(1, u"参数名称")
            show_panel.show_table_grid.SetColLabelValue(2, u"分布类型")
            show_panel.show_table_grid.SetColLabelValue(3, u"分布参数")
            show_panel.show_table_grid.SetColLabelValue(4, u"抽样方法")

            # Rows
            # show_panel.show_table_grid.EnableDragRowSize(True)
            show_panel.show_table_grid.SetRowLabelSize(80)
            show_panel.show_table_grid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

            # Label Appearance

            # Cell Defaults
            show_panel.show_table_grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

            """"设置内容"""
            i = 0
            self.method_default = []
            for row in record:
                show_panel.show_table_grid.SetCellValue(i, 0, str(row[0]))
                show_panel.show_table_grid.SetCellValue(i, 1, str(row[1]))
                show_panel.show_table_grid.SetCellValue(i, 2, str(row[2]))
                show_panel.show_table_grid.SetCellValue(i, 3, str(row[3]))
                # 按照分布方式对应的可选抽样方法设置下拉框
                show_panel.show_table_grid.SetCellEditor(i, 4, grid.GridCellChoiceEditor(SM.available_method[str(row[2])]))
                # 设置默认值为第一个选项
                show_panel.show_table_grid.SetCellValue(i, 4, SM.available_method[str(row[2])][0])
                i = i + 1
                # 记录默认选项 以便在抽样方法设置时 作为默认值插入抽样方法列表
                self.method_default.append(SM.available_method[str(row[2])][0])

            show_panel.gbSizer.Add(show_panel.show_table_grid, wx.GBPosition(1,0),
                             wx.GBSpan(1, 3), wx.ALL, 2)

            # 分割线
            # show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition,
            #                                       wx.DefaultSize, wx.LI_HORIZONTAL)
            # show_panel.sStaticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition,
            #                                        wx.DefaultSize, wx.LI_HORIZONTAL)

            # 上方提示信息Panel
            commonTag.setModeltag(show_panel, n_id)


            # show_panel.bSSizer.Add(show_panel.sStaticline, 0, wx.EXPAND | wx.ALL, 2)



            # 下方btmPanel
            show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition,
                                           (-1, 40), wx.TAB_TRAVERSAL)
            show_panel.confirmPanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
                                            (280, 28), wx.TAB_TRAVERSAL)

            show_panel.m_button = wx.Button(show_panel.confirmPanel, wx.ID_ANY, u"确定",
                                        (0, 0), (100, 28), 0)
            show_panel.m_button.Bind(wx.EVT_BUTTON, self.select_method_test)
            show_panel.cancel = wx.Button(show_panel.confirmPanel, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.Cancel, show_panel.cancel)

            # show_panel布局设置



            # show_panel.gbSizer.Add(show_panel.staticline, wx.GBPosition(26,0),
            #                  wx.GBSpan(1, 3), wx.ALL, 5)
            # show_panel.gbSizer.Add(show_panel.staticline, wx.GBPosition(26,0),
            #                  wx.GBSpan(1, 3), wx.ALL, 5)
            # # show_panel.bSizer.Add(scrollPanel, 0, wx.EXPAND | wx.ALL, 5)
            # show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND | wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)


            show_panel.gbSizer.Add(show_panel.bSizer, wx.GBPosition(2,0),
                             wx.GBSpan(2, 5), wx.EXPAND | wx.ALL, 5)
            # show_panel.gbSizer.Add(show_panel.btmPanel, wx.GBPosition(27,0),
                             # wx.GBSpan(1, 3), wx.ALL, 5)
            # show_panel.SetSizer(show_panel.bSizer)
            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()

            # 初始化confirmPanel位置
            x, y = show_panel.btmPanel.GetSize()
            w, h = show_panel.confirmPanel.GetSize()
            show_panel.confirmPanel.SetPosition((x - w - 25, y - h - 5))

            # show_panel.Bind(wx.EVT_SIZE,lambda evt, show_panel=show_panel: self.OnReSize(evt, show_panel))


    # 逐一输出选择的抽样方法
    def select_method_test(self, event):
        self.get_method()
        thisstep = self.GetCurrentPage().GetId()
        nextstep = self.GetCurrentPage().GetId() + 1
        while(self.GetCurrentPage().GetId() == thisstep):
            self.up_select_method(nextstep, 1)

    def get_method(self):
        self.method = []
        for i in range(0,self.tablelen):
            x = self.show_panel.show_table_grid.GetCellEditor(i, 4)
            if(x.Control != None): # 当选项框被选择时 选择选择的值 否则选择默认值
                method_append = x.GetValue()
            else:
                method_append = self.method_default[i]
            print(method_append)
            self.method.append(method_append)

    def up_select_method(self,n_id, flag = 0):
        # print(n_id)
        if(flag == 1):
            n_id /= 2

        """ 选择抽样方法 """
        pageId = n_id * 2
        flag = 0
        pageFocus = None
        for x in range(self.GetPageCount()):
            if pageId == self.GetPage(x).GetId():
                pageFocus = self.GetPage(x)
                print(pageId)
                flag = 1
                break

        if flag != 0:
            pageFocus.SetFocus()
            self.Refresh()
            self.Layout()
        else:
            self.select_method_panel = UPSelectMethodPanel.SelectSamplingMethodPanel(self, n_id)
            self.get_method()
            self.select_method_panel.set_up(self.Para, self.method)  # 在这里传入参数
           # n_id = self.navTree.GetItemData(self.navTree.GetSelection())  # 获取校准模型的id
            title = u"设置抽样数量"
            self.AddPage(self.select_method_panel, title, True, wx.NullBitmap)

    def up_test(self):
        """ 传播实验展示 """
        self.test_panel = UPShowPanel.TestPanel(self, para=self.Para ,id = self.Para.model_id)
        self.AddPage(self.test_panel, u"传播分析", True, wx.NullBitmap)

    # 关闭
    def Cancel(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()