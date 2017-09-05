import random
import wx

########################################################################
class TabPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent, page):
        """"""
        wx.Panel.__init__(self, parent=parent)
        self.page = page

        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))

        btn = wx.Button(self, label="Change Selection")
        btn.Bind(wx.EVT_BUTTON, self.onChangeSelection)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    #----------------------------------------------------------------------
    def onChangeSelection(self, event):
        """
        Change the page!
        """
        notebook = self.GetParent()
        notebook.SetSelection(self.page)

########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Notebook Tutorial",
                          size=(600,400)
                          )
        panel = wx.Panel(self)

        notebook = wx.Notebook(panel)
        tabOne = TabPanel(notebook, 1)
        notebook.AddPage(tabOne, "Tab 1")

        tabTwo = TabPanel(notebook, 0)
        notebook.AddPage(tabTwo, "Tab 2")

        tabTwo = TabPanel(notebook, 2)
        notebook.AddPage(tabTwo, "Tab 3")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()