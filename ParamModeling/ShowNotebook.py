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
import applicationSceneDialog as asd
import causeDialog as cd
import effectDialog as ed
import lifeTimeDialog as ltd
import plotPanel as pp
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class ShowNotebook(aui.AuiNotebook):

    # 用于存储ParaSettingWindow中设置的信息
    para_info = 'para_info'
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
    def uncertaintyDis(self, pProj = 0):

        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
        title = u"不确定性设置" + u'（模型：' + modelinfo[0][0] + ')'
        self.AddPage(self.show_panel, title, True, wx.NullBitmap)
        show_panel = self.show_panel
        show_panel.pid = pProj
        show_panel.params = Sql.selectSql((pProj,), Sql.selectInfromations)

        # self.theLastParams = show_panel.params

        self.arg_descr = []
        self.arg_name = []
        self.arg_unit = []
        self.arg_type = []
        self.dis_type = []
        self.dis_arg = []
        self.uncertainty_kind = []
        self.measurement = []
        self.cause = []
        self.effect = []
        self.pattern = []
        self.life_time = []
        self.application_scene = []
        self.arg_id = []
        self.begin_time = []
        self.end_time = []
        self.cause_return = []
        self.effect_return =[]
        self.dis_arg_1 = []
        self.dis_arg_2 = []
        self.all_number = 0

        for index in show_panel.params:
            self.arg_descr.append(index[0])
            self.arg_name.append(index[1])
            self.arg_unit.append(index[2])
            self.arg_type.append(index[3])
            self.dis_type.append(index[4])
            self.dis_arg.append(index[5])
            # if index[5] != None:
            # if index[5] != None
            print '----------------'
            print index[5]
            # print index[5].split(" ")
            if index[5] != None:
                if len(index[5].split(" ")) == 1 and index[5].split(" ")[0] != '':
                    self.dis_arg_1.append(index[5].split(" ")[0])
                    self.dis_arg_2.append('')
                elif len(index[5].split(" ")) == 3:
                    self.dis_arg_1.append(index[5].split(" ")[1])
                    self.dis_arg_2.append(index[5].split(" ")[2])
                else:
                    self.dis_arg_1.append('')
                    self.dis_arg_2.append('')
            else:
                self.dis_arg_1.append('')
                self.dis_arg_2.append('')

            # self.dis_arg_1.append(index[5].split(" ")[1] if index[5] != None else '')
            # self.dis_arg_2.append(index[5].split(" ")[2] if index[5] != None and len(index[5].split(" "))==3 else '')
            # testDisArg = index[5].split(" ")
            self.uncertainty_kind.append(index[6])
            self.measurement.append(index[7])
            self.cause_return.append(index[8])
            self.effect_return.append(index[9])
            self.cause.append(index[8].split(" ") if index[8] != None else '')
            self.effect.append(index[9].split(" ")  if index[9] != None else '')
            self.pattern.append(index[10])
            self.life_time.append(index[11])
            self.begin_time.append(index[11].split(" ")[0] if index[11] != None else '')
            self.end_time.append(index[11].split(" ")[1] if index[11] != None else '')
            self.application_scene.append(index[12])
            self.arg_id.append(index[13])
            self.all_number += 1

        # show_panel 的布局，只有 scrollPanel 一个元素
        show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
        #为实现滚动条加入 scrollPanel
        show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        show_panel.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = show_panel.scrolledWindow

        # -----------------------------------------
        # scrollPanel 的布局，元素为显示的控件
        bSizer15 = show_panel.bSizer

        # scrollPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel12 = wx.Panel(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText_arg_list = wx.StaticText(self.m_panel12, wx.ID_ANY, u"参数列表", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.m_staticText_arg_list.Wrap(-1)
        self.m_staticText_arg_list.SetFont(wx.Font(20, 70, 90, 90, False, wx.EmptyString))

        bSizer9.Add(self.m_staticText_arg_list, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        # ----------------------------------------------------descr
        m_listBox_choice_argChoices = self.arg_descr
        self.m_listBox_choice_arg = wx.ListBox(self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               m_listBox_choice_argChoices, wx.LB_ALWAYS_SB)
        self.m_listBox_choice_arg.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        bSizer9.Add(self.m_listBox_choice_arg, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel12.SetSizer(bSizer9)
        self.m_panel12.Layout()
        bSizer9.Fit(self.m_panel12)
        bSizer13.Add(self.m_panel12, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel13 = wx.Panel(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText_arg_setting = wx.StaticText(self.m_panel13, wx.ID_ANY, u"参数设置", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.m_staticText_arg_setting.Wrap(-1)
        self.m_staticText_arg_setting.SetFont(wx.Font(20, 70, 90, 90, False, wx.EmptyString))

        bSizer10.Add(self.m_staticText_arg_setting, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel14 = wx.Panel(self.m_panel13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel43 = wx.Panel(self.m_panel14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer29 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel49 = wx.Panel(self.m_panel43, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer32 = wx.BoxSizer(wx.VERTICAL)

        # ==========

        # ============

        self.m_panel50 = wx.Panel(self.m_panel49, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer18 = wx.GridSizer(6, 2, 0, 0)

        self.m_staticText_arg_descr = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数描述", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.m_staticText_arg_descr.Wrap(-1)
        self.m_staticText_arg_descr.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText_arg_descr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_arg_descr = wx.TextCtrl(self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.m_textCtrl_arg_descr.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_textCtrl_arg_descr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        self.m_staticText_arg_name = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数名称", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.m_staticText_arg_name.Wrap(-1)
        self.m_staticText_arg_name.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText_arg_name, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_arg_name = wx.TextCtrl(self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.m_textCtrl_arg_name.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_textCtrl_arg_name, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        self.m_staticText1_arg_unit = wx.StaticText(self.m_panel50, wx.ID_ANY, u"单位描述", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.m_staticText1_arg_unit.Wrap(-1)
        self.m_staticText1_arg_unit.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText1_arg_unit, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_arg_unit = wx.TextCtrl(self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.m_textCtrl_arg_unit.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        gSizer18.Add(self.m_textCtrl_arg_unit, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        # --------------------
        self.m_staticText20 = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数开始时间", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText20.Wrap(-1)
        self.m_staticText20.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText20, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_arg_begin_time = wx.TextCtrl(self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                     wx.DefaultSize, 0)
        self.m_textCtrl_arg_begin_time.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_textCtrl_arg_begin_time, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        self.m_staticText21 = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数结束时间", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText21.Wrap(-1)
        self.m_staticText21.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText21, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_arg_end_time = wx.TextCtrl(self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.m_textCtrl_arg_end_time.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_textCtrl_arg_end_time, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        # --------------------
        self.m_staticText_arg_type = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数类型", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.m_staticText_arg_type.Wrap(-1)
        self.m_staticText_arg_type.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer18.Add(self.m_staticText_arg_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_choice_arg_typeChoices = [config.arg_type_get[i] for i in range(len(config.arg_type_get))]
        self.m_choice_arg_type = wx.Choice(self.m_panel50, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           m_choice_arg_typeChoices, 0)
        self.m_choice_arg_type.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        # self.m_choice_arg_type.SetSelection(0)
        gSizer18.Add(self.m_choice_arg_type, 0,
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)

        # =====
        # self.m_staticText_arg_type = wx.StaticText(self.m_panel50, wx.ID_ANY, u"参数类型", wx.DefaultPosition,
        #                                            wx.DefaultSize, 0)
        # self.m_staticText_arg_type.Wrap(-1)
        # gSizer18.Add(self.m_staticText_arg_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        #
        # m_choice_arg_typeChoices = [config.arg_type_get[i] for i in range(len(config.arg_type_get))]
        # self.m_choice_arg_type = wx.Choice(self.m_panel50, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
        #                                    m_choice_arg_typeChoices, 0)
        # self.m_choice_arg_type.SetSelection(0)
        #
        # # ---------------------------------------------------------
        # gSizer18.Add(self.m_choice_arg_type, 0,
        #              wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
        # =====

        self.m_panel50.SetSizer(gSizer18)
        self.m_panel50.Layout()
        gSizer18.Fit(self.m_panel50)
        bSizer32.Add(self.m_panel50, 6, wx.EXPAND | wx.ALL, 5)

        self.m_panel271 = wx.Panel(self.m_panel49, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer12 = wx.GridSizer(0, 2, 0, 0)


        self.m_panel271.SetSizer(gSizer12)
        self.m_panel271.Layout()
        gSizer12.Fit(self.m_panel271)
        bSizer32.Add(self.m_panel271, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel49.SetSizer(bSizer32)
        self.m_panel49.Layout()
        bSizer32.Fit(self.m_panel49)
        bSizer29.Add(self.m_panel49, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel46 = wx.Panel(self.m_panel43, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer30 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel47 = wx.Panel(self.m_panel46, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer19 = wx.GridSizer(6, 2, 0, 0)

        self.m_staticText_uncertainty_kind = wx.StaticText(self.m_panel47, wx.ID_ANY, u"不确定性设置", wx.DefaultPosition,
                                                           wx.DefaultSize, 0)
        self.m_staticText_uncertainty_kind.Wrap(-1)
        self.m_staticText_uncertainty_kind.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText_uncertainty_kind, 1,
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        # --------------------------------------------------
        m_choice_uncertainty_kindChoices = [config.uncertaintyKind[i] for i in range(len(config.uncertaintyKind))]
        self.m_choice_uncertainty_kind = wx.Choice(self.m_panel47, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                   m_choice_uncertainty_kindChoices, 0)
        # self.m_choice_uncertainty_kind.SetSelection(0)
        self.m_choice_uncertainty_kind.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_choice_uncertainty_kind, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
                     10)

        self.m_staticText_measurement = wx.StaticText(self.m_panel47, wx.ID_ANY, u"度量方法", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.m_staticText_measurement.Wrap(-1)
        self.m_staticText_measurement.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText_measurement, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
                     5)

        m_choice_measurementChoices = [config.measurement[i] for i in range(len(config.measurement))]
        self.m_choice_measurement = wx.Choice(self.m_panel47, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              m_choice_measurementChoices, 0)
        self.m_choice_measurement.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        # self.m_choice_measurement.SetSelection(0)
        gSizer19.Add(self.m_choice_measurement, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        self.m_staticText_pattern = wx.StaticText(self.m_panel47, wx.ID_ANY, u"不确定性模式", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.m_staticText_pattern.Wrap(-1)
        self.m_staticText_pattern.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText_pattern, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_choice_patternChoices = [config.pattern[i] for i in range(len(config.pattern))]
        self.m_choice_pattern = wx.Choice(self.m_panel47, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          m_choice_patternChoices, 0)
        self.m_choice_pattern.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        # self.m_choice_pattern.SetSelection(0)
        gSizer19.Add(self.m_choice_pattern, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL|wx.EXPAND, 10)

        # --------------------
        self.m_staticText19 = wx.StaticText(self.m_panel47, wx.ID_ANY, u"参数分布类型", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText19.Wrap(-1)
        self.m_staticText19.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText19, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_choice6Choices = [config.dis_type_get1[i] for i in range(len(config.dis_type_get1))]
        self.m_choice_dis_type = wx.Choice(self.m_panel47, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice6Choices, 0)
        # self.m_choice_dis_type.SetSelection(0)
        self.m_choice_dis_type.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_choice_dis_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)

        self.m_choice_dis_type.Bind(wx.EVT_CHOICE, self.onChangeChoice)

        # -------------------
        self.m_staticText_dis_arg_1 = wx.StaticText(self.m_panel47, wx.ID_ANY, u"分布参数1", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.m_staticText_dis_arg_1.Wrap(-1)
        self.m_staticText_dis_arg_1.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText_dis_arg_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_dis_arg_1 = wx.TextCtrl(self.m_panel47, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.m_textCtrl_dis_arg_1.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        gSizer19.Add(self.m_textCtrl_dis_arg_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        self.m_staticText_dis_arg_2 = wx.StaticText(self.m_panel47, wx.ID_ANY, u"分布参数2", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.m_staticText_dis_arg_2.Wrap(-1)
        self.m_staticText_dis_arg_2.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer19.Add(self.m_staticText_dis_arg_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_dis_arg_2 = wx.TextCtrl(self.m_panel47, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.m_textCtrl_dis_arg_2.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        gSizer19.Add(self.m_textCtrl_dis_arg_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 10)

        # self.m_staticText_arg_type = wx.StaticText(self.m_panel47, wx.ID_ANY, u"参数类型", wx.DefaultPosition,
        #                                            wx.DefaultSize, 0)
        # self.m_staticText_arg_type.Wrap(-1)
        # gSizer12.Add(self.m_staticText_arg_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        # # _-----------------------set arg_type------------------------------------------------------
        # m_choice_arg_typeChoices = [config.arg_type_get[i] for i in range(len(config.arg_type_get))]
        # self.m_choice_arg_type = wx.Choice(self.m_panel47, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
        #                                    m_choice_arg_typeChoices, 0)
        # self.m_choice_arg_type.SetSelection(0)
        # gSizer12.Add(self.m_choice_arg_type, 1,
        #              wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
        #
        # .....................................



        # --------------------
        self.m_panel47.SetSizer(gSizer19)
        self.m_panel47.Layout()
        gSizer19.Fit(self.m_panel47)
        bSizer30.Add(self.m_panel47, 6, wx.EXPAND | wx.ALL, 5)

        self.m_panel48 = wx.Panel(self.m_panel46, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer31 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_other = wx.Button(self.m_panel48, wx.ID_ANY, u"参数分布文件导入", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button_other.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        bSizer31.Add(self.m_button_other, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button_other.Bind(wx.EVT_BUTTON, self.chooseFile)

        self.m_panel48.SetSizer(bSizer31)
        self.m_panel48.Layout()
        bSizer31.Fit(self.m_panel48)
        bSizer30.Add(self.m_panel48, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel46.SetSizer(bSizer30)
        self.m_panel46.Layout()
        bSizer30.Fit(self.m_panel46)
        bSizer29.Add(self.m_panel46, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel43.SetSizer(bSizer29)
        self.m_panel43.Layout()
        bSizer29.Fit(self.m_panel43)
        bSizer14.Add(self.m_panel43, 7, wx.EXPAND | wx.ALL, 5)

        self.m_panel281 = wx.Panel(self.m_panel14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer7 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText_cause = wx.StaticText(self.m_panel281, wx.ID_ANY, u"起因", wx.DefaultPosition, wx.DefaultSize,
                                                0)
        self.m_staticText_cause.Wrap(-1)
        self.m_staticText_cause.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer7.Add(self.m_staticText_cause, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, 5)

        self.m_staticText_effect = wx.StaticText(self.m_panel281, wx.ID_ANY, u"影响", wx.DefaultPosition, wx.DefaultSize,
                                                 0)
        self.m_staticText_effect.Wrap(-1)
        self.m_staticText_effect.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        gSizer7.Add(self.m_staticText_effect, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, 5)

        self.m_panel281.SetSizer(gSizer7)
        self.m_panel281.Layout()
        gSizer7.Fit(self.m_panel281)
        bSizer14.Add(self.m_panel281, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel28 = wx.Panel(self.m_panel14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer8 = wx.GridSizer(0, 2, 0, 0)

        # m_checkList_causeChoices = self.arg_descr
        m_checkList_causeChoices = []
        self.m_checkList_cause = wx.CheckListBox(self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 50),
                                                 m_checkList_causeChoices, wx.LB_ALWAYS_SB)
        self.m_checkList_cause.SetMinSize(wx.Size(-1, 50))
        self.m_checkList_cause.SetMaxSize(wx.Size(-1, 50))
        self.m_checkList_cause.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        gSizer8.Add(self.m_checkList_cause, 1,
                    wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        # m_checkList_effectChoices = self.arg_descr
        m_checkList_effectChoices = []
        self.m_checkList_effect = wx.CheckListBox(self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 50),
                                                  m_checkList_effectChoices, wx.LB_ALWAYS_SB)
        self.m_checkList_effect.SetMinSize(wx.Size(-1, 50))
        self.m_checkList_effect.SetMaxSize(wx.Size(-1, 50))

        self.m_checkList_effect.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))


        gSizer8.Add(self.m_checkList_effect, 1,
                    wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_panel28.SetSizer(gSizer8)
        self.m_panel28.Layout()
        gSizer8.Fit(self.m_panel28)
        bSizer14.Add(self.m_panel28, 2, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        self.m_panel31 = wx.Panel(self.m_panel14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel34 = wx.Panel(self.m_panel31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer22 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel33 = wx.Panel(self.m_panel34, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText_application_scene = wx.StaticText(self.m_panel33, wx.ID_ANY, u"场景说明", wx.DefaultPosition,
                                                            wx.DefaultSize, 0)
        self.m_staticText_application_scene.Wrap(-1)
        self.m_staticText_application_scene.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        bSizer19.Add(self.m_staticText_application_scene, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_richText_application_scene = wx.richtext.RichTextCtrl(self.m_panel33, wx.ID_ANY, wx.EmptyString,
                                                                     wx.DefaultPosition, wx.DefaultSize,
                                                                     0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.m_richText_application_scene.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        bSizer19.Add(self.m_richText_application_scene, 3, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel33.SetSizer(bSizer19)
        self.m_panel33.Layout()
        bSizer19.Fit(self.m_panel33)
        bSizer22.Add(self.m_panel33, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel34.SetSizer(bSizer22)
        self.m_panel34.Layout()
        bSizer22.Fit(self.m_panel34)
        bSizer21.Add(self.m_panel34, 2, wx.EXPAND | wx.ALL, 5)

        self.m_panel35 = wx.Panel(self.m_panel31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer23 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel29 = wx.Panel(self.m_panel35, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer23.Add(self.m_panel29, 1, wx.EXPAND | wx.ALL, 5)

        self.m_button_ok = wx.Button(self.m_panel35, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.m_button_ok, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_button_ok.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        self.m_button_ok.Hide()

        self.m_button_cancel = wx.Button(self.m_panel35, wx.ID_ANY, u"下一项", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.m_button_cancel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_button_cancel.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))
        self.m_button_cancel.Bind(wx.EVT_BUTTON, self.next_arg)

        self.m_panel35.SetSizer(bSizer23)
        self.m_panel35.Layout()
        bSizer23.Fit(self.m_panel35)
        bSizer21.Add(self.m_panel35, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel31.SetSizer(bSizer21)
        self.m_panel31.Layout()
        bSizer21.Fit(self.m_panel31)
        bSizer14.Add(self.m_panel31, 3, wx.EXPAND | wx.ALL, 5)

        self.m_panel14.SetSizer(bSizer14)
        self.m_panel14.Layout()
        bSizer14.Fit(self.m_panel14)
        bSizer10.Add(self.m_panel14, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel13.SetSizer(bSizer10)
        self.m_panel13.Layout()
        bSizer10.Fit(self.m_panel13)
        bSizer13.Add(self.m_panel13, 3, wx.EXPAND | wx.ALL, 5)

        scrollPanel.SetSizer(bSizer13)
        scrollPanel.Layout()
        bSizer13.Fit(scrollPanel)

        # bSizer15.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        # W***************************************************

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
        show_panel.save.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        show_panel.save.Bind(wx.EVT_BUTTON, self.saveUncertainty_all)
        show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
                                      (140, 0), (100, 28), 0)
        show_panel.cancel.SetFont(wx.Font(13, 70, 90, 90, False, wx.EmptyString))

        show_panel.cancel.Bind(wx.EVT_BUTTON, self.cancelUncertainty)

        #         show_panel布局设置

        scrollPanel.SetSizer(bSizer13)
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

        scrollPanel.Bind(wx.EVT_LISTBOX_DCLICK, self.choiceList)

    def chooseFile(self, event):
        filePath = None
        exprssion = None
        dlg = wx.FileDialog(self, u"选择文件", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            filePath = dlg.GetPath()
        dlg.Destroy()
        # file_object = open(filePath)
        with open(filePath) as f:
            line = f.readline()
            while line:
                if line.__contains__('expr'):
                    print line
                    break
                line = f.readline()
            exprssion = line.replace(' ', '')[6:-2]
            self.m_textCtrl_func.SetLabelText(exprssion)

    def onChangeChoice(self, event):
        self.m_textCtrl_dis_arg_1.Clear()
        self.m_textCtrl_dis_arg_2.Clear()
        # self.m_textCtrl_func.Clear()
        if self.m_choice_dis_type.GetSelection() == 0:
            self.m_staticText_dis_arg_1.SetLabelText('mu')
            self.m_staticText_dis_arg_2.SetLabelText('sigma')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 1:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 2:
            self.m_staticText_dis_arg_1.SetLabelText('theta')
            self.m_staticText_dis_arg_2.Hide()
            self.m_textCtrl_dis_arg_2.Hide()
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 3:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_dis_arg_1.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Show(True)
            # self.m_textCtrl_func.Show(True)
            self.m_button_other.Show(True)

    def choiceList(self, event):
        # 选择第几个
        sel = self.m_listBox_choice_arg.GetSelection()
        text = self.m_listBox_choice_arg.GetString(sel)
        self.m_textCtrl_arg_descr.SetValue(self.arg_descr[sel] if self.arg_descr[sel] != None else '')
        self.m_textCtrl_arg_name.SetValue(self.arg_name[sel] if self.arg_name[sel] != None else '')
        self.m_textCtrl_arg_unit.SetValue(self.arg_unit[sel] if self.arg_unit[sel] != None else '')
        self.m_textCtrl_arg_begin_time.SetValue(self.begin_time[sel] if self.begin_time[sel] !=None else '')
        self.m_textCtrl_arg_end_time.SetValue(self.end_time[sel] if self.end_time[sel] != None else '')
        self.m_textCtrl_dis_arg_1.SetValue(self.dis_arg_1[sel] if self.dis_arg_1[sel] != None else '')
        self.m_textCtrl_dis_arg_2.SetValue(self.dis_arg_2[sel] if self.dis_arg_2[sel] != None else '')
        self.m_richText_application_scene.SetValue(self.application_scene[sel] if self.application_scene[sel] != None else '')
        if self.arg_type[sel] != None:
            self.m_choice_arg_type.SetSelection(self.arg_type[sel])
        else:
            # LLLLLL = config.arg_type_get[0]
            self.m_choice_arg_type.SetSelection(0)
        # self.m_choice_arg_type.SetSelection(self.arg_type[sel]
        #                                     if self.arg_type[sel] != None
        #                                     else config.arg_type_get[0])
        # print config.measurement[0]
        # self.m_choice_measurement.SetSelection(self.measurement[sel] if self.measurement[sel] != None else 0)
        if self.measurement[sel] != None:
            self.m_choice_measurement.SetSelection(self.measurement[sel])

        # self.m_choice_pattern.SetSelection(self.pattern[sel] if self.pattern[sel] != None else 0)
        if self.pattern[sel] != None:
            self.m_choice_pattern.SetSelection(self.pattern[sel])
        # print self.uncertainty_kind[sel]
        # self.m_choice_uncertainty_kind.SetSelection(self.uncertainty_kind[sel] if self.uncertainty_kind[sel] != None else 0)
        if self.uncertainty_kind[sel] != None:
            self.m_choice_uncertainty_kind.SetSelection(self.uncertainty_kind[sel])
        # print config.dis_index_set[config.dis_type_get[self.dis_type[sel]]]
        if self.dis_type[sel] != None:
            self.m_choice_dis_type.SetSelection(
                config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]])
            # self.m_choice_dis_type.SetSelection(config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]] if self.dis_type[sel] != None else 0)
        if self.m_choice_dis_type.GetSelection() == 0:
            self.m_staticText_dis_arg_1.SetLabelText('mu')
            self.m_staticText_dis_arg_2.SetLabelText('sigma')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 1:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 2:
            self.m_staticText_dis_arg_1.SetLabelText('theta')
            self.m_staticText_dis_arg_2.Hide()
            self.m_textCtrl_dis_arg_2.Hide()
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 3:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_dis_arg_1.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Show(True)
            # self.m_textCtrl_func.Show(True)
            self.m_button_other.Show(True)

        getCauseList = []
        getEffectList = []

        self.m_checkList_cause.Clear()
        self.m_checkList_effect.Clear()

        CauseList = self.arg_descr[:]
        del CauseList[sel]
        # print '-------**-----'
        # print CauseList
        # print '--------@@----'

        EffectList = self.arg_descr[:]
        del EffectList[sel]
        # print '-------**-----'
        # print EffectList
        # print '--------@@----'
        self.m_checkList_cause.Set(CauseList)
        # self.m_checkList_effect.Clear()
        self.m_checkList_effect.Set(EffectList)

        for index in self.cause[sel]:
            if index != "":
                getCauseList.append(CauseList.index(index))
        # del getCauseList[sel]
        self.m_checkList_cause.SetCheckedItems(getCauseList)
        for index in self.effect[sel]:
            if index != "":
                getEffectList.append(EffectList.index(index))
        # del getEffectList[sel]
        self.m_checkList_effect.SetCheckedItems(getEffectList)

        # show_panel.grid.SetCellValue(index, 3, config.arg_type_get[show_panel.params[index][5]]
        print "hahahahah",sel
        print text

    def changePage(self, theSel):
        # 选择第几个
        sel = theSel
        text = self.m_listBox_choice_arg.GetString(sel)
        self.m_textCtrl_arg_descr.SetValue(self.arg_descr[sel] if self.arg_descr[sel] != None else '')
        self.m_textCtrl_arg_name.SetValue(self.arg_name[sel] if self.arg_name[sel] != None else '')
        self.m_textCtrl_arg_unit.SetValue(self.arg_unit[sel] if self.arg_unit[sel] != None else '')
        self.m_textCtrl_arg_begin_time.SetValue(self.begin_time[sel] if self.begin_time[sel] != None else '')
        self.m_textCtrl_arg_end_time.SetValue(self.end_time[sel] if self.end_time[sel] != None else '')
        self.m_textCtrl_dis_arg_1.SetValue(self.dis_arg_1[sel] if self.dis_arg_1[sel] != None else '')
        self.m_textCtrl_dis_arg_2.SetValue(self.dis_arg_2[sel] if self.dis_arg_2[sel] != None else '')
        self.m_richText_application_scene.SetValue(
            self.application_scene[sel] if self.application_scene[sel] != None else '')
        self.m_choice_arg_type.SetSelection(
            self.arg_type[sel] if self.arg_type[sel] != None else config.arg_type_get[0])
        # print config.measurement[0]

        if self.measurement[sel] != None:
            self.m_choice_measurement.SetSelection(self.measurement[sel])

        # self.m_choice_pattern.SetSelection(self.pattern[sel] if self.pattern[sel] != None else 0)
        if self.pattern[sel] != None:
            self.m_choice_pattern.SetSelection(self.pattern[sel])
        # print self.uncertainty_kind[sel]
        # self.m_choice_uncertainty_kind.SetSelection(self.uncertainty_kind[sel] if self.uncertainty_kind[sel] != None else 0)
        if self.uncertainty_kind[sel] != None:
            self.m_choice_uncertainty_kind.SetSelection(self.uncertainty_kind[sel])
        # print config.dis_index_set[config.dis_type_get[self.dis_type[sel]]]
        if self.dis_type[sel] != None:
            self.m_choice_dis_type.SetSelection(
                config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]])
            # self.m_choice_dis_type.SetSelection(config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]] if self.dis_type[sel] != None else 0)
        if self.m_choice_dis_type.GetSelection() == 0:
            self.m_staticText_dis_arg_1.SetLabelText('mu')
            self.m_staticText_dis_arg_2.SetLabelText('sigma')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 1:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_p2.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 2:
            self.m_staticText_dis_arg_1.SetLabelText('theta')
            self.m_staticText_dis_arg_2.Hide()
            self.m_textCtrl_dis_arg_2.Hide()
            # self.m_staticText_func.Hide()
            # self.m_textCtrl_func.Hide()
            self.m_button_other.Hide()
        elif self.m_choice_dis_type.GetSelection() == 3:
            self.m_staticText_dis_arg_1.SetLabelText('上界')
            self.m_staticText_dis_arg_2.SetLabelText('下界')
            # self.m_staticText_dis_arg_1.Show(True)
            self.m_staticText_dis_arg_2.Show(True)
            self.m_textCtrl_dis_arg_2.Show(True)
            # self.m_staticText_func.Show(True)
            # self.m_textCtrl_func.Show(True)
            self.m_button_other.Show(True)
        # self.m_choice_measurement.SetSelection(self.measurement[sel] if self.measurement[sel] != None else 0)
        # self.m_choice_pattern.SetSelection(self.pattern[sel] if self.pattern[sel] != None else 0)
        # # print self.uncertainty_kind[sel]
        # self.m_choice_uncertainty_kind.SetSelection(
        #     self.uncertainty_kind[sel] if self.uncertainty_kind[sel] != None else 0)
        # # print config.dis_index_set[config.dis_type_get[self.dis_type[sel]]]
        # self.m_choice_dis_type.SetSelection(
        #     config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]] if self.dis_type[sel] != None else 0)
        getCauseList = []
        getEffectList = []

        CauseList = self.arg_descr[:]
        del CauseList[sel]
        # print '-------**-----'
        # print CauseList
        # print '--------@@----'

        EffectList = self.arg_descr[:]
        del EffectList[sel]
        # print '-------**-----'
        # print EffectList
        # print '--------@@----'
        self.m_checkList_cause.Set(CauseList)
        # self.m_checkList_effect.Clear()
        self.m_checkList_effect.Set(EffectList)

        for index in self.cause[sel]:
            if index != "":
                getCauseList.append(CauseList.index(index))
        self.m_checkList_cause.SetCheckedItems(getCauseList)
        for index in self.effect[sel]:
            if index != "":
                getEffectList.append(EffectList.index(index))
        self.m_checkList_effect.SetCheckedItems(getEffectList)

        # show_panel.grid.SetCellValue(index, 3, config.arg_type_get[show_panel.params[index][5]]
        print "hahahahah", sel
        print text


    def OnReSize(self, event, show_panel):
        show_panel.Layout()
#         在绑定的size事件中使右下角保存panel右对齐
        x, y = show_panel.btmPanel.GetSize()
        w, h = show_panel.savePanel.GetSize()
        show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
        show_panel.Layout()

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



    def saveUncertainty_all(self, event):
        show_panel = self.GetCurrentPage()
        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # updateInformations = "update model_arg set arg_descr = %s, arg_name = %s, arg_unit = %s , arg_type = %s, dis_type=%s, " \
            #                      "dis_arg = %s, uncertainty_kind = %s," \
            #                      " measurement = %s, cause = %s, effect = %s, " \
            #                      "pattern = %s, life_time = %s, application_scene = %s where arg_id = %s"
            for index in range(len(show_panel.params)):
                # arg_type = config.arg_type_set[show_panel.grid.GetCellValue(index, 3).encode("utf-8")]
                # dis_type = config.dis_type_set[show_panel.grid.GetCellValue(index, 4).encode("utf-8")]
                # dis_value = show_panel.grid.GetCellValue(index, 5)
                # uncertainty_kind = config.uncertaintyKind_set[show_panel.grid.GetCellValue(index, 2).encode("utf-8")]
                # measurement = config.measurement_set[show_panel.grid.GetCellValue(index, 3).encode("utf-8")]
                # cause = show_panel.grid.GetCellValue(index, 4)
                # effect = show_panel.grid.GetCellValue(index, 5)
                # pattern = config.pattern_set[show_panel.grid.GetCellValue(index, 6).encode("utf-8")]
                # life_time = show_panel.grid.GetCellValue(index, 7)
                # application_scene = show_panel.grid.GetCellValue(index, 8)
                cursor.execute(Sql.updateInformations, (self.arg_descr[index], self.arg_name[index], self.arg_unit[index],
                                                        self.arg_type[index],self.dis_type[index], self.dis_arg[index],
                                                        self.uncertainty_kind[index], self.measurement[index], self.cause_return[index],
                                                        self.effect_return[index], self.pattern[index], self.life_time[index], self.application_scene[index],
                                                        self.arg_id[index]))
            conn.commit()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        self.DeletePage(self.GetPageIndex(show_panel))

    def cancelUncertainty(self, event):
        show_panel = self.GetCurrentPage()
        # db_config = config.datasourse
        # try:
        #     conn = mysql.connector.connect(**db_config)
        #     cursor = conn.cursor()
        #     for index in range(len(show_panel.params)):
        #         uncertainty_kind = config.uncertaintyKind_set[show_panel.grid.GetCellValue(index, 2).encode("utf-8")]
        #         measurement = config.measurement_set[show_panel.grid.GetCellValue(index, 3).encode("utf-8")]
        #         cause = show_panel.grid.GetCellValue(index, 4)
        #         effect = show_panel.grid.GetCellValue(index, 5)
        #         pattern = config.pattern_set[show_panel.grid.GetCellValue(index, 6).encode("utf-8")]
        #         life_time = show_panel.grid.GetCellValue(index, 7)
        #         application_scene = show_panel.grid.GetCellValue(index, 8)
        #         cursor.execute(Sql.updateUncertainty, (
        #         uncertainty_kind, measurement, cause, effect, pattern, life_time, application_scene,
        #         show_panel.params[index][1]))
        #     conn.commit()
        # except mysql.connector.Error as e:
        #     print(e)
        # finally:
        #     cursor.close()
        #     conn.close()
        self.DeletePage(self.GetPageIndex(show_panel))


    def next_arg(self, event):
        sel = self.m_listBox_choice_arg.GetSelection()
        text = self.m_listBox_choice_arg.GetString(sel)
        self.arg_descr[sel] = self.m_textCtrl_arg_descr.GetValue().encode("utf-8")
        self.arg_name[sel] = self.m_textCtrl_arg_name.GetValue().encode("utf-8")
        self.arg_unit[sel] = self.m_textCtrl_arg_unit.GetValue().encode("utf-8")
        # print config.arg_type_get[self.m_choice_arg_type.GetSelection()]
        self.arg_type[sel] = config.arg_type_set[config.arg_type_get[self.m_choice_arg_type.GetSelection()]]
        self.dis_type[sel] = config.dis_type_set[config.dis_type_get1[self.m_choice_dis_type.GetSelection()]].encode("utf-8")
        self.dis_arg[sel] = (" " +str(self.m_textCtrl_dis_arg_1.GetValue())+ " " + str(self.m_textCtrl_dis_arg_2.GetValue())).encode("utf-8")
        self.dis_arg_1[sel] = str(self.m_textCtrl_dis_arg_1.GetValue()).encode("utf-8")
        self.dis_arg_2[sel] = str(self.m_textCtrl_dis_arg_2.GetValue()).encode("utf-8")

        self.uncertainty_kind[sel] = config.uncertaintyKind_set[config.uncertaintyKind[self.m_choice_uncertainty_kind.GetSelection()]]
        self.measurement[sel] = config.measurement_set[config.measurement[self.m_choice_measurement.GetSelection()]]
        # temptCauseList = self.m_checkList_cause.GetCheckedStrings()
        string1 = ""

        # for index in range(len(self.m_checkList_cause.CheckedStrings)):
        #     self.cause[sel][index] = self.m_checkList_cause.CheckedStrings[index]
        # for index in range(len(self.m_checkList_effect.CheckedStrings)):
        #     self.effect[sel][index] = self.m_checkList_effect.CheckedStrings[index]

        for index in self.m_checkList_cause.GetCheckedStrings():
            string1 += str(index) + " "

        self.cause_return[sel] = string1.encode("utf-8")

        string2 = ""
        for index in self.m_checkList_effect.GetCheckedStrings():
            string2 += str(index) + " "
        self.effect_return[sel] = string2.encode("utf-8")

        if self.cause_return[sel] !=None:
            self.cause[sel] = self.cause_return[sel].split(" ")
        else:
            self.cause[sel] = ''

        if self.effect_return[sel] !=None:
            self.effect[sel] = self.effect_return[sel].split(" ")
        else:
            self.effect[sel] = ''

        # self.cause.append(self.cause_return[sel].split(" ") if index[8] != None else '')
        # self.effect.append(self.effect_return[sel].split(" ") if index[9] != None else '')

        self.pattern[sel] = config.pattern_set[config.pattern[self.m_choice_pattern.GetSelection()]]

        self.life_time[sel] = (str(self.m_textCtrl_arg_begin_time.GetValue()) + " " + str(self.m_textCtrl_arg_end_time.GetValue())).encode("utf-8")
        self.application_scene[sel] = self.m_richText_application_scene.GetValue().encode("utf-8")

        if sel < self.all_number - 1:
            ShowNotebook.changePage(self,sel+1)
            self.m_listBox_choice_arg.SetSelection(sel+1)
        else:
            ShowNotebook.changePage(self, 0)
            self.m_listBox_choice_arg.SetSelection(0)


        # print self.m_checkList_cause.GetCheckedStrings()


    def saveUncertainty(self, event):
        show_panel = self.GetCurrentPage()
        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            for index in range(len(show_panel.params)):
                uncertainty_kind = config.uncertaintyKind_set[show_panel.grid.GetCellValue(index, 2).encode("utf-8")]
                measurement = config.measurement_set[show_panel.grid.GetCellValue(index, 3).encode("utf-8")]
                cause = show_panel.grid.GetCellValue(index, 4)
                effect = show_panel.grid.GetCellValue(index, 5)
                pattern = config.pattern_set[show_panel.grid.GetCellValue(index, 6).encode("utf-8")]
                life_time = show_panel.grid.GetCellValue(index, 7)
                application_scene = show_panel.grid.GetCellValue(index, 8)
                cursor.execute(Sql.updateUncertainty, (uncertainty_kind, measurement, cause, effect, pattern, life_time, application_scene, show_panel.params[index][1]))
            conn.commit()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        self.DeletePage(self.GetPageIndex(show_panel))


    def onSet(self, event):
        sel = self.m_listBox_choice_arg.GetSelection()
        # text = self.m_listBox_choice_arg.GetString(sel)
        show_panel = self.GetCurrentPage()
        self.para_info = ''

        the_dialog = psw.ParaSettingWindow(self)
        the_dialog.set_origin_info(self.m_choice_dis_type.GetStringSelection())
        # the_dialog.set_origin_info(u'正态分布')
        the_dialog.ShowModal()

        show_panel = self.GetCurrentPage()
        self.m_choice_dis_type.SetSelection(
            config.dis_type_reverse[config.dis_type_get[self.dis_type[sel]]] if self.dis_type[sel] != None else 0)


    def onSet_uncertaintyModule(self, event):
        show_panel = self.GetCurrentPage()
        self.para_info = ''
        self.numberCount = 0
        if event.GetCol() == 8:
            numberCount = 8
            the_dialog = asd.applicationSceneDialog(self)
            the_dialog.set_origin_info(show_panel.grid.GetCellValue(event.GetRow(), 8))
            # the_dialog.set_origin_info(u'正态分布')
            the_dialog.ShowModal()
        elif event.GetCol() == 7:
            numberCount = 7
            the_dialog = ltd.lifeTimeDialog(self)
            # the_dialog.set_origin_info(show_panel.grid.GetCellValue(event.GetRow(), 7))
            # the_dialog.set_origin_info(u'正态分布')
            the_dialog.ShowModal()
        elif event.GetCol() == 5:
            numberCount = 5
            the_dialog = ed.effectDialog(self)
            the_dialog.set_origin_info(show_panel.grid.GetCellValue(event.GetRow(), 5))
            # the_dialog.set_origin_info(u'正态分布')
            the_dialog.ShowModal()
        elif event.GetCol() == 4:
            numberCount = 4
            the_dialog = cd.causeDialog(self)
            the_dialog.set_origin_info(show_panel.grid.GetCellValue(event.GetRow(), 4))
            # the_dialog.set_origin_info(u'正态分布')
            the_dialog.ShowModal()
        else:
            return
        show_panel = self.GetCurrentPage()
        show_panel.grid.SetCellValue(event.GetRow(), numberCount, self.para_info)

    # def uncertaintyDis(self, pProj = 0):
    #
    #     self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
    #                                wx.DefaultSize, wx.TAB_TRAVERSAL)
    #     modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
    #     title = u"不确定性设置" + u'（模型：' + modelinfo[0][0] + ')'
    #     self.AddPage(self.show_panel, title, True, wx.NullBitmap)
    #     show_panel = self.show_panel
    #     show_panel.pid = pProj
    #     show_panel.params = Sql.selectSql((pProj,), Sql.selectUncertainty)
    #     # show_panel 的布局，只有 scrollPanel 一个元素
    #     show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
    #     #为实现滚动条加入 scrollPanel
    #     show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY,
    #                                                   wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
    #     show_panel.scrolledWindow.SetScrollRate(5, 5)
    #     scrollPanel = show_panel.scrolledWindow
    #     # scrollPanel 的布局，元素为显示的控件
    #     show_panel.gbSizer = wx.GridBagSizer(5, 5)
    #     show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
    #     show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
    #
    #     show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"请设置不确定参数情况：",
    #                                            wx.DefaultPosition, wx.DefaultSize, 0)
    #     show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
    #                            wx.GBSpan(1, 1), wx.ALL, 5)
    #
    #     show_panel.grid = grid.Grid(scrollPanel, wx.ID_ANY,
    #                                 wx.DefaultPosition, wx.DefaultSize, 0)
    #     # 参数表格
    #     show_panel.grid.CreateGrid(len(show_panel.params), 9)
    #     # set the form of every cell
    #     show_panel.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTRE)
    #     # set the size of 1st column
    #     show_panel.grid.SetColSize(0, 200)
    #     show_panel.grid.SetColSize(2, 150)
    #     show_panel.grid.SetColSize(6, 150)
    #     # show_panel.grid.SetColSize(3, 150)
    #     # show_panel.grid.SetColSize(3, 150)
    #     # -------------ADD---------------
    #     show_panel.grid.SetColLabelValue(0, "参数描述")
    #     show_panel.grid.SetColLabelValue(1, "参数名")
    #     show_panel.grid.SetColLabelValue(2, "不确定性类型")
    #     for i in range(len(show_panel.params)):
    #         show_panel.grid.SetCellEditor(i, 2, grid.GridCellChoiceEditor(
    #             config.uncertaintyKind.values()))
    #     show_panel.grid.SetColLabelValue(3, "度量方法")
    #     for i in range(len(show_panel.params)):
    #         show_panel.grid.SetCellEditor(i, 3, grid.GridCellChoiceEditor(
    #             config.measurement.values()))
    #     show_panel.grid.SetColLabelValue(4, "起因")
    #     show_panel.grid.SetColLabelValue(5, "影响")
    #     show_panel.grid.SetColLabelValue(6, "不确定性模式")
    #     for i in range(len(show_panel.params)):
    #         show_panel.grid.SetCellEditor(i, 6, grid.GridCellChoiceEditor(
    #             config.pattern.values()))
    #     show_panel.grid.SetColLabelValue(7, "时间周期")
    #     show_panel.grid.SetColLabelValue(8, "应用场景")
    #
    #     # update the date from sql
    #     for index in range(len(show_panel.params)):
    #         show_panel.grid.SetCellValue(index, 0, show_panel.params[index][2])
    #         show_panel.grid.SetCellValue(index, 1, show_panel.params[index][0])
    #
    #         show_panel.grid.SetCellValue(index, 2, config.uncertaintyKind[show_panel.params[index][3]]
    #         if show_panel.params[index][3] != None else '')
    #         # if show_panel.params[index][4] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 3, config.measurement[show_panel.params[index][4]]
    #         if show_panel.params[index][4] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 4, show_panel.params[index][5]
    #         if show_panel.params[index][5] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 5, show_panel.params[index][6]
    #         if show_panel.params[index][6] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 6, config.pattern[show_panel.params[index][7]]
    #         if show_panel.params[index][7] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 7, show_panel.params[index][8]
    #         if show_panel.params[index][8] != None else '')
    #
    #         show_panel.grid.SetCellValue(index, 8, show_panel.params[index][9]
    #         if show_panel.params[index][9] != None else '')
    #
    #         # show_panel.grid.SetCellValue(index, 6, '双击此处设置')
    #         # # set the color of the 7th column
    #         # show_panel.grid.SetCellBackgroundColour(index, 6, wx.LIGHT_GREY)
    #
    #         # for i in range(3):
    #         #     show_panel.grid.SetReadOnly(index, i)
    #         # show_panel.grid.SetReadOnly(index, 5)
    #         show_panel.grid.SetReadOnly(index, 0)
    #         show_panel.grid.SetReadOnly(index, 1)
    #         show_panel.grid.SetReadOnly(index, 4)
    #         show_panel.grid.SetReadOnly(index, 5)
    #         show_panel.grid.SetReadOnly(index, 7)
    #         show_panel.grid.SetReadOnly(index, 8)
    #     # create new form if the button be clicked
    #     show_panel.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onSet_uncertaintyModule)
    #     # to be continued
    #     show_panel.gbSizer.Add(show_panel.grid, wx.GBPosition(3, 4),
    #                            wx.GBSpan(1, 6), wx.ALL, 5)
    #
    #     #分割线
    #     show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition,
    #                                           wx.DefaultSize, wx.LI_HORIZONTAL)
    #
    #     # 下方btmPanel
    #     show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition,
    #                                    (-1, 40), wx.TAB_TRAVERSAL)
    #     show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
    #                                     (280, 28), wx.TAB_TRAVERSAL)
    #     '''
    #     show_panel.check = wx.Button(show_panel.savePanel, wx.ID_ANY, u"LL",
    #                                 (105, 0), (30, 28), 0)
    #     show_panel.check.Bind(wx.EVT_BUTTON, self.ShowContent)
    #     '''
    #     show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"保存",
    #                                 (0, 0), (100, 28), 0)
    #     show_panel.save.Bind(wx.EVT_BUTTON, self.saveUncertainty)
    #     show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
    #                                   (140, 0), (100, 28), 0)
    #     show_panel.cancel.Bind(wx.EVT_BUTTON, self.cancelUncertainty)
    #
    #     #         show_panel布局设置
    #     scrollPanel.SetSizer(show_panel.gbSizer)
    #     scrollPanel.Layout()
    #     show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND |wx.ALL, 5 )
    #     show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
    #     show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
    #     show_panel.SetSizer(show_panel.bSizer)
    #     show_panel.Layout()
    #
    #     #         初始化savePanel位置
    #     x, y = show_panel.btmPanel.GetSize()
    #     w, h = show_panel.savePanel.GetSize()
    #     show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
    #
    #     #         show_panel.Bind(wx.EVT_SIZE, self.OnReSize)
    #     show_panel.Bind(wx.EVT_SIZE,
    #                     lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))
    # def formulaDis(self, pProj = 0):
    #
    #     self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
    #                                wx.DefaultSize, wx.TAB_TRAVERSAL)
    #     modelinfo = Sql.selectSql(args=(pProj,), sql=Sql.selectModel)
    #     title = u"公式展示" + u'（模型：' + modelinfo[0][0] + ')'
    #     self.AddPage(self.show_panel, title, True, wx.NullBitmap)
    #     show_panel = self.show_panel
    #     show_panel.pid = pProj
    #     show_panel.params = Sql.selectSql((pProj,), Sql.selectInfromations)
    #
    #
    #     self.theLastParams = show_panel.params
    #
    #     self.effect = []
    #     # self.cause = []
    #     self.paramsName = []
    #     tempt = []
    #
    #     for index in range(len(self.theLastParams)):
    #         self.paramsName.append(self.theLastParams[index][0])
    #         tempt = self.theLastParams[index][8].split(" ")
    #         for indexInner in range(len(tempt)):
    #             self.effect.append([self.paramsName[index],tempt[indexInner]])
    #
    #     pp.showPanel(self)
    #
    #
    #     # show_panel 的布局，只有 scrollPanel 一个元素
    #     show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
    #     #为实现滚动条加入 scrollPanel
    #     show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY,
    #                                                   wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
    #     show_panel.scrolledWindow.SetScrollRate(5, 5)
    #     scrollPanel = show_panel.scrolledWindow
    #     # scrollPanel 的布局，元素为显示的控件
    #     show_panel.gbSizer = wx.GridBagSizer(5, 5)
    #     show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
    #     show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
    #
    #     self.theScrollPanel = scrollPanel
    #
    #     self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     self.theScrollPanel.SetSizer(self.sizer)
    #
    #     scrollPanel.m_panel_list = wx.Panel(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
    #     bSizer9 = wx.BoxSizer(wx.VERTICAL)
    #     scrollPanel.m_panel_list.SetSizer(bSizer9)
    #
    #     scrollPanel.m_staticText7 = wx.StaticText(scrollPanel.m_panel_list, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
    #     bSizer9.Add(scrollPanel.m_staticText7, 0, wx.ALL, 5)
    #
    #     # m_listBox1Choices = [ u"1拉普拉斯", u"2古尔丹", u"3", u"4", u"clear"]
    #     m_listBox1Choices = scrollPanel.paramsName
    #     m_listBox1 = wx.ListBox(scrollPanel.m_panel_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox1Choices, wx.LB_ALWAYS_SB)
    #     m_listBox1.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
    #     bSizer9.Add(m_listBox1, 1, wx.ALL | wx.EXPAND, 5)
    #     # scrollPanel.sizer.Add(m_listBox1, 1, wx.ALL | wx.EXPAND, 5)
    #     scrollPanel.sizer.Add(scrollPanel.m_panel_list, 1, wx.EXPAND |wx.ALL, 5)
    #
    #     scrollPanel.m_panel_showPicture = wx.Panel(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
    #     bSizer10 = wx.BoxSizer(wx.VERTICAL)
    #     scrollPanel.m_panel_showPicture.SetSizer(bSizer10)
    #
    #     scrollPanel.m_staticText8 = wx.StaticText(scrollPanel.m_panel_showPicture, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
    #     bSizer10.Add(scrollPanel.m_staticText8, 0, wx.ALL, 5)
    #
    #     # 重置Image对象尺寸的函数
    #     # def resizeBitmap(image, width=100, height=100):
    #     #     bmp = image.Scale(width, height).ConvertToBitmap()
    #     #     return bmp
    #
    #     image1 = wx.Image('ba.png', wx.BITMAP_TYPE_PNG).Rescale(640, 480).ConvertToBitmap()
    #     bmp1 = wx.StaticBitmap(scrollPanel.m_panel_showPicture, wx.ID_ANY, wx.Bitmap( image1 ), wx.DefaultPosition, wx.DefaultSize, 0 )  # 转化为wx.StaticBitmap()形式
    #     # resizeBitmap(image1, 200, 200)
    #     bSizer10.Add(bmp1, 1, flag=wx.ALL | wx.EXPAND, border=5)
    #     scrollPanel.sizer.Add(scrollPanel.m_panel_showPicture, 3, wx.EXPAND | wx.ALL, 5)
    #
    #     scrollPanel.m_panel_list.Layout()
    #     scrollPanel.m_panel_showPicture.Layout()
    #
    #
    #
    # # self.figure = Figure()
    #     # self.axes = self.figure.add_subplot(111)
    #     # self.canvas = FigureCanvas(show_panel, -1, self.figure)
    #     # self.canvas.SetMinSize((460, 250))
    #     # self.canvas.SetMaxSize((460, 250))
    #     #
    #     # self.sizer.Add(self.canvas)
    #
    #
    #
    #     # pp.showPanel(self)
    #     # show_panel.gbSizer.Add(show_panel.plotPanel, wx.GBPosition(2, 4),
    #     #                        wx.GBSpan(1, 1), wx.ALL, 5)
    #
    #
    #
    #     #分割线
    #     show_panel.staticline = wx.StaticLine(show_panel, wx.ID_ANY, wx.DefaultPosition,
    #                                           wx.DefaultSize, wx.LI_HORIZONTAL)
    #
    #     # 下方btmPanel
    #     show_panel.btmPanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition,
    #                                    (-1, 40), wx.TAB_TRAVERSAL)
    #     show_panel.savePanel = wx.Panel(show_panel.btmPanel, wx.ID_ANY, wx.DefaultPosition,
    #                                     (280, 28), wx.TAB_TRAVERSAL)
    #     '''
    #     show_panel.check = wx.Button(show_panel.savePanel, wx.ID_ANY, u"LL",
    #                                 (105, 0), (30, 28), 0)
    #     show_panel.check.Bind(wx.EVT_BUTTON, self.ShowContent)
    #     '''
    #     show_panel.save = wx.Button(show_panel.savePanel, wx.ID_ANY, u"确定",
    #                                 (0, 0), (100, 28), 0)
    #     show_panel.save.Bind(wx.EVT_BUTTON, self.saveUncertainty_new)
    #     show_panel.cancel = wx.Button(show_panel.savePanel, wx.ID_ANY, u"取消",
    #                                   (140, 0), (100, 28), 0)
    #     show_panel.cancel.Bind(wx.EVT_BUTTON, self.cancelUncertainty)
    #
    #     #         show_panel布局设置
    #     # scrollPanel.SetSizer(show_panel.gbSizer)
    #     scrollPanel.Layout()
    #     show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND |wx.ALL, 5 )
    #     show_panel.bSizer.Add(show_panel.staticline, 0, wx.EXPAND |wx.ALL, 5)
    #     show_panel.bSizer.Add(show_panel.btmPanel, 0, wx.EXPAND | wx.ALL, 5)
    #     show_panel.SetSizer(show_panel.bSizer)
    #     show_panel.Layout()
    #
    #     #         初始化savePanel位置
    #     x, y = show_panel.btmPanel.GetSize()
    #     w, h = show_panel.savePanel.GetSize()
    #     show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
    #
    #     #         show_panel.Bind(wx.EVT_SIZE, self.OnReSize)
    #     show_panel.Bind(wx.EVT_SIZE,
    #                     lambda evt, show_panel=show_panel : self.OnReSize(evt, show_panel))
