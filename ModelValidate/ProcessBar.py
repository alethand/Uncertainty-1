# -*- coding: utf-8 -*-
import time
import wx


class ProcessBar(wx.Frame):
    def __init__(self, parent, title, time_range):
        super(ProcessBar, self).__init__(parent, title=title, size=(300, 200))
        self.range = time_range
        self.count = 0
        panel = wx.Panel(self)
        self.gauge = wx.Gauge(panel, range=self.range, size=(250, 25), style=wx.GA_HORIZONTAL)
        v_box = wx.BoxSizer(wx.VERTICAL)
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        h_box.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
        v_box.Add((0, 30))
        v_box.Add(h_box, flag=wx.ALIGN_CENTRE)
        v_box.Add((0, 20))
        panel.SetSizer(v_box)
        self.SetSize((300, 200))
        self.Centre()
        self.Show(True)

    def set_process(self, count, end=0):
        if end == 1:  # 快速结束进度条
            while True:
                time.sleep(0.001)
                count += 1
                self.gauge.SetValue(count)
                if count >= self.range*3/2:
                    return
        else:  # 按count 设置进度条
            self.gauge.SetValue(count)

    def start_loading(self):
        while True:
            self.gauge.SetValue(self.count)
            self.count += 1
            time.sleep(0.002)
            if self.count >= self.range*5/4:
                break

    def end_loading(self, end_info):
        time.sleep(0.5)
        self.Destroy()
        dlg = wx.MessageDialog(None, end_info, u'提示')
        dlg.ShowModal()

    def loadFunction(self,end_info,func,*args):
        self.start_loading()
        res=func(*args)
        self.end_loading(end_info)
        return res