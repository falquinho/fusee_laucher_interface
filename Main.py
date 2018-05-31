import wx
from CustomFrame import CustomFrame


app = wx.App()

myFrame = CustomFrame(None, title="Fusée Gelée Interfacée")
myFrame.Show()

app.MainLoop()
