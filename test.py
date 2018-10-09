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
## Class MyPanel1
###########################################################################

class MyPanel1(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(712, 511),
                          style=wx.TAB_TRAVERSAL)

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_para = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_para.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        m_listBox5Choices = []
        self.m_listBox5 = wx.ListBox(self.m_panel_para, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     m_listBox5Choices, 0)
        fgSizer3.Add(self.m_listBox5, 1, wx.ALL, 5)

        self.m_panel18 = wx.Panel(self.m_panel_para, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel18.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        fgSizer3.Add(self.m_panel18, 4, wx.EXPAND | wx.ALL, 5)

        self.m_panel_para.SetSizer(fgSizer3)
        self.m_panel_para.Layout()
        fgSizer3.Fit(self.m_panel_para)
        bSizer_main.Add(self.m_panel_para, 4, wx.EXPAND | wx.ALL, 5)

        self.m_panel7 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel7.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer3 = wx.GridSizer(1, 3, 0, 0)

        gSizer3.AddSpacer((0, 0), 1, 0, 5)

        self.m_button_ok = wx.Button(self.m_panel7, wx.ID_ANY, u"确定", wx.Point(0, 3), wx.DefaultSize, 0)
        gSizer3.Add(self.m_button_ok, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel7.SetSizer(gSizer3)
        self.m_panel7.Layout()
        gSizer3.Fit(self.m_panel7)
        bSizer_main.Add(self.m_panel7, 1, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        # Connect Events
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.ok_function)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def ok_function(self, event):
        event.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyPanel1(None)
    frame.Show()
    app.MainLoop()