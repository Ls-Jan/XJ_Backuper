__version__='1.0.1'
__author__='Ls_Jan'
__all__=['PushButton']


from ._Base import _Base
from PyQt5.QtGui import QPaintEvent,QIcon
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QPushButton,QStyleOptionButton,QStyle,QWidget
import typing

class PushButton(QPushButton,_Base):
	@typing.overload
	def __init__(self, parent: typing.Optional[QWidget] = ...) -> None: ...
	@typing.overload
	def __init__(self, text: str, parent: typing.Optional[QWidget] = ...) -> None: ...
	@typing.overload
	def __init__(self, icon: QIcon, text: str, parent: typing.Optional[QWidget] = ...) -> None: ...

	def __init__(self,*args):
		super().__init__(*args)
	def paintEvent(self,event:QPaintEvent):
		ptr=self.painter()
		style=self.style()
		rect=self.lgeometry()
		rect.moveTopLeft(QPoint(0,0))
		opt=QStyleOptionButton()
		self.initStyleOption(opt)
		opt.rect=rect
		style.drawControl(QStyle.ControlElement.CE_PushButton,opt,ptr,self)



	

