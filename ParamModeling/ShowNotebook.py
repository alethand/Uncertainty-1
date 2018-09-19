# -*- coding: utf-8 -*-

import wx
import sys
import collections
from wx import aui
from wx import grid
import Sql
import config
import mysql.connector
from mysql.connector import Error
from wx.lib.mixins.listctrl import TextEditMixin

import ParaSettingWindow as psw

class ShowNotebook(aui.AuiNotebook):

    # 用于存储ParaSettingWindow中设置的信息
    para_info = 'para_info'
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        
    def ParamDis(self, pProj = 0):
        
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
        title = u"参数设置" + u'（模型：' + modelinfo[0][0] + ')'
        self.AddPage(self.show_panel, title, True, wx.NullBitmap)
        show_panel = self.show_panel
        show_panel.pid = pProj
        show_panel.params = Sql.selectSql((pProj,), Sql.selectParams)
        # show_panel 的布局，只有 scrollPanel 一个元素
        show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
        #为实现滚动条加入 scrollPanel
        show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY, 
                    wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        show_panel.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = show_panel.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        show_panel.gbSizer = wx.GridBagSizer(5, 5)
        show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"请设置参数类型及分布情况：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
        
        show_panel.grid = grid.Grid(scrollPanel, wx.ID_ANY, 
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        # 参数表格
        show_panel.grid.CreateGrid(len(show_panel.params), 7)
        show_panel.grid.SetColSize(0, 200)
        show_panel.grid.SetColLabelValue(0, "参数描述")
        show_panel.grid.SetColLabelValue(1, "参数名")
        show_panel.grid.SetColLabelValue(2, "单位")
        show_panel.grid.SetColLabelValue(3, "参数类型")
        show_panel.grid.SetColSize(3, 200)
        for i in range(len(show_panel.params)):
            show_panel.grid.SetCellEditor(i, 3, grid.GridCellChoiceEditor(
                                                    config.arg_type_get.values()))
        show_panel.grid.SetColLabelValue(4, "参数分布类型")
        for i in range(len(show_panel.params)):
            show_panel.grid.SetCellEditor(i, 4, grid.GridCellChoiceEditor(
                                                    config.dis_type_get.values()))
        show_panel.grid.SetColLabelValue(5, "参数分布数值")
        show_panel.grid.SetColLabelValue(6, "参数设置")
        show_panel.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        for index in range(len(show_panel.params)):
            show_panel.grid.SetCellValue(index, 0, show_panel.params[index][3])
            show_panel.grid.SetCellValue(index, 1, show_panel.params[index][0])
            show_panel.grid.SetCellValue(index, 2, show_panel.params[index][4]
                            if show_panel.params[index][4] != None else '')
            show_panel.grid.SetCellValue(index, 3, config.arg_type_get[show_panel.params[index][5]]
                            if show_panel.params[index][5] != None else '')
            show_panel.grid.SetCellValue(index, 4, config.dis_type_get[show_panel.params[index][6]]
                            if show_panel.params[index][6] != None else '')

            show_panel.grid.SetCellValue(index, 5, show_panel.params[index][7]
                            if show_panel.params[index][7] != None else '')

            show_panel.grid.SetCellValue(index, 6, '双击此处设置')
            show_panel.grid.SetCellBackgroundColour(index, 6, wx.LIGHT_GREY)
            for i in range(3):
                show_panel.grid.SetReadOnly(index, i)
            show_panel.grid.SetReadOnly(index, 5)
            show_panel.grid.SetReadOnly(index, 6)
        show_panel.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.onSet)
        show_panel.gbSizer.Add(show_panel.grid, wx.GBPosition(3, 4),
                               wx.GBSpan(1, 6), wx.ALL, 5)
        
        #分割线
        show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                                  wx.DefaultSize, wx.LI_HORIZONTAL)
            
        # 下方btmPanel
        show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition, 
                                       (-1, 40), wx.TAB_TRAVERSAL)
        show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
                                        (280, 28), wx.TAB_TRAVERSAL)
        '''
        show_panel.check = wx.Button(show_panel.savePanel, wx.ID_ANY, u"LL",
                                    (105, 0), (30, 28), 0)
        show_panel.check.Bind(wx.EVT_BUTTON, self.ShowContent)
        '''
        show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"保存",
                                    (0, 0), (100, 28), 0)
        show_panel.save.Bind(wx.EVT_BUTTON, self.SaveParam)
        show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
                                      (140, 0), (100, 28), 0)
        show_panel.cancel.Bind(wx.EVT_BUTTON, self.CancelParam)

#         show_panel布局设置
        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND |wx.ALL, 5 )
        show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
        show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(show_panel.bSizer)
        show_panel.Layout()
        
#         初始化savePanel位置
        x, y = show_panel.btmPanel.GetSize()
        w, h = show_panel.savePanel.GetSize()
        show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))

#         show_panel.Bind(wx.EVT_SIZE, self.OnReSize)
        show_panel.Bind(wx.EVT_SIZE, 
            lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))
    
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
        
    def SaveParam(self, event):
        show_panel = self.GetCurrentPage()
        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            for index in range(len(show_panel.params)):
                arg_type = config.arg_type_set[show_panel.grid.GetCellValue(index, 3).encode("utf-8")]
                dis_type = config.dis_type_set[show_panel.grid.GetCellValue(index, 4).encode("utf-8")]
                dis_value = show_panel.grid.GetCellValue(index, 5)
                cursor.execute(Sql.updateParams, (arg_type, dis_type, dis_value, show_panel.params[index][1]))
            conn.commit()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        self.DeletePage(self.GetPageIndex(show_panel))
        
    def CancelParam(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))

    '''
    def ShowContent(self, event):
        show_panel = self.GetCurrentPage()
        print('-------------')
        for i in range(0, len(show_panel.params)):
            print(show_panel.grid.GetCellValue(i, 4))
        print('-------------')
    '''

    def onSet(self, event):
        show_panel = self.GetCurrentPage()
        self.para_info = ''
        if event.GetCol() == 6:
            the_dialog = psw.ParaSettingWindow(self)
            the_dialog.set_origin_info(show_panel.grid.GetCellValue(event.GetRow(), 4))
            the_dialog.ShowModal()
        else:
            return
        show_panel = self.GetCurrentPage()
        show_panel.grid.SetCellValue(event.GetRow(), 5, self.para_info)
