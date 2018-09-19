import wx
class CustomedScrolledWindow(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent=parent)
        self.text_ctrl = wx.TextCtrl(self, value='...', style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.Add(self.text_ctrl, flag = wx.EXPAND, proportion=wx.EXPAND)
        self.SetSizer(sizer)
