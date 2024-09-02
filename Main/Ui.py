import wx
app = wx.App() 
def view_text(text):
    window = wx.Frame(None, title = "Text", size = (300,200)) 
    panel = wx.Panel(window) 
    label = wx.StaticText(panel, label = text, pos = (0,0))
    window.Show(True) 
    app.MainLoop()