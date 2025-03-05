
__version__='1.1.1'
__author__='Ls_Jan'
__all__=['Canvas']

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,QRect,QPoint,QChildEvent,QEvent,QMargins
from PyQt5.QtGui import QWheelEvent,QResizeEvent,QMouseEvent
from typing import Union,Set
from ..Widgets._Base import _Base
from ._Option import _Option
from ....Structs.XJ_MouseStatus import XJ_MouseStatus
from ..QMatrix import QMatrix

class Canvas(QWidget):
	'''
		画布类，使用非常简单，控件直接setParent即可加入其中，
		控件的geometry作为逻辑位置，加入画布后仅可通过画布的Set_WidgetPos更新控件的逻辑位置。
		滚轮缩放，右键拖拽(均可禁用)，设置缩放中心(可撤走)，设置缩放值。

		虽然可以向画布中添加任意控件，
		但建议使用XJQ_Resizable.Widgets下的控件以便达到更好的缩放效果(例如字体跟随缩放)，
		控件的逻辑位置变化需通过wid.setProperty('lgeometry',rect:QRect)设置(或是调用Canvas.Set_WidPos)。
		调用wid.setGeometry是无意义的。
	'''
	__option:_Option#特殊功能
	__mouseStatus:XJ_MouseStatus#XJ_MouseStatus
	__matrix:QMatrix#转换矩阵，逻辑坐标→显示坐标
	__fixed:Set[int]#狗皮膏药一动不动的控件，用于特殊场合。仅记录id(wid)而不是wid
	def __init__(self):
		super().__init__()
		self.__option=_Option()
		self.__matrix=QMatrix()
		self.__mouseStatus=XJ_MouseStatus()
		self.__fixed=set()
	def Set_Option(self,scale:bool=None,drag:bool=None):
		'''
			可以启用/禁用滚轮缩放、鼠标拖拽
		'''
		if(scale==None):
			scale=self.__option.scalable
		if(drag==None):
			drag=self.__option.draggable
		self.__option.scalable=scale
		self.__option.draggable=drag
	def Set_ScaleLimit(self,*,min:int=None,max:int=None):
		'''
			设置缩放极限值
		'''
		self.__matrix.Set_ScaleLimit(min,max)
	def Set_ScaleCenter(self,obj_or_pos:Union[QWidget,QPoint]):
		'''
			设置缩放中心。
			传入None则缩放时以鼠标位置为准
		'''
		self.__option.scaleCenter=obj_or_pos
	def Set_ScaleRate(self,rate,pos:QPoint=None,*,increase:bool=False):
		'''
			设置缩放比，pos为缩放中心(QPoint对象)。
			如果increase为真那么以“增量”的形式调整缩放比(一般用不上)。
			pos指定为None则默认使用画布中心
		'''
		if(pos==None):
			center=self.__option.scaleCenter
			if(isinstance(center,QPoint)):
				pos=center
			elif(center in self.children()):
				pos=center.geometry().center()
			else:
				sz=self.geometry().size()/2
				pos=QPoint(sz.width(),sz.height())
		self.__matrix.Opt_Scale(pos.x(),pos.y(),rate,not increase)
		self.Opt_Update()
	def Get_ScaleRate(self):
		'''
			获取当前缩放比
		'''
		return self.__matrix.Get_ScaleRate()
	def Opt_MoveCenterTo(self,obj_or_pos:Union[QWidget,QPoint]):
		'''
			移动画布中心到指定坐标，传入的可以是QPoint(逻辑坐标)也可以是控件对象
		'''
		pos=None
		if(isinstance(obj_or_pos,QPoint)):
			pos=self.__matrix.Get_TransQPoint(obj_or_pos)[0]
		elif(obj_or_pos in self.children()):
			pos=obj_or_pos.geometry().center()
		if(pos):
			size=self.size()
			center=QPoint(size.width()>>1,size.height()>>1)
			offset=center-pos
			self.Opt_MoveCanvas(offset)
	def Set_ViewArea(self,area:QRect=None):
		'''
			设置需要显示的逻辑范围。
			如果area为None则缩放显示所有控件
		'''
		if(area==None):
			area=QRect()
			for child in self.children():
				area=area.united(self.Get_WidPos(child))
		area=area.marginsAdded(QMargins(10,10,10,10))#小加一点空白
		self.Set_ScaleRate(min(self.width()/area.width(),self.height()/area.height()))
		self.Opt_MoveCenterTo(area.center())
		return True
	def Opt_MoveCanvas(self,offset:QPoint):
		'''
			增量移动画布，移动效果与鼠标拖拽一致
		'''
		self.__matrix.Opt_Move(offset.x(),offset.y())
		self.Opt_Update()
	def Set_WidPos(self,wid:QWidget,rect:QRect):
		'''
			设置控件逻辑位置。
			本质上就是调用wid.setProperty('lgeometry',rect)
		'''
		wid.setProperty('lgeometry',rect)
		self.Opt_Update()
	def Set_WidFixed(self,wid:QWidget,flag:bool=True):
		'''
			设置控件是否位置固定。
			固定的控件不受画布拖拽缩放影响，不受“逻辑位置”变化，始终在画布固定位置(也可以将其称之为“非画布元素”)，
			目标控件可调用wid.setGeometry直接设置实际位置。
			如果wid=None并且flag=False那么将取消所有固定的控件。
		'''
		if(flag):
			if(wid):
				self.__fixed.add(id(wid))
		else:
			if(wid):
				self.__fixed.remove(id(wid))
			else:
				self.__fixed.clear()
	def Get_WidPos(self,wid:QWidget):
		'''
			获取控件逻辑位置。
			本质上就是调用wid.property('lgeometry')
		'''
		return wid.property('lgeometry')
	def Opt_Update(self):
		'''
			更新画布，在内部控件位置发生变化时需手动主动调用
		'''
		for wid in self.children():
			if(isinstance(wid,QWidget)):
				rect=wid.property('lgeometry')
				if(rect and id(wid) not in self.__fixed):
					wid.setGeometry(self.__matrix.Get_TransQRect(rect)[0])
		self.update()
	def wheelEvent(self,event:QWheelEvent):
		if(self.__option.scalable):
			pos=None if self.__option.scaleCenter else event.pos()#如果锁定拖拽那么以中心进行缩放
			rate=1+event.angleDelta().y()/1000
			self.Set_ScaleRate(rate,pos,increase=True)
	def mousePressEvent(self,event:QMouseEvent):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
	def mouseMoveEvent(self,event:QMouseEvent):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			if(ms.Get_PressButtonStatus()[0]==Qt.RightButton):#右键拖拽
				offset=ms.Get_MoveDelta(False)
				self.Opt_MoveCanvas(offset)
	def mouseReleaseEvent(self,event:QMouseEvent):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
	def resizeEvent(self,event:QResizeEvent):
		'''
			在画布调整大小时始终保持中心位置不变
		'''
		szo=event.oldSize()
		szn=event.size()
		if(szo.isValid() and szo.isValid()):
			dx=szn.width()-szo.width()
			dy=szn.height()-szo.height()
			self.Opt_MoveCanvas(QPoint(dx/2,dy/2))
	def event(self,e:QEvent):
		if(isinstance(e,QChildEvent)):
			wid=e.child()
			super().event(e)
			if(isinstance(wid,QWidget)):
				rect=wid.geometry()
				if(e.removed()):
					wid.setGeometry(self.__matrix.Get_TransQRect(rect,invert=True)[0])#将位置复原
					if(isinstance(wid,_Base)):
						wid.setMatrix(None)
				else:
					self.Opt_Update()
					self.Set_WidPos(wid,rect)
					if(isinstance(wid,_Base)):
						wid.setMatrix(self.__matrix)
		return super().event(e)



