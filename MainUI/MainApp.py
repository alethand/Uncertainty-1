# -*- coding: utf-8 -*-

import wx
import guiManager


class MainAPP(wx.App):
    
    # 初始打开登录界面
    def OnInit(self):
        self.manager = guiManager.GuiManager(self.UpdateUI)
        self.frame = self.manager.GetFrame(0, {})
        self.frame.Show()
        return True
    
    # 登录或注销时切换Frame
    def UpdateUI(self, ftype, params = {}):
        self.frame.Destroy()
        self.frame = self.manager.GetFrame(ftype, params)
        self.frame.Show(True)

def main():
    app = MainAPP()
    app.MainLoop()

if __name__ == '__main__':
    main()