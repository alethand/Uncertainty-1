# -*- coding: utf-8 -*-

import wx
import Sql


def setModeltag(show_panel, n_id):
    show_panel.bSSizer = wx.BoxSizer(wx.VERTICAL)
    modelinfo = Sql.selectSql(args=(n_id,), sql=Sql.selectModel)
    show_panel.tagPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition,
                                   (-1, 20), wx.TAB_TRAVERSAL)
    static_text = wx.StaticText(show_panel.tagPanel, wx.ID_ANY, u'当前模型：', (0, 0), wx.DefaultSize, 0)
    static_text1 = wx.StaticText(show_panel.tagPanel, wx.ID_ANY, modelinfo[0][0], (80, 0), wx.DefaultSize, 0)
    static_text.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))
    show_panel.bSSizer.Add(show_panel.tagPanel, 0, wx.EXPAND | wx.ALL, 2)
    show_panel.gbSizer.Add(show_panel.bSSizer, wx.GBPosition(0, 0),
                           wx.GBSpan(1, 5), wx.EXPAND | wx.ALL, 0)