# -*- coding: utf-8 -*-
from __future__ import division

import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled
import wx.lib.newevent
from wx import aui
import ValidateUi as cp
import MetaPanel
import DataPanel

class ShowNotebook(aui.AuiNotebook):
    def __init__(self, parent=None):
        self.parent = parent
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    #点击模型验证后会发生的事情
    def start_validation(self):

        # 如果没有选择模型，则提示并退出
        if cp.n_id==-1:
            dlg = wx.MessageDialog(None, message='请在左下方导航树先双击选择一个仿真模型', caption='提示')
            dlg.ShowModal()
            return

        self.valid_panel = MetaPanel.MetaPanel(self, cp.n_id)
        title = u"仿真验证"
        self.AddPage(self.valid_panel, title, True, wx.NullBitmap)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.on_close)

        self.Refresh()

    #点击导入数据后会发生的事情
    def end_import_data(self):
        self.data_panel = DataPanel.DataPanel(self, cp.n_id)
        title = u"数据概览"
        self.AddPage(self.data_panel, title, True, wx.NullBitmap)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.on_close)

        self.Refresh()

    # 关闭的时候取消验证页面对模型的记录信息
    def on_close(self,event):
        if self.GetPageCount()==0 :
            cp.n_id=-1
            cp.model_d=0
            cp.real_d=0
        else:
            pass







