import wx
import wx.adv



class CustomFrame(wx.Frame):

    def __init__(self, *arg, **kw):
        super(CustomFrame, self).__init__(*arg, **kw)

        self.devConnected = False
        self.fileSelected = "" 
        self.myTimer      = wx.Timer(self)
        self.noTicks      = 0

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.fileSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.spaceAnim = wx.adv.AnimationCtrl(self, size=wx.Size(200, 200), style=wx.adv.AC_NO_AUTORESIZE)
        self.devLabel  = wx.StaticText(self, label="Looking for device")
        self.btnOpen   = wx.Button(self, -1, "Select Payload")
        self.fileLabel = wx.StaticText(self, label="No payload selected.")
        self.btnLaunch = wx.Button(self, -1, "Launch Fusée!")

        self.spaceAnim.LoadFile("space_anim.gif")

        self.fileSizer.Add(self.btnOpen, 0, wx.ALL|wx.ALIGN_LEFT, 8)
        self.fileSizer.Add(self.fileLabel, 0, wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 8)

        self.mainSizer.Add(self.spaceAnim, 0, wx.ALL|wx.ALIGN_CENTER, 8)
        self.mainSizer.Add(self.devLabel, 0, wx.ALL|wx.ALIGN_CENTER, 8)
        self.mainSizer.Add(self.fileSizer, 0, wx.ALL, 0)
        self.mainSizer.Add(self.btnLaunch, 0, wx.ALL|wx.EXPAND, 8)

        self.SetSizerAndFit(self.mainSizer)

        self.validateLaunch()

        self.Layout()

        self.spaceAnim.Play()

        self.Bind(wx.EVT_TIMER, self.onTimerUpdate)
        self.myTimer.Start(300)
    


    def validateLaunch(self):
        if self.fileSelected != "" and self.devConnected:
            self.btnLaunch.Enable()
        else:
            self.btnLaunch.Disable()

    

    def onTimerUpdate(self, evt):
        self.devLabel.SetLabel("Looking for device"+("." * self.noTicks))

        self.noTicks += 1
        if self.noTicks > 3: self.noTicks = 0
