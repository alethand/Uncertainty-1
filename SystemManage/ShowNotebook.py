# -*- coding: utf-8 -*-

import wx
from wx import aui
import Sql


class ShowNotebook(aui.AuiNotebook):
    # 用于存储ParaSettingWindow中设置的信息
    para_info = 'para_info'
    
    def __init__(self, parent=None):
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
    
    def operationManuDis(self, pProj=0):
        """ 展示操作说明 """
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
        title = u"操作说明" + u'（模型：' + modelinfo[0][0] + ')'
        self.AddPage(self.show_panel, title, True, wx.NullBitmap)
        show_panel = self.show_panel
        show_panel.pid = pProj
        show_panel.params = Sql.selectSql((pProj,), Sql.selectParams)
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
        # show_panel布局设置
        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(show_panel.bSizer)
        show_panel.Layout()
        
        show_panel.Bind(wx.EVT_SIZE,
                        lambda evt, show_panel=show_panel: self.OnReSize(evt, show_panel))
    
    def copyrightManuDis(self, pProj=0):
        """ 展示版权说明 """
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
        title = u"版权说明" + u'（模型：' + modelinfo[0][0] + ')'
        self.AddPage(self.show_panel, title, True, wx.NullBitmap)
        show_panel = self.show_panel
        show_panel.pid = pProj
        show_panel.params = Sql.selectSql((pProj,), Sql.selectParams)
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
        # show_panel布局设置
        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(show_panel.bSizer)
        show_panel.Layout()
        
        show_panel.Bind(wx.EVT_SIZE,
                        lambda evt, show_panel=show_panel: self.OnReSize(evt, show_panel))
    
    def OnReSize(self, event, show_panel):
        show_panel.Layout()
        #         在绑定的size事件中使右下角保存panel右对齐
        x, y = show_panel.btmPanel.GetSize()
        w, h = show_panel.savePanel.GetSize()
        show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
        show_panel.Layout()

#     def OnReSize(self, event):
#         show_panel = self.GetCurrentPage()
#         show_panel.Layout()
# #         在绑定的size事件中使右下角保存panel右对齐
#         x, y = show_panel.btmPanel.GetSize()
#         w, h = show_panel.savePanel.GetSize()
#         for i in range(self.PageCount):
#             show_panel = self.GetPage(i)
#             show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
#             show_panel.Layout()


