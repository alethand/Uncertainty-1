# -*- coding: utf-8 -*-

from __future__ import division

import time
import wx
import NavTree
import ShowNotebook
import ProcessBar as pb


n_id = 0
sym0 = 0
sym1 = 0
sym2 = 0
class CalibrationPanel(wx.Panel):

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()

    def InitUI(self):
        # 上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)

        # self.button_ImportData = wx.Button(self.btnPanel, wx.ID_ANY, u"查看数据",
        #                         wx.DefaultPosition, wx.DefaultSize, 0)
        # self.button_ImportData.SetBitmap(wx.Bitmap('icon/data.ico'))
        # self.Bind(wx.EVT_BUTTON, self.ClickImportData, self.button_ImportData)

        self.button2 = wx.Button(self.btnPanel, wx.ID_ANY, u"元模型建模",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button2.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickSetup, self.button2)

        self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"优化模型",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.button3.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickOptSetup, self.button3)


        # tabSizer.Add(self.button1, 0, wx.ALL, 5)
#        tabSizer.Add(self.button_ImportData, 0, wx.ALL, 5)
        tabSizer.Add(self.button2, 0, wx.ALL, 5)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        """双击选择模型"""
        self.navTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ClickModelSelect)
        """右键选择模型"""
        self.navTree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.ClickModelSelect)
        """"""""""""""""""""
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

    def ClickModelSelect(self, event):
        global n_id
        try:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())  #获取校准模型的id
            if n_id==0:
                raise NameError('...')
            # dlg = wx.MessageDialog(None, message='你选择了模型的id是%d'%(n_id))
            # dlg.ShowModal()
            global sym0
            sym0 = 1
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()

    def ClickSelect(self):
        global n_id
        try:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())  #获取校准模型的id
            if n_id==0:
                raise NameError('...')
            # dlg = wx.MessageDialog(None, message='你选择了模型的id是%d'%(n_id))
            # dlg.ShowModal()
            global sym0
            sym0 = 1
            return True
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()
            return False

    # def ClickImportData(self, event):
    #     # 第一次点击
    #     if(self.showNotebook.GetCurrentPage() == None):
    #         self.ClickSelect()
    #         self.showNotebook.ImportDataPanel_NEW()
    #         self.showNotebook.onClick_button_import()
    #     else:
    #         thisid = self.navTree.GetItemData(self.navTree.GetSelection())
            
    #         # 确保一次点击能成功跳转
    #         thisstep = self.showNotebook.GetCurrentPage().GetId()
    #         # 是奇数的时候跳转到相应偶数 否则就是在当前页不执行任何跳转操作 可防止在当前页点按钮导致死循环 
    #         if((thisstep % 2) != 0):
    #             while(self.showNotebook.GetCurrentPage().GetId() == thisstep):
    #                 self.ClickSelect()
    #                 self.showNotebook.ImportDataPanel_NEW()
    #                 self.showNotebook.onClick_button_import()
            

    def ClickSetup(self, event):
        # 第一次点击
        if(self.showNotebook.GetCurrentPage() == None):
           if(self.ClickSelect()):
                self.loadPage(self.showNotebook.BuildMetaPanel_NEW)

        else:
            thisid = self.navTree.GetItemData(self.navTree.GetSelection())
            
            # 确保一次点击能成功跳转
            thisstep = self.showNotebook.GetCurrentPage().GetId()
            # 是偶数的时候跳转到相应奇数 否则就是在当前页不执行任何跳转操作 可防止在当前页点按钮导致死循环 
            if((thisstep % 2) != 1):
                while(self.showNotebook.GetCurrentPage().GetId() == thisstep):
                    if(self.ClickSelect()):
                        self.loadPage(self.showNotebook.BuildMetaPanel_NEW)

    def ClickOptSetup(self, event):
        # 第一次点击
        if(self.showNotebook.GetCurrentPage() == None):
            if(self.ClickSelect()):
                self.loadPage(self.showNotebook.OptPanel_NEW)
        else:
            thisid = self.navTree.GetItemData(self.navTree.GetSelection())
            
            # 确保一次点击能成功跳转
            thisstep = self.showNotebook.GetCurrentPage().GetId()
            # 是奇数的时候跳转到相应偶数 否则就是在当前页不执行任何跳转操作 可防止在当前页点按钮导致死循环 
            if((thisstep % 2) != 0):
                while(self.showNotebook.GetCurrentPage().GetId() == thisstep):
                    if(self.ClickSelect()):
                        self.loadPage(self.showNotebook.OptPanel_NEW)

    def loadPage(self,pagInit):
        self.xpb = pb.ProcessBar(None, '数据导入中', 1000)
        self.xpb.loadFunction(pagInit,'数据导入已经完成！')
