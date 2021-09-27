import wx
import os
import numpy as np
import socket

base_size = (1280,720)
wind_size = base_size
btnSize = (wind_size[0]//9,wind_size[1]//15)
imgWindSize = (wind_size[0]//6*4,wind_size[1]//10*8)
logoSize = (wind_size[0]//8,wind_size[1]//8)
btnEdge = wind_size[0]//5*4
imgPos = (wind_size[0]//25, wind_size[1]//14)

class picLog(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, title='ObjDetector0xA3', size=wind_size,style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

		#背景设定
		self.color = (59, 61, 71)
		self.SetBackgroundColour(self.color)
		self.panel = wx.Panel(self, pos=imgPos, size=imgWindSize)
		# self.panel.SetBackgroundColour('white')
		self.image2= wx.Image( "images/white.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.white = wx.StaticBitmap(self.panel, -1, self.image2, pos=(0,0), size=imgWindSize)
		

		# FILE 按钮
		bmp=wx.Image("images/FILE.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		self.SelBtn = wx.BitmapButton(self,-1,bmp, pos=(btnEdge, wind_size[1]//9 + wind_size[1]//5*0),style=wx.NO_BORDER)
		self.SelBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)

		# START 按钮
		bmp=wx.Image("images/START.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		self.SelBtn = wx.BitmapButton(self,-1,bmp,pos=(btnEdge, wind_size[1]//9 + wind_size[1]//5*1),style=wx.NO_BORDER)
		self.SelBtn.Bind(wx.EVT_BUTTON, self.start)

		# CLEAR 按钮
		bmp = wx.Image("images/CLEAR.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		self.SelBtn = wx.BitmapButton(self,-1,bmp,pos=(btnEdge, wind_size[1]//9 + wind_size[1]//5*2), style=wx.NO_BORDER)
		self.SelBtn.Bind(wx.EVT_BUTTON, self.clear)

		# VS 按钮
		bmp = wx.Image("images/VS.png",
					   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		self.SelBtn = wx.BitmapButton(self,-1,bmp,pos=(btnEdge, wind_size[1]//9 + wind_size[1]//5*3), style=wx.NO_BORDER)
		self.SelBtn.Bind(wx.EVT_BUTTON, self.CameraOn)
		
		# bmp = wx.Image("images/sou.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		# self.SelBtn = wx.BitmapButton(self, -1, bmp, pos=(btnEdge - wind_size[0]//10, wind_size[1] - wind_size[1]//4), style=wx.NO_BORDER)

		self.image =None
		self.show = None


	# 读取文件目录
	def onOpenFile(self, event):
		wildcard = 'All files(*.*)|*.*'
		dialog = wx.FileDialog(None, '选择', os.getcwd(), '', wildcard, wx.FD_OPEN)
		res = []
		
		# 判断文件名合法性
		self.FileName = wx.TextCtrl(self, pos=(5, 5), size=(0, 0))
		if dialog.ShowModal() == wx.ID_OK:
			self.FileName.SetValue(dialog.GetPath())
			self.FileName = self.FileName.GetValue()
			dialog.Destroy()
		else:
			return

		# 显示图片
		self.panel.DestroyChildren()
		self.image1 = wx.Image(self.FileName, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		resSize = self.image1.GetSize()
		self.show = wx.StaticBitmap(self.panel, -1, self.image1, pos=(0,0), size=(resSize[0]*imgWindSize[1]//resSize[1],imgWindSize[1]))
		self.panel.Fit()

	# 开始检测
	def start(self, event):

		# 调取接口进行目标检测
		res = socket.detectImg(self.FileName)
		resimg = res.copy()
		resimg[:,:,[0,1,2]] = resimg[:,:,[2,1,0]]
		resSize = resimg.shape
		resimg = wx.Image(resSize[1],resSize[0],resimg).ConvertToBitmap()
		self.panel.DestroyChildren()

		# 显示识别后的图片
		self.show = wx.StaticBitmap(self.panel, -1, resimg, pos=(0,0), size=(resSize[1]*imgWindSize[1]//resSize[0],imgWindSize[1]))
		self.panel.Fit()

	# 清除结果
	def clear(self, event):

		self.panel.DestroyChildren()
		self.image2= wx.Image( "images/white.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.white = wx.StaticBitmap(self.panel, -1, self.image2, pos=(0,0), size=imgWindSize)
		self.panel.Fit()

	# 打开摄像头
	def CameraOn(self, event):
		socket.detectVideo()

app = wx.App()
SiteFrame = picLog()
SiteFrame.Show()
app.MainLoop()