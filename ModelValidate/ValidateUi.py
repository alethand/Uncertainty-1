# -*- coding: utf-8 -*-

import wx
import NavTree
import ShowNotebook
import ValidateBuildMetaModel as build_meta
import ProcessBar as pb

# 记录最新选择的模型信息
n_id = -1
model_d = 0
real_d = 0


# 模型验证的主界面
# 包含上方按钮
class ValidatePanel(wx.Panel):

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()

    # 初始化UI布局
    def InitUI(self):
        # 上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        self.btn_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(self.btn_panel_sizer)

        self.button_import_data = wx.Button(self.btnPanel, wx.ID_ANY, u"导入数据",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_import_data.Bind(wx.EVT_LEFT_DOWN, self.Import)

        self.button_valid = wx.Button(self.btnPanel, wx.ID_ANY, u"仿真验证",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_valid.SetBitmap(wx.Bitmap('icon/validate.ico'))
        self.button_valid.Bind(wx.EVT_LEFT_DOWN, self.Validation)
        self.btn_panel_sizer.Add(self.button_import_data, 0, wx.ALL, 5)
        self.btn_panel_sizer.Add(self.button_valid, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        """双击选择模型"""
        self.navTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.ClickModelSelect)
        """右键选择模型"""
        # self.navTree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.ClickModelSelect)
        """"""""""""""""""""
        # displayPanel布局
        display_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # 1，4 代表比列
        display_panel_sizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        display_panel_sizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(display_panel_sizer)

        # 整个模块布局
        valid_ui_sizer = wx.BoxSizer(wx.VERTICAL)
        valid_ui_sizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        valid_ui_sizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(valid_ui_sizer)

    # 选择仿真验证
    def Validation(self, event):
        self.showNotebook.start_validation()

    # 模型选择
    def ClickModelSelect(self, event):
        # 获取校准模型的数据库id
        global n_id

        if n_id != -1:
            dlg = wx.MessageDialog(None, message='您正在验证一个模型，验证结束后打开新模型', caption='提示')
            dlg.ShowModal()
            return
        else:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())
    # 提示先选择模型再进行操作
    def Import(self, event):
        if n_id == -1:
            dlg = wx.MessageDialog(None, message='请先在左下方导航树先双击选择一个仿真模型', caption='提示')
            dlg.ShowModal()
            return
        else:
            # 增加一个对话框
            dlg = MyDialog(self)
            dlg.ShowModal()


# 用来进行导入数据的对话框
class MyDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(339, 159), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.text_white = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_white.Wrap(-1)

        bSizer1.Add(self.text_white, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_white = wx.StaticText(self, wx.ID_ANY, u"选择导入仿真模型数据或者元模型数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_white.Wrap(-1)

        self.text_white.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "宋体"))

        bSizer1.Add(self.text_white, 2, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.text_white = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_white.Wrap(-1)

        bSizer2.Add(self.text_white, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.model_import = wx.Button(self, wx.ID_ANY, u"仿真模型数据导入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.model_import, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.text_white = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_white.Wrap(-1)

        bSizer2.Add(self.text_white, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.meta_import = wx.Button(self, wx.ID_ANY, u"元模型数据导入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.meta_import, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.text_white = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_white.Wrap(-1)

        bSizer2.Add(self.text_white, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer2, 3, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.model_import.Bind(wx.EVT_BUTTON, self.import_model_data)
        self.meta_import.Bind(wx.EVT_BUTTON, self.import_meta_data)

        # Virtual event handlers, overide them in your derived class

    # 先关闭对话框，然后开始导入数据，期间等待的时候要有进度条
    def import_model_data(self, event):
        self.Close()
        global model_d, real_d

        xpb = pb.ProcessBar(None, '请稍等', 100)
        res = xpb.loadFunction("导入数据完成", build_meta.import_model_data, n_id)
        model_d, real_d = res[0], res[1]

        print 'model_d shape:{} real_d_shape:{}'.format(model_d.shape,real_d.shape)
        # 调用ValidatePanel的showNotebook的函数
        self.GetParent().showNotebook.end_import_data()

    def import_meta_data(self, event):
        """ToDO"""
        self.Close()
        dlg = wx.MessageDialog(None, message='暂时还未实现', caption='提示')
        dlg.ShowModal()
