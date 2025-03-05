__version__='1.1.0'
__author__='Ls_Jan'
__all__=['_Base']

from ..QMatrix import QMatrix
from PyQt5.QtGui import QPainter,QTransform
from PyQt5.QtCore import QRect,QSize
from PyQt5.QtWidgets import QWidget

class _Base:
	'''
		可缩放控件基类
	'''
	def __init__(self):
		self.__matrix:QMatrix=None
	def setLGeometry(self,rect:QRect):
		'''
			设置控件逻辑位置，并改变实际位置。
			亦可通过wid.setProperty('lgeometry',rect)的方式进行设置
		'''
		# 在C++中可以使用指针强转这样的歪门邪道来调用派生类的另一父类的函数
		wid:QWidget=self
		wid.setProperty('lgeometry',rect)
		wid.setGeometry(self.transRect(rect))
	def lgeometry(self):
		'''
			获取控件逻辑位置。
			亦可通过wid.property('lgeometry')的方式进行获取。
			如果没有设置过该属性但又有相应的转换矩阵，则会根据当前位置得到逻辑位置并将其写入。
			如果连转换矩阵都不存在则返回当前位置。
		'''
		wid:QWidget=self
		rect=wid.property('lgeometry')
		if(rect==None):
			rect=wid.geometry()
			if(self.__matrix):
				rect=self.__matrix.Get_TransQRect(rect,invert=True)[0]
				wid.setProperty('lgeometry',rect)
		return rect
	def scaleRate(self):
		'''
			获取缩放比例。
			转换矩阵不存在时返回1。
		'''
		return self.__matrix.Get_ScaleRate() if self.__matrix else 1
	def setMatrix(self,matrix:QMatrix):
		'''
			设置转换矩阵
		'''
		self.__matrix=matrix
	def matrix(self):
		'''
			获取转换矩阵
		'''
		return self.__matrix
	def transRect(self,rect:QRect):
		'''
			获取转换坐标
		'''
		return self.__matrix.Get_TransQRect(rect)[0] if self.__matrix else rect
	def painter(self):
		'''
			获取设置过QTransform的QPainter
		'''
		ptr=QPainter(self)
		if(self.__matrix):
			rate=self.__matrix.Get_ScaleRate()
			trans=QTransform()
			trans.scale(rate,rate)
			ptr.setTransform(trans)
		return ptr
