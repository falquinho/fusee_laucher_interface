import wx
import wx.adv
import fusee_launcher as Fusee
import MockArguments



class CustomFrame(wx.Frame):
    
    def __init__(self, *arg, **kw):
        super(CustomFrame, self).__init__(*arg, **kw)

        self.devVid       = 0x0955
        self.devPid       = 0x7321

        self.devConnected = False
        self.payloadPath  = "" 
        self.myTimer      = wx.Timer(self)
        self.noTicks      = 0
        self.labelSize    = 18
        self.haxBackend   = Fusee.HaxBackend.create_appropriate_backend()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.fileSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.animPanel = wx.Panel(self, size=wx.Size(200, 200))
        self.spaceAnim = wx.adv.AnimationCtrl(self.animPanel, size=wx.Size(200, 200), style=wx.adv.AC_NO_AUTORESIZE)
        self.rocktAnim = wx.adv.AnimationCtrl(self.animPanel, size=wx.Size(200, 200), style=wx.adv.AC_NO_AUTORESIZE)
        self.devLabel  = wx.StaticText(self, label="Looking for device")
        self.btnOpen   = wx.Button(self, -1, "Select Payload")
        self.fileLabel = wx.StaticText(self, label="No payload selected.")
        self.btnLaunch = wx.Button(self, -1, "Launch Fusée!")

        self.spaceAnim.LoadFile("space_anim.gif")
        self.rocktAnim.LoadFile("rocket_anim.gif")
        self.spaceAnim.Play()
        self.rocktAnim.Play()
        self.rocktAnim.Hide()

        self.fileSizer.Add(self.btnOpen, 0, wx.ALL|wx.ALIGN_LEFT, 8)
        self.fileSizer.Add(self.fileLabel, 0, wx.RIGHT|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 8)

        self.mainSizer.Add(self.animPanel, 0, wx.ALL|wx.ALIGN_CENTER, 8)
        self.mainSizer.Add(self.devLabel, 0, wx.ALL|wx.ALIGN_CENTER, 8)
        self.mainSizer.Add(self.fileSizer, 0, wx.ALL, 0)
        self.mainSizer.Add(self.btnLaunch, 0, wx.ALL|wx.EXPAND, 8)

        self.SetSizerAndFit(self.mainSizer)

        self.validateLaunch()

        self.Layout()


        self.Bind(wx.EVT_BUTTON, self.onBtnOpenPressed, self.btnOpen)
        self.Bind(wx.EVT_BUTTON, self.onBtnLaunchPressed, self.btnLaunch)

        self.Bind(wx.EVT_TIMER, self.onTimerUpdate)
        self.myTimer.Start(300)
    


    def validateLaunch(self):
        if self.payloadPath != "" and self.devConnected:
            self.btnLaunch.Enable()
        else:
            self.btnLaunch.Disable()

    

    def onTimerUpdate(self, evt):
        dev = self.haxBackend.find_device(self.devVid, self.devPid)
        if dev != None:
            self.devConnected = True
            self.rocktAnim.Show()
            self.devLabel.SetLabel("Device found!")
        else:
            self.devConnected = False
            self.rocktAnim.Hide()
            self.devLabel.SetLabel("Looking for device"+("."*self.noTicks))
            self.noTicks = (self.noTicks+1)%4

        self.validateLaunch()



    def onBtnOpenPressed(self, evt):
        with wx.FileDialog(
            self, "Select payload.", wildcard="Binary (*.bin)|*.bin", style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST
        ) as fDialog:
            if fDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            self.payloadPath = fDialog.GetPath()

            slicePos = len(self.payloadPath)-self.labelSize
            self.fileLabel.SetLabel(".."+self.payloadPath[max(0, slicePos):])

            self.validateLaunch()
    


    def onBtnLaunchPressed():
        args = MockArguments.MockArguments()
        args.payload = self.payloadPath
        Fusee.do_hax(args)
        pass
        