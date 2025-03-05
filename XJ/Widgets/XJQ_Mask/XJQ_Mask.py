
__version__='1.1.1'
__author__='Ls_Jan'

from ...Functions.QColorToRGBA import QColorToRGBA
from ...Structs.XJ_MouseStatus import XJ_MouseStatus

from PyQt5.QtCore import Qt,pyqtSignal,QPoint,QRect,QEvent
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QStyleOptionFrame
from PyQt5.QtGui import QColor,QPainter,QPixmap,QBitmap,QWheelEvent,QMouseEvent

__all__=['XJQ_Mask']

class XJQ_Mask(QLabel):#加载动画蒙版
	'''
		- 遮蔽控件的不二之选，可以调用mask.hide()将遮罩暂时隐藏；
		- 纯色遮罩，虽然是可以实现渐变色遮罩但实际上这种需求一次都没出现过，于是舍弃渐变色效果；
		- 可调用Set_CenterWidget指定一个XJQ_LoadingAnimation对象以实现遮罩加载动画效果；
		- 调用setParent更改父控件以达到单控件复用效果(虽然没必要)，在遮罩不使用时可通过mask.setParent(None)弃用；
		- 提供clicked(int)信号以满足特殊场合(例如实现“点击空白位置以取消”的操作)，左键(-1)、中键(0)、右键(1)；
		- 提供点击穿透以满足特殊场合；
		- [本功能已移除，理由是不需要]可指定不被遮挡的控件；
	'''
	clicked=pyqtSignal(int)
	def __init__(self,
			  parent:QWidget=None,
			  color:QColor=QColor(0,0,0,224),
			  clickBlock:bool=True,
			  centerWidget:QWidget=None):
		'''
			需指定parent，独立使用不生效；
			color为遮罩颜色，如果需要渐变色则需要通过setStyleSheet手动设置；
			clickBolck决定是否屏蔽点击，不屏蔽的状态下遮罩处于点击穿透状态，屏蔽的话遮罩可点击并且被点击(不包括拖拽时的鼠标释放)时会发送clicked(int)信号；
			centerWidget为中心控件，用来放动画的，可后期通过Set_CenterWidget进行修改；
		'''
		super().__init__(parent)
		self.setAttribute(Qt.WA_TransparentForMouseEvents, not clickBlock)#鼠标事件穿透
		self.show()
		hbox=QHBoxLayout(self)
		hbox.addStretch()
		hbox.addStretch()
		hbox.setAlignment(Qt.AlignCenter)
		self.__centerWidget=None
		self.__mt=XJ_MouseStatus()
		self.__uncoverWidgets=tuple()#不被遮挡的控件
		self.Set_MaskColor(color)
		self.Set_CenterWidget(centerWidget)
	def Set_CenterWidget(self,wid:QWidget):
		'''
			设置处于遮罩中心位置的控件，通常设置XJQ_LoadingAnimation对象
		'''
		hbox=self.layout()
		if(self.__centerWidget):
			hbox.removeWidget(self.__centerWidget)
		if(wid):
			hbox.insertWidget(1,wid)
			wid.show()
		self.__centerWidget=wid
	def Set_MaskColor(self,color:QColor):
		self.setStyleSheet(f'''
			.XJQ_Mask{{
				background-color:{QColorToRGBA(color,True)};
			}}
		''')
	def Set_UncoverWidgets(self,*wids:QWidget):
		'''
			设置不被遮挡的控件
		'''
		self.__uncoverWidgets=wids
		self.update()
	def Get_CenterWidget(self):
		'''
			返回中心控件。
		'''
		return self.__centerWidget
	def mousePressEvent(self,event):
		self.__mt.Opt_Update(event)
		return super().mousePressEvent(event)
	def mouseReleaseEvent(self,event:QMouseEvent):
		self.__mt.Opt_Update(event)
		if(not self.__mt.Get_HasMoved()):
			key={
				Qt.MouseButton.LeftButton:-1,
				Qt.MouseButton.MidButton:0,
				Qt.MouseButton.RightButton:1
			}
			self.clicked.emit(key[event.button()])
	def paintEvent(self,event):
		if(not self.parent()):
			return
		self.resize(self.parent().size())
		if(self.__uncoverWidgets):#提高效率
			bit=QBitmap(self.size())
			bit.fill(Qt.GlobalColor.black)
			ptr=QPainter(bit)
			for wid in self.__uncoverWidgets:
				p1=wid.mapToGlobal(QPoint(0,0))
				p2=self.mapFromGlobal(p1)
				ptr.fillRect(QRect(p2,wid.size()),Qt.GlobalColor.white)
			ptr.end()
			self.setMask(bit)
		else:
			self.clearMask()
		super().paintEvent(event)
