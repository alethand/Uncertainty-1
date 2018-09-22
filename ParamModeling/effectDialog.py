# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class applicationSceneDialog
###########################################################################

class effectDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"影响", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_showText = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_showText.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gbSizer_showText = wx.GridBagSizer(0, 0)
        gbSizer_showText.SetFlexibleDirection(wx.BOTH)
        gbSizer_showText.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_richText_application = wx.richtext.RichTextCtrl(self.m_panel_showText, wx.ID_ANY, wx.EmptyString,
                                                               wx.DefaultPosition, wx.Size(470, 190),
                                                               0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.m_richText_application.Enable(False)
        gbSizer_showText.Add(self.m_richText_application, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)


        self.m_panel_showText.SetSizer(gbSizer_showText)
        self.m_panel_showText.Layout()
        gbSizer_showText.Fit(self.m_panel_showText)
        bSizer_main.Add(self.m_panel_showText, 3, wx.EXPAND | wx.ALL, 5)

        self.m_panel_button = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_button.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer_button = wx.GridSizer(1, 4, 0, 0)

        gSizer_button.AddSpacer(1)

        gSizer_button.AddSpacer(1)

        self.m_button_edit = wx.Button(self.m_panel_button, wx.ID_ANY, u"编辑", wx.Point(0, 3), wx.DefaultSize, 0)
        gSizer_button.Add(self.m_button_edit, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button_ok = wx.Button(self.m_panel_button, wx.ID_ANY, u"确定", wx.Point(0, 5), wx.DefaultSize, 0)
        gSizer_button.Add(self.m_button_ok, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_panel_button.SetSizer(gSizer_button)
        self.m_panel_button.Layout()
        gSizer_button.Fit(self.m_panel_button)
        bSizer_main.Add(self.m_panel_button, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_edit.Bind(wx.EVT_BUTTON, self.edit_applicationScene)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.ok_applicationScene)

    def __del__(self):
        pass

    def set_origin_info(self, info):
        self.onChangeChoice(None, info)

    # Virtual event handlers, overide them in your derived class
    def edit_applicationScene(self, event):
        self.m_richText_application.Enable(True)
        event.Skip()

    def ok_applicationScene(self, event):
        self.GetParent().para_info = (self.m_richText_application.GetValue())
        print(self.GetParent().para_info)
        self.Destroy()
        # event.Skip()

    def onChangeChoice(self, event, info):
        self.m_richText_application.Clear()
        self.m_richText_application.SetValue(info)





if __name__ == '__main__':
    app = wx.App(False)
    frame = effectDialog(None)
    frame.Show()
    app.MainLoop()