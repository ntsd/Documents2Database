# -*- coding: utf-8 -*-

import wx

class MyFrame(wx.Frame):
    isLeftDown = False

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, size=wx.Size(500, 500))
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel = wx.Panel(self, wx.ID_ANY)
        bSizer1.Add(self.m_panel, 3, wx.EXPAND | wx.ALL, 5)

        self.bmp = wx.EmptyBitmap(500, 500)
        self.staticBMP = wx.StaticBitmap(self.m_panel, wx.ID_ANY, self.bmp)

        self.SetSizer(bSizer1)

        # bind event
        self.staticBMP.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.staticBMP.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.staticBMP.Bind(wx.EVT_MOTION, self.OnMove)

    def drawRectangle(self, pos, pos2):
        dc = wx.ClientDC(self.staticBMP)
        dc.SetBrush( wx.TRANSPARENT_BRUSH )
        dc.SetPen(wx.Pen(wx.Colour(0,0,255)) )
        dc.DrawRectangle(pos[0], pos[1], pos2[0]-pos[0], pos2[1]-pos[1])


    pos = None
    def OnLeftDown(self, event):
        self.pos = event.GetPosition()
        self.pos2 = event.GetPosition()
        self.isLeftDown = True

    def OnLeftUp(self, event):
        self.isLeftDown = False
        self.drawRectangle(self.pos, self.pos2)

    def OnMove(self, event):
        if self.isLeftDown:
            self.pos2 = event.GetPosition()
            #dc = wx.ClientDC(self.staticBMP)
            #dc.DrawBitmap(self.bmp, 0, 0)



if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()