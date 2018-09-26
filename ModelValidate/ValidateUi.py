# -*- coding: utf-8 -*-

import wx
import NavTree
import ShowNotebook

# 记录最新选择的模型信息
n_id = -1

# 模型验证的主界面
class ValidatePanel(wx.Panel):

    def __init__(self, parent = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()

    # 初始化UI布局
    def InitUI(self):
        #上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        self.btn_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(self.btn_panel_sizer)


        self.button = wx.Button(self.btnPanel, wx.ID_ANY, u"仿真验证",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button.SetBitmap(wx.Bitmap('icon/validate.ico'))
        self.button.Bind(wx.EVT_LEFT_DOWN, self.Validation)
        self.btn_panel_sizer.Add(self.button, 0, wx.ALL, 5)



        #下方导航树及展示界面panel 
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        """双击选择模型"""
        self.navTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ClickModelSelect)
        """右键选择模型"""
        self.navTree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.ClickModelSelect)
        """"""""""""""""""""
        #displayPanel布局
        display_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # 1，4 代表比列
        display_panel_sizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        display_panel_sizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(display_panel_sizer)
        
        #整个模块布局
        valid_ui_sizer = wx.BoxSizer(wx.VERTICAL)
        valid_ui_sizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        valid_ui_sizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(valid_ui_sizer)

    #选择仿真验证
    def Validation(self, event):
        self.showNotebook.start_validation()

    # 模型选择
    def ClickModelSelect(self, event):
        # 获取校准模型的数据库id
        global n_id

        if n_id!=-1 :
            dlg = wx.MessageDialog(None, message='您正在验证一个模型，验证结束后打开新模型', caption='提示')
            dlg.ShowModal()
            return
        else:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())
            # dlg = wx.MessageDialog(None, message='模型：%s' % n_id , caption='提示')
            # dlg.ShowModal()
            # return