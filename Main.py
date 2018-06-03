import wx
from CustomFrame import CustomFrame


app = wx.App()

myFrame = CustomFrame(None, title="Fusée Gelée Interfacée", style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER)
myFrame.Show()

app.MainLoop()
