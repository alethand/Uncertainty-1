# -*- coding: utf-8 -*-

import wx
import wx.xrc
import config


class ParaSettingWindow(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                           title=u"分布参数设置", size=wx.Size(500, 300))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_kind = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_kind.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        bSizer_kind = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_kind = wx.StaticText(self.m_panel_kind, wx.ID_ANY, u"分布类型", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.m_staticText_kind.Wrap(-1)
        bSizer_kind.Add(self.m_staticText_kind, 0, wx.ALL, 5)

        m_choice_kindChoices = [u"正态分布", u"均匀分布", u"指数分布", u"任意分布"]
        self.m_choice_kind = wx.Choice(self.m_panel_kind, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       m_choice_kindChoices, 0)
        self.m_choice_kind.SetSelection(0)
        self.m_choice_kind.Bind(wx.EVT_CHOICE, self.onChangeChoice)
        bSizer_kind.Add(self.m_choice_kind, 0, wx.ALL, 5)

        self.m_panel_kind.SetSizer(bSizer_kind)
        self.m_panel_kind.Layout()
        bSizer_kind.Fit(self.m_panel_kind)
        bSizer_main.Add(self.m_panel_kind, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_para = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_para.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gbSizer_para = wx.GridBagSizer(0, 0)
        gbSizer_para.SetFlexibleDirection(wx.BOTH)
        gbSizer_para.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        gbSizer_para.SetEmptyCellSize(wx.Size(3, 5))

        self.m_staticText_p1 = wx.StaticText(self.m_panel_para, wx.ID_ANY, u"参数1", wx.Point(0, 1), wx.DefaultSize, 0)
        self.m_staticText_p1.Wrap(-1)
        gbSizer_para.Add(self.m_staticText_p1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_p1 = wx.TextCtrl(self.m_panel_para, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       0)
        gbSizer_para.Add(self.m_textCtrl_p1, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText_p2 = wx.StaticText(self.m_panel_para, wx.ID_ANY, u"参数2", wx.Point(1, 1), wx.DefaultSize, 0)
        self.m_staticText_p2.Wrap(-1)
        gbSizer_para.Add(self.m_staticText_p2, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_p2 = wx.TextCtrl(self.m_panel_para, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       0)
        gbSizer_para.Add(self.m_textCtrl_p2, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText_func = wx.StaticText(self.m_panel_para, wx.ID_ANY, u"概率密度函数", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText_func.Wrap(-1)
        gbSizer_para.Add(self.m_staticText_func, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_func = wx.TextCtrl(self.m_panel_para, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       0)
        gbSizer_para.Add(self.m_textCtrl_func, wx.GBPosition(2, 2), wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_button_select_file = wx.Button(self.m_panel_para, wx.ID_ANY, u"选择文件", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button_select_file.Bind(wx.EVT_BUTTON, self.chooseFile)
        gbSizer_para.Add(self.m_button_select_file, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_panel_para.SetSizer(gbSizer_para)
        self.m_panel_para.Layout()
        gbSizer_para.Fit(self.m_panel_para)
        bSizer_main.Add(self.m_panel_para, 3, wx.EXPAND | wx.ALL, 5)

        self.m_panel_ok = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_ok.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer_ok = wx.GridSizer(1, 4, 0, 0)

        gSizer_ok.AddSpacer(1)
        gSizer_ok.AddSpacer(1)

        self.m_button_ok = wx.Button(self.m_panel_ok, wx.ID_ANY, u"确定", wx.Point(0, 3), wx.DefaultSize, 0)
        gSizer_ok.Add(self.m_button_ok, 0, wx.ALL, 5)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.onClickOK)

        self.m_button_cancel = wx.Button(self.m_panel_ok, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer_ok.Add(self.m_button_cancel, 0, wx.ALL, 5)
        self.m_button_cancel.Bind(wx.EVT_BUTTON, self.onClickCancel)

        self.m_panel_ok.SetSizer(gSizer_ok)
        self.m_panel_ok.Layout()
        gSizer_ok.Fit(self.m_panel_ok)
        bSizer_main.Add(self.m_panel_ok, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def set_origin_info(self, info):
        self.m_choice_kind.SetSelection(config.dis_index_set.get(info))
        self.onChangeChoice(None)

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
        self.m_textCtrl_p1.Clear()
        self.m_textCtrl_p2.Clear()
        self.m_textCtrl_func.Clear()
        if self.m_choice_kind.GetSelection() == 0:
            self.m_staticText_p1.SetLabelText('mu')
            self.m_staticText_p2.SetLabelText('sigma')
            self.m_staticText_p2.Show(True)
            self.m_textCtrl_p2.Show(True)
            self.m_staticText_func.Hide()
            self.m_textCtrl_func.Hide()
            self.m_button_select_file.Hide()
        elif self.m_choice_kind.GetSelection() == 1:
            self.m_staticText_p1.SetLabelText('上界')
            self.m_staticText_p2.SetLabelText('下界')
            self.m_staticText_p2.Show(True)
            self.m_textCtrl_p2.Show(True)
            self.m_staticText_func.Hide()
            self.m_textCtrl_func.Hide()
            self.m_button_select_file.Hide()
        elif self.m_choice_kind.GetSelection() == 2:
            self.m_staticText_p1.SetLabelText('theta')
            self.m_staticText_p2.Hide()
            self.m_textCtrl_p2.Hide()
            self.m_staticText_func.Hide()
            self.m_textCtrl_func.Hide()
            self.m_button_select_file.Hide()
        elif self.m_choice_kind.GetSelection() == 3:
            self.m_staticText_p1.SetLabelText('上界')
            self.m_staticText_p2.SetLabelText('下界')
            self.m_staticText_p2.Show(True)
            self.m_textCtrl_p2.Show(True)
            self.m_staticText_func.Show(True)
            self.m_textCtrl_func.Show(True)
            self.m_button_select_file.Show(True)

    def onClickOK(self, event):
        self.GetParent().para_info = (self.m_textCtrl_func.GetValue() + ' '
                                      + self.m_textCtrl_p1.GetValue() + ' '
                                      + self.m_textCtrl_p2.GetValue())
        print(self.GetParent().para_info)
        self.Destroy()

    def onClickCancel(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = ParaSettingWindow(None)
    frame.Show()
    app.MainLoop()