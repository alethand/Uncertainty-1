# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
from __future__ import print_function
from __future__ import print_function
import thread

import time

import sys
import wx
import wx.xrc
import wx.lib.newevent
from wx import grid
from wx.lib.mixins.grid import GridAutoEditMixin

import ProcessBar as pb

from SamplingMethod import *
import Sql
import commonTag

class SelectSamplingMethodPanel(wx.Panel):
    count = 0
    strategystr = {'random':1,'LHS':2}
    def __init__(self, parent,n_id):
        """ 初始化 """
        wx.Panel.__init__(self, parent, n_id * 2, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)

        # self 的布局，有 scrollPanel 和input_panel两个元素
        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        # 为实现滚动条加入 scrollPanel
        self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = self.scrolledWindow

        # 上部modelInfo_Panel
        self.modelInfo_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self.modelInfo_panel.SetMaxSize(wx.Size(-1,100))
        # modelInfo_panel 的布局，元素为显示的控件
        self.modelInfo_panel.gbSizer = wx.GridBagSizer(5, 5)
        self.modelInfo_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.modelInfo_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 上部input_Panel
        self.input_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                       (-1, 40), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1,100))
        # input_panel 的布局，元素为显示的控件
        self.input_panel.gbSizer = wx.GridBagSizer(5, 5)
        self.input_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.input_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)



        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer_show = wx.GridBagSizer(5, 5)
        self.gbSizer_show.SetFlexibleDirection(wx.BOTH)
        self.gbSizer_show.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        first_positon = 0
        next_positon = 1 + first_positon

        self.m_staticText_erp_size = wx.StaticText(self.input_panel, wx.ID_ANY, u"固有不确定性参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_panel.gbSizer.Add(self.m_staticText_erp_size, wx.GBPosition(first_positon, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_erp_size = wx.TextCtrl(self.input_panel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.input_panel.gbSizer.Add(self.m_textCtrl_erp_size, wx.GBPosition(first_positon, 5),
                               wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_staticText_esp_size = wx.StaticText(self.input_panel, wx.ID_ANY, u"认知不确定性参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_panel.gbSizer.Add(self.m_staticText_esp_size, wx.GBPosition(first_positon, 9),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_esp_size = wx.TextCtrl(self.input_panel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.input_panel.gbSizer.Add(self.m_textCtrl_esp_size, wx.GBPosition(first_positon, 10),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_staticText_input_size = wx.StaticText(self.input_panel, wx.ID_ANY, u"仿真系统输入参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_panel.gbSizer.Add(self.m_staticText_input_size, wx.GBPosition(next_positon, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_input_size = wx.TextCtrl(self.input_panel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.input_panel.gbSizer.Add(self.m_textCtrl_input_size, wx.GBPosition(next_positon, 5),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        ''' 确认和重置按钮的panel begins '''
        self.m_button_ok = wx.Button(self.input_panel, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.create_sample)
        self.input_panel.gbSizer.Add(self.m_button_ok, wx.GBPosition(next_positon, 10),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_reset = wx.Button(self.input_panel, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)
        self.input_panel.gbSizer.Add(self.m_button_reset, wx.GBPosition(next_positon, 11),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_show = wx.Button(self.input_panel, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)
        self.m_button_show.Show(False)
        self.input_panel.gbSizer.Add(self.m_button_show, wx.GBPosition(next_positon, 12),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        ''' 确认和重置按钮的panel ends '''

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                              wx.DefaultSize, wx.LI_HORIZONTAL)

        # 上方提示信息Panel
        commonTag.setModeltag(self.modelInfo_panel, n_id)

        # 提示信息
        self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"抽样设置：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_set.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))

        self.m_staticText_set.SetMaxSize(wx.Size(-1, 20))

        self.m_staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
                                          wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText_show.SetMaxSize(wx.Size(-1, 20))


        # show_panel布局设置
        self.input_panel.SetSizer(self.input_panel.gbSizer)
        self.modelInfo_panel.SetSizer(self.modelInfo_panel.gbSizer)
        scrollPanel.SetSizer(self.gbSizer_show)
        # ADD
        self.bSizer.Add(self.modelInfo_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.bSizer.Add(self.m_staticText_set, 1, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.bSizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        self.bSizer.Add(self.m_staticText_show, 1, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.bSizer)

        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def set_up(self, p, method):
        """ 外部设置分布类型、抽样方法和参数以及参数名称等 """
        '''用类传递'''
        self.method_name = method
        self.param = p
        self.Er_p_size_of_par = 0
        self.Es_p_size_of_par = 0
        self.input_size_of_par = 0

        self.Er_p_name = []
        self.Es_p_name = []
        self.input_name = []
        i = 0
        for pt in self.param.partype:
            if (pt == 1):
                self.Er_p_size_of_par += 1
                self.Er_p_name.append(self.param.name[i])
            else:
                if(pt == 2):
                    self.Es_p_size_of_par += 1
                    self.Es_p_name.append(self.param.name[i])
                else:
                    self.input_size_of_par += 1
                    self.input_name.append(self.param.name[i])
            i += 1
        pass

    # 等待写操作完成的方法
    # 进度条控制添加完成
    # 进度条由此处发消息进行控制
    def writing(self):
        self.xpb = pb.ProcessBar(None, '抽样中', 1000)
        # 循环抽样并写入所有的参数的抽样结果 生成抽样实验方案
        self.count = 0
        self.results = []
        for p in self.param.para:
            self.get_Result_Of_Paras(self.count)
            self.count += 1
        while(self.count <= 200):
            time.sleep(0.01)
            self.count += 1
            self.xpb.SetProcess(self.count)
        self.SQLrun()
        self.xpb.SetProcess(self.count,1)
        time.sleep(0.5)
        dlg = wx.MessageDialog(None, message='抽样完成！')
        dlg.ShowModal()
        # create event class

        # 创建用于展示结果的 事件 用来代替展示结果按键绑定的事件 使之能自动发起该事件 而不用 点击按键
        ShowResultEvent, EVT_SHOW_RESULT = wx.lib.newevent.NewEvent()

        m_show = wx.Control()

        wx.PostEvent(m_show, ShowResultEvent())

        m_show.Bind(EVT_SHOW_RESULT, self.show_result)

        self.Layout()



    def draw_table(self, i, x, y):
        results = self.type_result[i]
        # size = self.ssize[i]
        size_of_par = self.size_of_par[i]

        grid = self.tables[i]
        grid.SetMaxSize(wx.Size(320, 360))
        grid.SetMinSize(wx.Size(320, 360))
        names = self.names[i]

        grid.CreateGrid(28, 13)
        grid.EnableEditing(True)
        grid.EnableGridLines(True)
        grid.EnableDragGridSize(False)
        grid.SetMargins(0, 0)


        # Columns
        grid.EnableDragColMove(False)
        grid.EnableDragColSize(True)
        grid.SetColLabelSize(30)
        grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        i = 0
        for namei in names:
            grid.SetColLabelValue(i, namei)
            i += 1


        # 设置内容
        # Rows
        grid.EnableDragRowSize(True)
        grid.SetRowLabelSize(80)
        grid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        """"设置内容"""
        j = 0
        for result in results:
            i = 0
            for row in result:
                # 截段输出 numpy 抽样结果过长
                grid.SetCellValue(i, j, str(("%.3f" % row)))
                i = i + 1
            j += 1


        self.gbSizer_show.Add(grid, wx.GBPosition(x, y), wx.GBSpan(1, 3), wx.ALL, 5)
        return y + size_of_par

    # 展示结果的方法
    # 抽样和显示抽样结果在一个类里面 反复读写数据库 没有必要 直接读取类的成员变量即可
    def show_result(self, event):
        self.m_staticText_show.SetLabelText(u"结果展示:")
        self.m_staticText_show.SetFont(wx.Font(10.5, 70, 90, 92, False, "宋体" ))
        # 清空gbSizer_show
        self.gbSizer_show.Clear()

        """固有不确定性参数表格"""
        self.ER_grid = grid.Grid(self.scrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        """认知不确定性参数表格"""
        self.ES_grid = grid.Grid(self.scrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        """输入参数表格"""
        self.Input_grid = grid.Grid(self.scrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        """表格列表"""
        self.tables = self.Input_grid, self.ER_grid, self.ES_grid

        # 设置提示字和表格的垂直距离

        text_position = 0
        table_position = text_position + 1
        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"固有不确定性参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer_show.Add(self.m_staticText_input_size, wx.GBPosition(text_position, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        # 获取返回的边界坐标 获取下一个参数的其实坐标
        nextstart = self.draw_table(1, table_position , 4) + 2

        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"认知不确定性参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer_show.Add(self.m_staticText_input_size, wx.GBPosition(text_position, nextstart),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        nextstart = self.draw_table(2,table_position ,nextstart) + 2

        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"输入参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer_show.Add(self.m_staticText_input_size, wx.GBPosition(text_position, nextstart),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.draw_table(0,table_position ,nextstart)
        self.scrolledWindow.Refresh()
        self.Layout()

    def create_sample(self, event):
        """ 用户点击确定按钮后开始抽样并写入数据库 """
        self.Er_p_size = int(self.m_textCtrl_erp_size.GetValue())
        self.Es_p_size = int(self.m_textCtrl_esp_size.GetValue())
        self.input_size = int(self.m_textCtrl_input_size.GetValue())
        self.ssize = self.input_size, self.Er_p_size, self.Es_p_size
        self.size_of_par = self.input_size_of_par, self.Er_p_size_of_par, self.Es_p_size_of_par
        self.names = self.input_name, self.Er_p_name, self.Es_p_name
        self.type_result = [],[],[]
#         print (self.param.para[0])
        self.stra = 0  # 具体策略编号

        # FIXME: 这里由于元组的问题，必须传入足够多的参数，传入para的数量是现有分布所需参数个数的最大值

#         Sql.clear_sampling_result() # 先清空历史数据
        Sql.clear_sampling_result_of_model(self.param.model_id)
        # 进度条UI放入子线程：
        try:
            thread.start_new_thread(self.writing, ())
        except:
            print("Error: unable to start thread")

    def reset_settings(self, event):
        """ 重置窗口中以输入的数据 """
        self.m_textCtrl_erp_size.Clear()
        self.m_textCtrl_esp_size.Clear()
        self.m_textCtrl_input_size.Clear()

    def get_Result_Of_Paras(self, i):
        # 判断长度防止元祖越界
        result = 0
        #FIXME:情况不全
        print(self.param.para[i])
        if len(self.param.para[i]) is 3:
            result = strategy[self.method_name[i]].GetResult(self.ssize[self.param.partype[i]], kind_dict[self.param.dtype[i]],
                                                         self.param.para[i][0], self.param.para[i][1], self.param.para[i][2])
        elif len(self.param.para[i]) is 2:
            result = strategy[self.method_name[i]].GetResult(self.ssize[self.param.partype[i]], kind_dict[self.param.dtype[i]],
                                                self.param.para[i][0], self.param.para[i][1])
        elif len(self.param.para[i]) is 1:
            result = strategy[self.method_name[i]].GetResult(self.ssize[self.param.partype[i]],
                                                             kind_dict[self.param.dtype[i]],
                                                             self.param.para[i][0])
        self.type_result[self.param.partype[i]].append(result)
        self.results.append(result)

    def SQLrun(self):
#         Sql.insert_sampling_result(self.param.name, self.results)
        Sql.insert_sampling_results(self.param.parid, self.results,self.method_name)

# class EditMixin(GridAutoEditMixin):
#     def __init__(self, parent):
#         # wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
#         GridAutoEditMixin.__init__(self)

