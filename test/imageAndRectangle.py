# -*- coding: utf-8 -*-

import wx
from copy import deepcopy

class MyFrame(wx.Frame):
    isLeftDown = False

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, size=wx.Size(500, 500))
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel = wx.Panel(self, wx.ID_ANY)
        bSizer1.Add(self.m_panel, 3, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(bSizer1)

        self.ImageBMP = wx.StaticBitmap(self.m_panel, wx.ID_ANY, wx.Bitmap("googles.png"))

        # bind event
        self.ImageBMP.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.ImageBMP.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.ImageBMP.Bind(wx.EVT_MOTION, self.OnMove)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        self.m_panel.SetFocus()

    boundaries = []

    def drawRectangle(self, pos, pos2):
        dc = wx.ClientDC(self.ImageBMP)
        dc.SetBrush( wx.TRANSPARENT_BRUSH )
        dc.SetPen(wx.Pen(wx.Colour(0,0,255)) )
        dc.DrawRectangle(pos[0], pos[1], pos2[0]-pos[0], pos2[1]-pos[1])
        self.boundaries.append([pos[0], pos[1], pos2[0]-pos[0], pos2[1]-pos[1]])

    pos = None
    pos2 = None
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

    def OnKeyDown(self, event=None):
        keycode = event.GetKeyCode()
        print(keycode, wx.WXK_DELETE)
        if keycode == wx.WXK_DELETE:
            print(self.boundaries)
            self.boundaries.clear()
            self.ImageBMP = wx.StaticBitmap(self.m_panel, wx.ID_ANY, wx.Bitmap("googles.png"))

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()
