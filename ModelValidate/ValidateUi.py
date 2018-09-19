# -*- coding: utf-8 -*-

import wx
import NavTree
import ShowNotebook

#模型管理功能模块界面
class ValidatePanel(wx.Panel):
    
    def __init__(self, parent = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()
        
    def InitUI(self):
        #上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)
        
        # self.button_ImportData = wx.Button(self.btnPanel, wx.ID_ANY, u"查看数据",
        #                                    wx.DefaultPosition, wx.DefaultSize, 0)
        # # self.button_ImportData.Disable()
        # self.button_ImportData.SetBitmap(wx.Bitmap('icon/data.ico'))
        # self.Bind(wx.EVT_BUTTON, self.ClickImportData, self.button_ImportData)
        # tabSizer.Add(self.button_ImportData, 0, wx.ALL, 5)

        self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"仿真验证",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button3.SetBitmap(wx.Bitmap('icon/validate.ico'))
        self.button3.Bind(wx.EVT_LEFT_DOWN, self. DefaultPosition)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)



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
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(hBoxSizer)
        
        #整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
#         self.Layout()
#         vBoxSizer.Fit(self)


    def ClickImport(self, event):
        self.showNotebook.NewProj0()

#         dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)  
#         if dlg.ShowModal() == wx.ID_OK:
#             Import_file.insert_blob(project='一元非线性回归', _dir=dlg.GetPath()) #文件夹路径  
#         dlg.Destroy()

#             self.navTree.updateTree()
#         dlg.Destroy()
    def DefaultPosition(self, event):
        #选择仿真验证
        self.showNotebook.NewProj2()

    # def ClickParaSetup(self, event):
    #     self.showNotebook.NewProj1()

    def ClickModelSelect(self, event):   #模型选择
        global n_id
        try:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())  # 获取校准模型的id
            if n_id == 0:
                raise NameError('...')
            global sym0
            sym0 = 1
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()
        self.button_ImportData.Enable()

    def ClickModel(self):  # 模型选择
        global n_id
        try:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())  # 获取校准模型的id
            if n_id == 0:
                raise NameError('...')
            global sym0
            sym0 = 1
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()
        self.button_ImportData.Enable()

    def ClickImportData(self, event):    #数据导入
        self.ClickModel()
        self.showNotebook.ImportDataPanel()
        self.showNotebook.onClick_button_import()
        print n_id
        # self.button3.Enable()
       # self.button2.Enable()