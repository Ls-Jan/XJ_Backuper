
__version__='1.0.0'
__author__='Ls_Jan'

from XJ.Functions.GetRealPath import GetRealPath
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager

from typing import Union
from PyQt5.QtWidgets import QWidget,QLabel,QLabel,QBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt,QSize,QTimer
from typing import Callable,Any,List

__all__=['XJQ_LoadingAnimation']

class XJQ_LoadingAnimation(QWidget):#加载动画蒙版
	'''
		加载动画，配合XJQ_Mask使用以实现加载动画蒙版效果
	'''
	def __init__(self,
			  iconPath:str=GetRealPath('./LoadingGIF.gif'),
			  textLst:list=list(range(4)),
			  textFunc=lambda arg:'加载中'+'.'*arg,
			  *,
			  dire:QBoxLayout.Direction=QBoxLayout.Direction.TopToBottom):
		'''
			iconPath为动图路径(可传静图)；
			textLst为文本列表；
			textFunc(tx:str)用于实现动态随机文本效果；
		'''
		QWidget.__init__(self)
		icon=QLabel()
		text=QLabel()
		timer=QTimer()
		mv=QMovie()

		timer.setInterval(1000)
		timer.timeout.connect(self.__UpdateText)
		icon.setMovie(mv)
		box=QBoxLayout(dire,self)
		box.setAlignment(Qt.AlignCenter)#居中对齐
		text.setAlignment(Qt.AlignCenter)
		box.addStretch()
		box.addWidget(icon)
		box.addWidget(text)
		box.addStretch()

		self.__mv=mv
		self.__txLst=textLst
		self.__txIndex=0
		self.__txFunc=textFunc
		self.__icon=icon
		self.__text=text
		self.__timer=timer
		self.Set_Direction(dire)
		self.Set_Icon(path=iconPath)
		self.setStyleSheet(GetRealPath('./StyleSheet.qss'))
		self.__UpdateText()
	def setStyleSheet(self,qss:str):
		'''
			对文本进行样式设置(文本颜色、大小等)，
			qss可以为文件路径
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss)
		self.__text.setStyleSheet(sm.styleSheet())
	def __UpdateText(self):
		length=len(self.__txLst)
		if(length>1):
			self.__txIndex+=1
			if(self.__txIndex>=len(self.__txLst)):
				self.__txIndex=0
			self.__text.setText(self.__txFunc(self.__txLst[self.__txIndex]))
		else:
			self.__timer.stop()
	def Set_Text(self,textLst:List[Any]=None,textFunc:Callable[[Any],str]=None):
		'''
			设置动态文本的参数列表以及文本转换函数textFunc(arg)，
			在加载过程中会循环textLst的参数并将其传递给textFunc以实现文本动态效果
		'''
		if(textLst!=None):
			self.__txLst=textLst
		if(textFunc!=None):
			self.__txFunc=textFunc
		self.__UpdateText()
	def Set_Icon(self,size:Union[QSize,tuple]=None,path:str=None):
		'''
			设置图标的文件路径以及图标大小
		'''
		if(path):
			self.__mv.setFileName(path)
			if(self.isVisible()):
				self.__mv.start()
		if(isinstance(size,tuple)):
			size=QSize(*size)
		if(size):
			self.__mv.setScaledSize(size)
	def Set_FrameDuration(self,icon:int=None,text:int=None):
		'''
			设置每帧持续时间(ms)
		'''
		if(icon!=None):
			self.__mv.jumpToNextFrame()#先跳到下一帧以减小nextFrameDelay带来的误差
			speed=self.__mv.nextFrameDelay()/icon#这傻狗只能通过百分比来进行帧时长设置，有点无语
			self.__mv.setSpeed(int(speed*100))
		if(text!=None):
			self.__timer.setInterval(text)
	def Set_Direction(self,dire:QBoxLayout.Direction):
		'''
			设置布局方向
		'''
		self.layout().setDirection(dire)
	def showEvent(self,event):
		self.__mv.start()
		self.__timer.start()
		return super().showEvent(event)
	def hideEvent(self,event):
		self.__mv.stop()
		self.__timer.stop()
		return super().hideEvent(event)
