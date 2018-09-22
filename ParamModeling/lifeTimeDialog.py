# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class lifeTimeDialog
###########################################################################

class lifeTimeDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"时间周期", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_para = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_para.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer7 = wx.GridSizer(2, 2, 0, 0)

        self.m_staticText_startingTime = wx.StaticText(self.m_panel_para, wx.ID_ANY, u"开始时间", wx.DefaultPosition,
                                                       wx.DefaultSize, 0)
        self.m_staticText_startingTime.Wrap(-1)
        gSizer7.Add(self.m_staticText_startingTime, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, 5)

        self.m_textCtrl_startingTime = wx.TextCtrl(self.m_panel_para, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        gSizer7.Add(self.m_textCtrl_startingTime, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.m_staticText_endTime = wx.StaticText(self.m_panel_para, wx.ID_ANY, u"结束时间", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.m_staticText_endTime.Wrap(-1)
        gSizer7.Add(self.m_staticText_endTime, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl_endTime = wx.TextCtrl(self.m_panel_para, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        gSizer7.Add(self.m_textCtrl_endTime, 0, wx.ALL, 5)

        self.m_panel_para.SetSizer(gSizer7)
        self.m_panel_para.Layout()
        gSizer7.Fit(self.m_panel_para)
        bSizer_main.Add(self.m_panel_para, 4, wx.EXPAND | wx.ALL, 5)

        self.m_panel7 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel7.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer3 = wx.GridSizer(1, 3, 0, 0)

        gSizer3.AddSpacer(1)

        self.m_button_ok = wx.Button(self.m_panel7, wx.ID_ANY, u"确定", wx.Point(0, 3), wx.DefaultSize, 0)
        gSizer3.Add(self.m_button_ok, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel7.SetSizer(gSizer3)
        self.m_panel7.Layout()
        gSizer3.Fit(self.m_panel7)
        bSizer_main.Add(self.m_panel7, 1, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.ok_function)

    def __del__(self):
        pass

    def set_origin_info(self, info):
        self.onChangeChoice(None, info)

    def onChangeChoice(self, event, info):
        self.m_textCtrl_startingTime.Clear()
        self.m_textCtrl_endTime.Clear()
        # self.m_textCtrl_startingTime.SetValue(info)
        # self.m_textCtrl_endTime.SetValue(info)

    # Virtual event handlers, overide them in your derived class
    def ok_function(self, event):
        self.GetParent().para_info = (self.m_textCtrl_startingTime.GetValue() + ' '
                                      + self.m_textCtrl_endTime.GetValue())
        print(self.GetParent().para_info)
        self.Destroy()
        # event.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    frame = lifeTimeDialog(None)
    frame.Show()
    app.MainLoop()
