import wx
from wx import aui
class TestPanel(wx.Panel):
    """ Simple class example for wx.aui.AuiNotebook. """

    def __init__(self, parent):
        """ Class constructor. """

        wx.Panel.__init__(self, parent, -1)

        # Create the wx.aui.AuiNotebook
        self.nb = wx.aui.AuiNotebook(self)

        # Create a simple text control
        page = wx.TextCtrl(self.nb, -1, "Hello World!", style=wx.TE_MULTILINE)
        # Add the text control as wx.aui.AuiNotebook page
        self.nb.AddPage(page, "Welcome")

        # Add some more pages to the wx.aui.AuiNotebook
        for num in range(1, 5):
            page = wx.TextCtrl(self.nb, -1, "This is page %d" % num, style=wx.TE_MULTILINE)
            self.nb.AddPage(page, "Tab Number %d" % num)

        # Put the wx.aui.AuiNotebook in a sizer and
        # assign the sizer to the main panel
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

# Create a wx.App instance
app = wx.App(0)

# This is our main application frame
frame = wx.Frame(None, -1, "wx.aui.AuiNotebook Sample")
panel = TestPanel(frame)

# Center the frame and show it
frame.CenterOnScreen()
frame.Show()

# Run the MainLoop(), we are done.
app.MainLoop()