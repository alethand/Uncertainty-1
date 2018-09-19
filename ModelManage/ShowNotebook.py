#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import aui
import Import_file
import Run
import Sql
import sys
from wx.lib.mixins.listctrl import TextEditMixin
import config


class ShowNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def RunModel(self, id):
        flag = 0
        for x in range(self.GetPageCount()):
            if 3 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                return
        if flag == 0:
            # 生成panel

            # 判断本地是否有该模型存在
            sys_path = Run.get_dir(id, '')
            if sys_path in sys.path:
                sys.path.remove(sys_path)  # 使当前模型路径为系统环境变量
            sys.path.insert(0, sys_path)
            if sys.modules.has_key(config.main_file):
                del sys.modules[config.main_file]
            try:
                __import__(config.main_file)
            except ImportError:
                Run.read_blob(id)

            """从数据库读取数据"""
            modelinfo = Sql.selectSql(args=(id,), sql=Sql.selectModel)
            inputparams = Sql.selectSql(args=(id,), sql=Sql.selectModelArgs)
            outparams = Sql.selectSql(args=(id,), sql=Sql.selectModelOutputArgs)
            vars = Sql.selectSql(args=(id,), sql=Sql.selectModelVars)

            self.show_panel3 = wx.Panel(self, 3, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            """新旧id"""
            self.show_panel3.old_id = id
            self.show_panel3.new_id = -1

            self.AddPage(self.show_panel3, u"仿真运行", True, wx.NullBitmap)
            show_panel = self.show_panel3
            show_panel.pid = modelinfo[0][2]
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

            show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型名称：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, -1), 0)
            show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5),
                                   wx.GBSpan(1, 3), wx.ALL, 5)
            show_panel.textCtrl1.WriteText(modelinfo[0][0])

            show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此模型名称已存在",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.staticText3.SetForegroundColour('red')
            show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.staticText3.Show(show=False)

            show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型描述：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, 100), wx.TE_MULTILINE | wx.TE_RICH)
            show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5),
                                   wx.GBSpan(3, 5), wx.ALL, 5)
            show_panel.textCtrl2.WriteText(modelinfo[0][1])

            show_panel.model_select = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型文件：",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.model_select, wx.GBPosition(6, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.dir_text = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.Size(480, -1), 0)
            show_panel.gbSizer.Add(show_panel.dir_text, wx.GBPosition(6, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.dir_text.WriteText('model_' + str(id))

            scrollPanel = show_panel.scrolledWindow
            show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数个数：", wx.DefaultPosition, wx.DefaultSize, 0)

            show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.var_num = wx.StaticText(scrollPanel, wx.ID_ANY, str(len(inputparams)),
                                               wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.var_num, wx.GBPosition(7, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数设置：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(8, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.inputform = EditMixin(scrollPanel)
            show_panel.inputform.InsertColumn(0, '变量名', width=160)
            show_panel.inputform.InsertColumn(1, '描述', width=160)
            show_panel.inputform.InsertColumn(2, '初始值', width=160)
            show_panel.inputform.InsertColumn(3, 'arg_id', width=0)
            for i in inputparams:
                index = show_panel.inputform.InsertItem(sys.maxint, i[0])
                show_panel.inputform.SetItem(index, 1, i[1])
                show_panel.inputform.SetItem(index, 2, str(i[2]))
                show_panel.inputform.SetItem(index, 3, str(i[3]))
            # show_panel.inputform.make_editor()
            show_panel.inputform.Disable()
            show_panel.gbSizer.Add(show_panel.inputform, wx.GBPosition(8, 5), wx.GBSpan(5, 7), wx.ALL, 5)

            show_panel.staticText6 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"变量设置：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText6, wx.GBPosition(13, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            """变量表"""
            show_panel.varsform = EditMixin(scrollPanel)
            show_panel.varsform.InsertColumn(0, '变量名', width=160)
            show_panel.varsform.InsertColumn(1, '描述', width=160)
            show_panel.varsform.InsertColumn(2, '初始值', width=160)
            show_panel.varsform.InsertColumn(3, 'arg_type', width=0)
            show_panel.varsform.InsertColumn(4, 'arg_id', width=0)
            for i in vars:
                index = show_panel.varsform.InsertItem(sys.maxint, i[0])
                show_panel.varsform.SetItem(index, 1, i[1])
                show_panel.varsform.SetItem(index, 2, str(i[2]))
                show_panel.varsform.SetItem(index, 3, str(i[3]))
                show_panel.varsform.SetItem(index, 4, str(i[4]))
            # show_panel.varsform.make_editor()
            # show_panel.inputform.GetItemText()
            show_panel.varsform.Disable()
            show_panel.gbSizer.Add(show_panel.varsform, wx.GBPosition(13, 5), wx.GBSpan(5, 7), wx.ALL, 5)

            show_panel.staticText7 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"输出参数：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText7, wx.GBPosition(18, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.outputform = EditMixin(scrollPanel)
            show_panel.outputform.InsertColumn(0, '变量名', width=160)
            show_panel.outputform.InsertColumn(1, '描述', width=160)
            show_panel.outputform.InsertColumn(2, 'op_id', width=0)
            show_panel.outputform.InsertColumn(3, '运行结果', width=160)
            for i in outparams:
                index = show_panel.outputform.InsertItem(sys.maxint, i[0])
                show_panel.outputform.SetItem(index, 1, i[1])
                show_panel.outputform.SetItem(index, 2, str(i[2]))
            # show_panel.outputform.make_editor()
            show_panel.outputform.Disable()

            show_panel.gbSizer.Add(show_panel.outputform, wx.GBPosition(18, 5), wx.GBSpan(5, 2),
                                   wx.ALL, 5)

            
            #分割线
            show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                                  wx.DefaultSize, wx.LI_HORIZONTAL)
            
            # 下方btmPanel
            show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                           (-1, 40), wx.TAB_TRAVERSAL)
            show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
                                      (280, 28), wx.TAB_TRAVERSAL)
            show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"运行",
                                        (0, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.TryRun, show_panel.save)
            show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.Cancel, show_panel.cancel)
 
            #show_panel布局设置
            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()
            show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
            show_panel.SetSizer(show_panel.bSizer)
            show_panel.Layout()
            
            #初始化savePanel位置
            x, y = show_panel.btmPanel.GetSize()
            w, h = show_panel.savePanel.GetSize()
            show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))

            show_panel.Bind(wx.EVT_SIZE, 
                lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))

    def UpdateModel(self, id):
        flag = 0
        for x in range(self.GetPageCount()):
            if 2 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                break
        if flag == 0:
            # 生成panel
            #判断本地是否有该模型存在
            sys_path = Run.get_dir(id, '')
            if sys_path in sys.path:
                sys.path.remove(sys_path)  # 使当前模型路径为系统环境变量
            sys.path.insert(0, sys_path)
            if sys.modules.has_key(config.main_file):
                del sys.modules[config.main_file]
            try:
                __import__(config.main_file)
            except ImportError:
                Run.read_blob(id)

            """从数据库读取数据"""
            modelinfo = Sql.selectSql(args=(id,), sql=Sql.selectModel)
            inputparams = Sql.selectSql(args=(id,), sql=Sql.selectModelArgs)
            outparams = Sql.selectSql(args=(id,), sql=Sql.selectModelOutputArgs)
            vars = Sql.selectSql(args=(id,), sql=Sql.selectModelVars)

            self.show_panel2 = wx.Panel(self, 2, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            """新旧id"""
            self.show_panel2.old_id = id
            self.show_panel2.new_id = -1

            self.AddPage(self.show_panel2, u"模型修改", True, wx.NullBitmap)
            show_panel = self.show_panel2
            show_panel.pid = modelinfo[0][2]
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

            show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型名称：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, -1), 0)
            show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5),
                                   wx.GBSpan(1, 3), wx.ALL, 5)
            show_panel.textCtrl1.WriteText(modelinfo[0][0])

            show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此模型名称已存在",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.staticText3.SetForegroundColour('red')
            show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.staticText3.Show(show=False)

            show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型描述：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, 100), wx.TE_MULTILINE | wx.TE_RICH)
            show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5),
                                   wx.GBSpan(3, 5), wx.ALL, 5)
            show_panel.textCtrl2.WriteText(modelinfo[0][1] 
                                           if modelinfo[0][1] != None else '')

            show_panel.model_select = wx.StaticText(scrollPanel, wx.ID_ANY, u"选择模型：",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.model_select, wx.GBPosition(6, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.dir_text = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.Size(380, 28), 0)
            show_panel.gbSizer.Add(show_panel.dir_text, wx.GBPosition(6, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.dir_text.WriteText('model_' + str(id))

            # show_panel.button1 = wx.Button(scrollPanel, wx.ID_ANY, u"导出模型",
            #                                wx.DefaultPosition, wx.DefaultSize, 0)
            # self.Bind(wx.EVT_BUTTON, self.ClickExport, show_panel.button1)
            # show_panel.gbSizer.Add(show_panel.button1, wx.GBPosition(6, 6),
            #                        wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.imp_button = wx.Button(scrollPanel, wx.ID_ANY, u"导入模型",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
            self.Bind(wx.EVT_BUTTON, self.ClickImport2, show_panel.imp_button)
            show_panel.gbSizer.Add(show_panel.imp_button, wx.GBPosition(6, 6),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            # Run.read_blob(id)
            # params = Run.read_param(id)

            show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数个数：", wx.DefaultPosition, wx.DefaultSize, 0)

            show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.var_num = wx.StaticText(scrollPanel, wx.ID_ANY, str(len(inputparams)),
                                               wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.var_num, wx.GBPosition(7, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数设置：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(8, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.inputform = EditMixin(scrollPanel)
            show_panel.inputform.InsertColumn(0, '变量名', width=160)
            show_panel.inputform.InsertColumn(1, '描述', width=160)
            show_panel.inputform.InsertColumn(2, '初始值', width=160)
            show_panel.inputform.InsertColumn(3, 'arg_id', width=0)
            for i in inputparams:
                index = show_panel.inputform.InsertItem(sys.maxint, i[0])
                show_panel.inputform.SetItem(index, 1, i[1])
                show_panel.inputform.SetItem(index, 2, str(i[2]))
                show_panel.inputform.SetItem(index, 3, str(i[3]))
            show_panel.inputform.make_editor()
            show_panel.gbSizer.Add(show_panel.inputform, wx.GBPosition(8, 5), wx.GBSpan(5, 7), wx.ALL, 5)

            show_panel.staticText6 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"变量设置：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText6, wx.GBPosition(13, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            """变量表"""
            show_panel.varsform = EditMixin(scrollPanel)
            show_panel.varsform.InsertColumn(0, '变量名', width=160)
            show_panel.varsform.InsertColumn(1, '描述', width=160)
            show_panel.varsform.InsertColumn(2, '初始值', width=160)
            show_panel.varsform.InsertColumn(3, 'arg_type', width=0)
            show_panel.varsform.InsertColumn(4, 'arg_id', width=0)
            for i in vars:
                index = show_panel.varsform.InsertItem(sys.maxint, i[0])
                show_panel.varsform.SetItem(index, 1, i[1])
                show_panel.varsform.SetItem(index, 2, str(i[2]))
                show_panel.varsform.SetItem(index, 3, str(i[3]))
                show_panel.varsform.SetItem(index, 4, str(i[4]))
            show_panel.varsform.make_editor()
            # show_panel.inputform.GetItemText()
            show_panel.gbSizer.Add(show_panel.varsform, wx.GBPosition(13, 5), wx.GBSpan(5, 7), wx.ALL, 5)

            show_panel.staticText7 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"输出参数：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText7, wx.GBPosition(18, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.outputform = EditMixin(scrollPanel)
            show_panel.outputform.InsertColumn(0, '变量名', width=240)
            show_panel.outputform.InsertColumn(1, '描述', width=240)
            show_panel.outputform.InsertColumn(2, 'op_id', width=0)
            for i in outparams:
                index = show_panel.outputform.InsertItem(sys.maxint, i[0])
                show_panel.outputform.SetItem(index, 1, i[1] if i[1] != None else '')
                show_panel.outputform.SetItem(index, 2, str(i[2]))
            show_panel.outputform.make_editor()

            show_panel.gbSizer.Add(show_panel.outputform, wx.GBPosition(18, 5), wx.GBSpan(5, 7),
                                   wx.ALL, 5)
            
            #分割线
            show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                                  wx.DefaultSize, wx.LI_HORIZONTAL)
             
            # 下方btmPanel
            show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                           (-1, 40), wx.TAB_TRAVERSAL)
            show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
                                      (280, 28), wx.TAB_TRAVERSAL)
            show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"保存",
                                        (0, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.SaveUpdate, show_panel.save)
            show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.Cancel, show_panel.cancel)
  
            #show_panel布局设置
            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()
            show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
            show_panel.SetSizer(show_panel.bSizer)
            show_panel.Layout()
             
            #初始化savePanel位置
            x, y = show_panel.btmPanel.GetSize()
            w, h = show_panel.savePanel.GetSize()
            show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
 
            show_panel.Bind(wx.EVT_SIZE, 
                lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))
            
    def clearControl(self, show_panel):
        if hasattr(show_panel, 'staticText4'):
            show_panel.staticText4.Destroy()
        if hasattr(show_panel, 'var_num'):
            show_panel.var_num.Destroy()
        if hasattr(show_panel, 'staticText5'):
            show_panel.staticText5.Destroy()
        if hasattr(show_panel, 'inputform'):
            show_panel.inputform.Destroy()
        if hasattr(show_panel, 'staticText6'):
            show_panel.staticText6.Destroy()
        if hasattr(show_panel, 'varsform'):
            show_panel.varsform.Destroy()
        if hasattr(show_panel, 'staticText7'):
            show_panel.staticText7.Destroy()
        if hasattr(show_panel, 'outputform'):
            show_panel.outputform.Destroy()
        if hasattr(show_panel, 'output_num'):
            show_panel.output_num.Destroy()
        if hasattr(show_panel, 'output_var'):
            show_panel.output_var.Destroy()
        return
    
    # 点击导出模型事件(修改界面)
    def ClickExport(self, event):
        show_panel = self.GetCurrentPage()
        self.clearControl(show_panel)
        show_panel.dir_text.Disable()
        show_panel.button1.Disable()
        show_panel.new_id = show_panel.old_id
        self.genInParams(show_panel.old_id, show_panel)
    
    # 点击导入模型事件(修改界面)
    def ClickImport2(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        proj_descr = show_panel.textCtrl2.GetValue()
        if proj_name == '':
            return
        # record = Sql.selectSql((proj_name, show_panel.pid), Sql.selectProj)
        # if record != []:
        #     show_panel.staticText3.Show(show=True)
        #     show_panel.Layout()
        #     return
        show_panel.staticText3.Show(show=False)
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            Sql.deleteSql(args=(show_panel.old_id,), sql=Sql.deleteFile)
            """重新导入模型，新id变化"""
            show_panel.new_id = Import_file.insert_blob(proj_name, show_panel.pid,
                                proj_descr, dlg.GetPath(), show_panel.old_id)
            show_panel.dir_text.SetValue(dlg.GetPath())
            show_panel.dir_text.Disable()
            show_panel.button1.Disable()
            self.clearControl(show_panel)
            self.genInParams(show_panel.new_id, show_panel)
        dlg.Destroy()

    def NewProj(self, pProj=0):
        flag = 0
        for x in range(self.GetPageCount()):
            if 1 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                break
        if flag == 0:
            self.show_panel = wx.Panel(self, 1, wx.DefaultPosition,
                                       wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.AddPage(self.show_panel, u"新建模型", True, wx.NullBitmap)
            self.show_panel.model_id = -1
            show_panel = self.show_panel
            show_panel.pid = pProj
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

            show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型名称：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, -1), 0)
            show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5),
                                   wx.GBSpan(1, 3), wx.ALL, 5)

            show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此模型名称已存在",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.staticText3.SetForegroundColour('red')
            show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.staticText3.Show(show=False)

            show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型描述：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, 100), wx.TE_MULTILINE | wx.TE_RICH)
            show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5),
                                   wx.GBSpan(3, 5), wx.ALL, 5)

            show_panel.model_select = wx.StaticText(scrollPanel, wx.ID_ANY, u"选择模型：",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.model_select, wx.GBPosition(6, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.dir_text = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.Size(380, -1), 0)
            show_panel.gbSizer.Add(show_panel.dir_text, wx.GBPosition(6, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.button1 = wx.Button(scrollPanel, wx.ID_ANY, u"导入模型",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
            self.Bind(wx.EVT_BUTTON, self.ClickImport, show_panel.button1)
            show_panel.gbSizer.Add(show_panel.button1, wx.GBPosition(6, 6),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            
            #分割线
            show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                                  wx.DefaultSize, wx.LI_HORIZONTAL)
            
            # 下方btmPanel
            show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                           (-1, 40), wx.TAB_TRAVERSAL)
            show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
                                      (280, 28), wx.TAB_TRAVERSAL)
            show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"保存",
                                        (0, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.SaveNew, show_panel.save)
            show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            self.Bind(wx.EVT_BUTTON, self.Cancel, show_panel.cancel)
 
            #show_panel布局设置
            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()
            show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
            show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
            show_panel.SetSizer(show_panel.bSizer)
            show_panel.Layout()
            
            #初始化savePanel位置
            x, y = show_panel.btmPanel.GetSize()
            w, h = show_panel.savePanel.GetSize()
            show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))

            show_panel.Bind(wx.EVT_SIZE, 
                lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))

    def OnReSize(self, event, show_panel):
        show_panel.Layout()
#         在绑定的size事件中使右下角保存panel右对齐
        x, y = show_panel.btmPanel.GetSize()
        w, h = show_panel.savePanel.GetSize()
        show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
        show_panel.Layout()

    # 点击导入模型事件
    def ClickImport(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        if proj_name == '':
            return
        proj_descr = show_panel.textCtrl2.GetValue()
        record = Sql.selectSql((proj_name, show_panel.pid), Sql.selectProj)
        if record != []:
            show_panel.staticText3.Show(show=True)
            show_panel.Layout()
            return
        show_panel.staticText3.Show(show=False)
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            proj = Import_file.insert_blob(proj_name, show_panel.pid,
                                           proj_descr, dlg.GetPath())
            show_panel.dir_text.SetValue(dlg.GetPath())
            show_panel.dir_text.Disable()
            show_panel.textCtrl1.Disable()  # 导入成功后控件变为不可编辑
            show_panel.textCtrl2.Disable()
            show_panel.button1.Disable()
            self.GetParent().GetParent().navTree.updateTree()
            self.genInParams(proj, show_panel)
        dlg.Destroy()

    # 导入成功后生成输入参数控件
    def genInParams(self, proj, show_panel):
        Run.read_blob(proj)
        params = Run.read_param(proj, config.param_func)
        vars = Run.read_param(proj, config.var_func)
        show_panel.model_id = proj

        scrollPanel = show_panel.scrolledWindow
        show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"参数个数：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        show_panel.var_num = wx.StaticText(scrollPanel, wx.ID_ANY, str(len(params)),
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.var_num, wx.GBPosition(7, 5),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"参数设置：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(8, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        """参数表"""
        show_panel.inputform = EditMixin(scrollPanel)
        show_panel.inputform.InsertColumn(0, '变量名', width=160)
        show_panel.inputform.InsertColumn(1, '描述', width=160)
        show_panel.inputform.InsertColumn(2, '初始值', width=160)
        for i in params:
            index = show_panel.inputform.InsertItem(sys.maxint, i[1])
            show_panel.inputform.SetItem(index, 1, i[0])
            show_panel.inputform.SetItem(index, 2, '0')
        show_panel.inputform.make_editor()
        show_panel.gbSizer.Add(show_panel.inputform, wx.GBPosition(8, 5), wx.GBSpan(5, 7), wx.ALL, 5)

        show_panel.staticText6 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"变量设置：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText6, wx.GBPosition(13, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        """变量表"""
        show_panel.varsform = EditMixin(scrollPanel)
        show_panel.varsform.InsertColumn(0, '变量名', width=160)
        show_panel.varsform.InsertColumn(1, '描述', width=160)
        show_panel.varsform.InsertColumn(2, '初始值', width=160)
        for i in vars:
            index = show_panel.varsform.InsertItem(sys.maxint, i[1])
            show_panel.varsform.SetItem(index, 1, i[0])
            show_panel.varsform.SetItem(index, 2, '0')
        show_panel.varsform.make_editor()
        # show_panel.inputform.GetItemText()
        show_panel.gbSizer.Add(show_panel.varsform, wx.GBPosition(13, 5), wx.GBSpan(5, 7), wx.ALL, 5)

        show_panel.output_num = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"输出个数：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.output_num, wx.GBPosition(18, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        show_panel.output_var = wx.TextCtrl(scrollPanel, wx.ID_ANY, '0',
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.output_var.Bind(wx.EVT_TEXT, self.OutputManage)
        show_panel.gbSizer.Add(show_panel.output_var, wx.GBPosition(18, 5),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.staticText7 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"输出参数：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText7, wx.GBPosition(18 + 1, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.outputform = EditMixin(scrollPanel)
        show_panel.outputform.InsertColumn(0, '变量名', width=240)
        show_panel.outputform.InsertColumn(1, '描述', width=240)
        # show_panel.outputform.InsertColumn(2, '初始值', width=160)
        # for i in params:
        #     index = show_panel.outputform.InsertItem(sys.maxint, i[0])
        #     show_panel.outputform.SetItem(index, 1, i[1])
        # show_panel.outputform.make_editor()

        show_panel.gbSizer.Add(show_panel.outputform, wx.GBPosition(18 + 1, 5), wx.GBSpan(5, 7), wx.ALL, 5)

        show_panel.Layout()

    # 生成输出参数表
    def OutputManage(self, event):
        show_panel = self.GetCurrentPage()
        num = show_panel.output_var.GetValue()
        if num.isdigit() == True:
            show_panel.outputform.ClearAll()
            show_panel.outputform.InsertColumn(0, '变量名', width=240)
            show_panel.outputform.InsertColumn(1, '描述', width=240)
            #   show_panel.outputform.InsertColumn(2, '初始值', width=160)
            for i in range(int(num)):
                index = show_panel.outputform.InsertItem(sys.maxint, u'y' + str(i + 1))
                show_panel.outputform.SetItem(index, 1, u'输出' + str(i + 1))
            show_panel.outputform.make_editor()

    # 保存更新设置
    def SaveUpdate(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        if proj_name == '':
            return
        proj_descr = show_panel.textCtrl2.GetValue()
        old_id = show_panel.old_id
        new_id = show_panel.new_id
        print old_id, '-----', new_id
        inputform = show_panel.inputform
        outputform = show_panel.outputform
        varsform = show_panel.varsform
        inputargs = []
        vars = []
        outputargs = []
        if new_id != -1:
            """删除旧模型"""
            Sql.deleteSql(args=(old_id,), sql=Sql.deleteSamplingResult)
            Sql.deleteSql(args=(old_id,), sql=Sql.deleteModelArgs)
            Sql.deleteSql(args=(old_id,), sql=Sql.deleteModelOutputArgs)
            # Sql.deleteSql(args=(old_id,), sql=Sql.deleteModel)

            """保存输入参数信息到inputargs"""
            for i in range(inputform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(inputform.GetItemText(i, j))
                inputargs.append(temp)

            """保存自变量信息到vars"""
            for i in range(varsform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(varsform.GetItemText(i, j))
                temp.append(0)
                vars.append(temp)

            """保存输出参数信息到inputargs"""
            for i in range(outputform.GetItemCount()):
                temp = []
                for j in range(2):
                    temp.append(outputform.GetItemText(i, j))
                outputargs.append(temp)
            if (Sql.insert_new_model(new_id, inputargs, vars, outputargs) == True) \
            and (Sql.updateSql((proj_name, proj_descr, new_id), Sql.updateProj) == True):
                print '=================================修改成功1'
            self.DeletePage(self.GetPageIndex(show_panel))
#             self.GetParent().GetParent().navTree.updateTree()
        elif new_id == -1:
            """保存输入参数信息到inputargs"""
            for i in range(inputform.GetItemCount()):
                temp = []
                for j in range(4):
                    temp.append(inputform.GetItemText(i, j))
                inputargs.append(temp)

            """保存自变量信息到vars"""
            for i in range(varsform.GetItemCount()):
                temp = []
                for j in range(5):
                    temp.append(varsform.GetItemText(i, j))
                vars.append(temp)
            """保存输出参数信息到inputargs"""
            for i in range(outputform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(outputform.GetItemText(i, j))
                outputargs.append(temp)
            if Sql.update_model(old_id, inputargs, vars, outputargs) == True \
            and (Sql.updateSql((proj_name, proj_descr, old_id), Sql.updateProj) == True):
                print '=================================修改成功2'
            self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()
        # 找到最高层MainUI的Frame
        self.Parent.Parent.Parent.Parent.Parent.updateTree()

    # 保存新建设置
    def SaveNew(self, event):
        try:
            show_panel = self.GetCurrentPage()
            model_id = show_panel.model_id
            inputform = show_panel.inputform
            outputform = show_panel.outputform
            varsform = show_panel.varsform
            inputargs = []
            vars = []
            outputargs = []
            """保存输入参数信息到inputargs"""
            for i in range(inputform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(inputform.GetItemText(i, j))
                inputargs.append(temp)
    
            """保存自变量信息到vars"""
            for i in range(varsform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(varsform.GetItemText(i, j))
                temp.append(0)
                vars.append(temp)
    
            """保存输出参数信息到inputargs"""
            for i in range(outputform.GetItemCount()):
                temp = []
                for j in range(2):
                    temp.append(outputform.GetItemText(i, j))
                outputargs.append(temp)
            if Sql.insert_new_model(model_id, inputargs, vars, outputargs) == True:
                print '=================================新建成功'
            self.DeletePage(self.GetPageIndex(show_panel))
            self.Refresh()
            # 找到最高层MainUI的Frame
            self.Parent.Parent.Parent.Parent.Parent.updateTree()
        except Exception as e:
            dlg = wx.MessageBox("请先导入模型", "提示" ,wx.OK | wx.ICON_INFORMATION)

    # 关闭
    def Cancel(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()

    # 仿真运行
    def TryRun(self, event):
        show_panel = self.GetCurrentPage()
        model_id = show_panel.old_id
        inputform = show_panel.inputform
        varsform = show_panel.varsform
        outputform = show_panel.outputform
        inputargs = []
        vars = []
        """保存输入参数信息到inputargs"""
        for i in range(inputform.GetItemCount()):
            inputargs.append(float(inputform.GetItemText(i, 2)))

        """保存自变量信息到vars"""
        for i in range(varsform.GetItemCount()):
            vars.append(float(varsform.GetItemText(i, 2)))

        result = Run.tryrun(model_id, vars, inputargs)
        print '=================================运行成功', result
        if type(result) == float:
            outputform.SetStringItem(0, 3, str(result))
        elif type(result) == tuple:
            for i in range(min(len(result), outputform.GetItemCount())):
                outputform.SetItem(i, 3, str(result[i]))
        show_panel.Refresh()
        # self.DeletePage(self.GetPageIndex(show_panel))
        # self.Refresh()


class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)