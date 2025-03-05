__version__='1.0.1'
__author__='Ls_Jan'
__all__=['Label']


from ._Base import _Base
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QLabel,QWidget
from PyQt5.QtCore import Qt,QPoint
import typing


class Label(QLabel,_Base):
	@typing.overload
	def __init__(self, parent: typing.Optional[QWidget] = ..., flags: typing.Union[Qt.WindowFlags, Qt.WindowType] = ...) -> None: ...
	@typing.overload
	def __init__(self, text: str, parent: typing.Optional[QWidget] = ..., flags: typing.Union[Qt.WindowFlags, Qt.WindowType] = ...) -> None: ...

	def __init__(self,*args):
		super().__init__(*args)
		self.__aspectRatio=True
	def __pixmap(self):
		pix=self.pixmap()
		if(not pix):
			mv=self.movie()
			if(mv):
				pix=mv.currentPixmap()
		if(pix and not pix.isNull()):
			if(self.hasScaledContents()):
				sz=self.contentsRect().size()
				pix=pix.scaled(pix.size().scaled(sz,Qt.AspectRatioMode.KeepAspectRatio) if self.__aspectRatio else sz)
		return pix
	def paintEvent(self,event:QPaintEvent):
		#见源码：https://codebrowser.dev/qt6/qtbase/src/widgets/widgets/qlabel.cpp.html#_ZN6QLabel10paintEventEP11QPaintEvent
		ptr=self.painter()
		style=self.style()
		rect=self.lgeometry()
		rect.moveTopLeft(QPoint(0,0))
		pix=self.__pixmap()
		ptr.setRenderHint(ptr.RenderHint.SmoothPixmapTransform)#能让绘制的线条(简单绘图)不那么难看
		if(pix):
			style.drawItemPixmap(ptr,rect,Qt.AlignmentFlag.AlignCenter,pix)
		else:
			style.drawItemText(ptr,rect,Qt.AlignmentFlag.AlignCenter,self.palette(),True,self.text())
	def setAspectRatio(self,flag:bool):
		'''
			设置缩放图片(setScaledContents)时是否固定宽高比
		'''
		self.__aspectRatio=flag
