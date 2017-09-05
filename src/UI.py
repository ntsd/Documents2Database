import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel
import os

from PIL import Image
import ImageOCR
import cv2

from Models import Boundary, Customer, Data, PO
from Datasource import saveJson

class ChooseFilePanel(wx.Panel):
    parent = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.currentDirectory = os.getcwd()
        openFileDlgBtn = wx.Button(self, label="Open File")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)

        addImagesButton = wx.Button(self, label="Add Images")
        addImagesButton.Bind(wx.EVT_BUTTON, parent.onAddImagesClick)  # we can use parent.method to call methos in parent

        self.pathsEditText = wx.TextCtrl(parent=self, id=-1, pos=(38, 70), size=(410, 500), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL)

        vbox = wx.BoxSizer(wx.VERTICAL)

        gs = wx.GridSizer(1, 3, 5, 5)

        gs.AddMany([(openFileDlgBtn, 0, wx.EXPAND),
                    (wx.StaticText(self), wx.EXPAND),
                    (addImagesButton, 0, wx.EXPAND)])

        vbox.Add(gs, proportion=1, flag=wx.EXPAND)
        vbox.Add(self.pathsEditText, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=1)
        self.SetSizer(vbox)

    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard="Images, PDF (*.pdf,*.jpg,*.png)|*.pdf;*.jpg;*.png|" \
                     "All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print("You chose the following file(s):")
            self.parent.imagesPaths = []
            for path in paths:
                print("choose path: "+path)
                self.pathsEditText.AppendText(path)
                self.parent.imagesPaths.append(path)
        dlg.Destroy()

class ChooseCustomerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        labelChooseCustomer = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        labelChooseCustomer.SetFont(font)
        labelChooseCustomer.SetLabel("Choose Customer")
        vbox.Add(labelChooseCustomer, flag=wx.ALIGN_CENTER_HORIZONTAL, border=1)

        customerPath = os.getcwd()+"/customers/"
        self.customers = [f for f in os.listdir(customerPath) if os.path.isfile(os.path.join(customerPath, f))]
        self.customerCompoBox = wx.ComboBox(self, choices=self.customers)
        vbox.Add(self.customerCompoBox, flag=wx.ALIGN_CENTER_HORIZONTAL, border=1)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        newCustomerButton = wx.Button(self, label="New")
        newCustomerButton.Bind(wx.EVT_BUTTON, parent.onNewCustomerClick)
        hbox.Add(newCustomerButton, border=1)

        chooseCustomerButton= wx.Button(self, label="Choose")
        chooseCustomerButton.Bind(wx.EVT_BUTTON, parent.onChooseCustomerClick)
        hbox.Add(chooseCustomerButton, border=1)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=1)


        self.SetSizer(vbox)

class NewCustomerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        newCustomerLabel = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        newCustomerLabel.SetFont(font)
        newCustomerLabel.SetLabel("New Customer     ")

        hbox.Add(newCustomerLabel, flag=wx.ALIGN_CENTER_HORIZONTAL)

        nameCustomerLabel = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
        nameCustomerLabel.SetLabel("Name")

        hbox.Add(nameCustomerLabel, flag=wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.nameNewCustomerEditText = wx.TextCtrl(parent=self, id=-1)
        hbox.Add(self.nameNewCustomerEditText, flag=wx.ALIGN_CENTER_HORIZONTAL)

        nextNewCustomerButton = wx.Button(self, label="Next")
        nextNewCustomerButton.Bind(wx.EVT_BUTTON, parent.onNextNewCustomerClick)
        hbox.Add(nextNewCustomerButton, flag=wx.ALIGN_RIGHT)

        vbox.Add(hbox)

        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #
        #
        #
        # vbox.Add(hbox2, border=10)

        #draw boundary
        self.imagePanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(850,1144), pos=(0,28), style=wx.SIMPLE_BORDER)
        self.imagePanel.SetupScrolling()
        self.imagePanel.SetBackgroundColour('#FFFFFF')
        #self.ImageBMP = wx.StaticBitmap(self.imagePanel, wx.ID_ANY, wx.Bitmap("2.png"))
        self.ImageBMP = wx.StaticBitmap(self.imagePanel, wx.ID_ANY, wx.Bitmap("googles.png"))

        # bind event
        self.ImageBMP.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.ImageBMP.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.ImageBMP.Bind(wx.EVT_MOTION, self.OnMove)

        vbox.Add(self.imagePanel, border=10)


        self.SetSizer(vbox)

    #to use for draw boundary
    boundaries = []
    isLeftDown = False

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
            self.ImageBMP = wx.StaticBitmap(self.imagePanel, wx.ID_ANY, wx.Bitmap("googles.png"))

class SetBoundaryPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        setBoundaryNameLabel = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        setBoundaryNameLabel.SetFont(font)
        setBoundaryNameLabel.SetLabel("Set Boundaries Name     ")

        hbox.Add(setBoundaryNameLabel, flag=wx.ALIGN_CENTER_HORIZONTAL)

        saveNewCustomerButton = wx.Button(self, label="Save")
        saveNewCustomerButton.Bind(wx.EVT_BUTTON, parent.onNextNewCustomerClick)
        hbox.Add(saveNewCustomerButton, flag=wx.ALIGN_RIGHT)

        vbox.Add(hbox)

        self.boundariesPanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(850,1144), pos=(0,28), style=wx.SIMPLE_BORDER)
        self.boundariesPanel.SetupScrolling()
        self.boundariesPanel.SetBackgroundColour('#FFFFFF')

        vbox.Add(self.boundariesPanel, border=10)

        self.SetSizer(vbox)

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Documents to text",
                          size=(800, 600))

        #init data
        self.imagesPaths = []


        self.chooseFilePanel = ChooseFilePanel(self)
        self.chooseCustomerPanel = ChooseCustomerPanel(self)
        self.chooseCustomerPanel.Hide()
        self.newCustomerPanel = NewCustomerPanel(self)
        self.newCustomerPanel.Hide()
        self.setBoundaryPanel = SetBoundaryPanel(self)
        self.setBoundaryPanel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.chooseFilePanel, 1, wx.EXPAND)
        self.sizer.Add(self.chooseCustomerPanel, 1, wx.EXPAND)
        self.sizer.Add(self.newCustomerPanel, 1, wx.EXPAND)
        self.sizer.Add(self.setBoundaryPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,
                                                  "Switch Panels",
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels,
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    def onSwitchPanels(self, event):
        if self.chooseFilePanel.IsShown():
            self.SetTitle("Choose Customer")
            self.chooseFilePanel.Hide()
            self.chooseCustomerPanel.Show()
        else:
            self.SetTitle("Choose File")
            self.chooseFilePanel.Show()
            self.chooseCustomerPanel.Hide()
        self.Layout()

    def onAddImagesClick(self, event):
        """change panel after add Image path"""
        self.chooseCustomerPanel.Show()
        self.chooseFilePanel.Hide()
        self.SetTitle("Choose Customer")
        self.Layout()

    def onNewCustomerClick(self, event):
        self.chooseCustomerPanel.Hide()
        self.newCustomerPanel.Show()

        self.newCustomerPanel.ImageBMP = wx.StaticBitmap(self.newCustomerPanel.imagePanel, wx.ID_ANY, wx.Bitmap(self.imagesPaths[0]))
        self.newCustomerPanel.ImageBMP.Bind(wx.EVT_LEFT_DOWN, self.newCustomerPanel.OnLeftDown)
        self.newCustomerPanel.ImageBMP.Bind(wx.EVT_LEFT_UP, self.newCustomerPanel.OnLeftUp)
        self.newCustomerPanel.ImageBMP.Bind(wx.EVT_MOTION, self.newCustomerPanel.OnMove)
        self.SetTitle("New Customer")
        self.Layout()

    def onChooseCustomerClick(self, event):
        pass

    def onNextNewCustomerClick(self, event):
        self.newCustomerPanel.Hide()
        self.setBoundaryPanel.Show()

        #use for test
        print(self.newCustomerPanel.boundaries)
        n=0

        ImageOCR.createGrayScaleImage(self.imagesPaths[0], "C:/Users/Jiravat/Desktop/git/Documents2Database/src/tmp/grayImage.png", preprocess="thresh")
        im = Image.open("C:/Users/Jiravat/Desktop/git/Documents2Database/src/tmp/grayImage.png").convert('RGB')

        boundaries = []
        po = PO(name="simple po")

        for b in self.newCustomerPanel.boundaries:
            area = (b[0], b[1], b[2]+b[0], b[3]+b[1])
            cropped_img = im.crop(area)
            cropped_img.save('C:/Users/Jiravat/Desktop/git/Documents2Database/src/tmp/'+str(n)+".png")
            # im2 = ImageOCR.preprocess(cropped_img)
            # im2.save('../tmp/'+str(n)+".png")
            text = ImageOCR.image_to_string(cropped_img)
            print(text)
            print("-------------------------------------")
            n+=1

            boundaries.append(Boundary("simple boundary title", b))
            po.addData(Data("simple title", text))

        customer = Customer("simple_customer", boundaries=boundaries)
        customer.addPO(po)
        print(customer.toJSON())
        saveJson("C:/Users/Jiravat/Desktop/git/Documents2Database/src/customers/"+customer.name+".json", customer)
        print("done")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
