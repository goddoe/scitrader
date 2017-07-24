import win32com.client as wclient
import win32ui, win32uiole
import win32con
import pywintypes
import os, sys, win32api, glob
from pywin.mfc import activex, window, dialog
"""
kiwoom = wclient.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")
print(kiwoom.__dict__)
print("="*30)
print(dir(kiwoom))

print("="*30)
print(vars(kiwoom))

print("="*30kkk)

kiwoom.CommConnect()
"""

class OCXFrame(window.MDIChildWnd):
    def __init__(self):
        pass # Dont call base class doc/view version...
    def Create(self, controlClass, title, rect = None, parent = None):
        style = win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW

        self._obj_ = win32ui.CreateMDIChild()
        self._obj_.AttachObject(self)
        self._obj_.CreateWindow(None, title, style, rect, parent)
         
        rect = self.GetClientRect()
        rect = (0,0,rect[2]-rect[0], rect[3]-rect[1])
        rect = (0,0,100, 100)
        self.ocx = controlClass()
        self.ocx.CreateControl("",win32con.WS_VISIBLE | win32con.WS_CHILD, rect, self, 1000)     
        self.ocx.CommConnect()
        print("connect")

kiwoom_module = wclient.gencache.GetClassForProgID("KHOPENAPI.KHOpenAPICtrl.1")

class Kiwoom(activex.Control, kiwoom_module ):
    pass

f = OCXFrame()
f.Create(Kiwoom, "kiwoom text")

