# -*- coding: utf-8 -*-

import wx
from wx import aui
from wx import grid

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                aui.AUI_NB_DEFAULT_STYLE)
        self.m_panel19 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        
        self.AddPage(self.m_panel19, u"UncertaintyModeling", False, wx.NullBitmap)
#         bSizer17 = wx.BoxSizer(wx.VERTICAL)
# 
#         self.m_auinotebook1.AddPage(self.m_panel19, u"UncertaintyModeling", False, wx.NullBitmap)
#         self.m_auinotebook1.DeletePage(self.m_auinotebook1.GetPageIndex(self.m_panel19))
# 
#         self.m_panel20 = wx.Panel(self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         bSizer18 = wx.BoxSizer(wx.VERTICAL)
# 
#         self.m_grid10 = grid.Grid(self.m_panel20, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
