# -*- coding: utf-8 -*-

import wx
import NavTree
import ShowNotebook


# 系统管理Panel
class SystemManegePanel(wx.Panel):
    
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()
    
    def InitUI(self):
        # 上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)
        
        self.button_operation = wx.Button(self.btnPanel, wx.ID_ANY, u"操作说明",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_operation.SetBitmap(wx.Bitmap('icon/arg.ico'))
        tabSizer.Add(self.button_operation, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.onClickOperation, self.button_operation)

        self.button_copyright = wx.Button(self.btnPanel, wx.ID_ANY, u"版权说明",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_copyright.SetBitmap(wx.Bitmap('icon/arg.ico'))
        tabSizer.Add(self.button_copyright, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.onClickCopyright, self.button_copyright)
        
        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        
        # displayPanel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
    
    def onClickOperation(self, event):
        if self.navTree.GetSelection().IsOk() == True:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())
            if n_id != 0:
                self.showNotebook.operationManuDis(n_id)
                return
        dlg = wx.MessageBox("请先选择一个模型", "提示" ,wx.OK | wx.ICON_INFORMATION)
    
    def onClickCopyright(self, event):
        if self.navTree.GetSelection().IsOk() == True:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())
            if n_id != 0:
                self.showNotebook.copyrightManuDis(n_id)
                return
        dlg = wx.MessageBox("请先选择一个模型", "提示" ,wx.OK | wx.ICON_INFORMATION)



