
__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJQ_VisibleTree']


from ..XJQ_Resizable.Canvas import Canvas
from ..XJQ_Resizable.Widgets.PushButton import PushButton
from ..XJQ_Resizable.Widgets.Label import Label
from .XJ_TreeDrawer_Base import XJ_TreeDrawer_Base

from PyQt5.QtCore import QRect,QPoint,QSignalMapper
from PyQt5.QtGui import QPixmap,QPainter,QColor

from typing import List,Tuple


class XJQ_VisibleTree(XJ_TreeDrawer_Base):
	'''
		可视树绘制器。需注意，其本身并不是控件，要调用Get_Canvas获取实际控件。
		绘制结果基于XJ.Widgets.XJQ_Resizable下的Canvas(画布)、PushButton(按钮)、Label(标签)。
		所有按钮均已绑定点击事件，连接Get_ClickedSignal返回的信号(clicked(int))即可
	'''
	def __init__(self):
		super().__init__()
		self.__smp=QSignalMapper()
		self.__canvas=Canvas()
		self.__lines=Label(self.__canvas)
		self.__nodes:List[PushButton]=[]
		self.__ptr=QPainter()
		self.__pix=QPixmap(1,1)
		self.__lineWidth=1
		self.__canvas.show()
		self.__canvas.resize(1200,700)
		self.__lines.setLGeometry(QRect(0,0,100,100))
		self.__treeSize=(0,0)
		self._DrawNode(0,0,0,0,0)#添加一个根节点，算是偷懒的做法(因为要绑信号槽)
		self.Set_LineWidth()
	def Set_LineWidth(self,width:int=3):
		'''
			设置线条粗细(默认3)
		'''
		self.__lineWidth=width
		self.Opt_Update()
	def Get_Canvas(self):
		'''
			返回画布控件
		'''
		return self.__canvas
	def Get_Node(self,nodeID:int):
		'''
			返回节点控件
		'''
		return self.__nodes[nodeID]
	def Get_ClickedSignal(self):
		'''
			返回按钮点击信号clicked(int)，其中int为对应的索引
		'''
		return self.__smp.mappedInt
	def Opt_Focus(self):
		'''
			将树的中心移动至控件中心
		'''
		self.__canvas.Opt_MoveCenterTo(QPoint(*self.__treeSize)/2)
	def _DrawStart(self,x:int,y:int,w:int,h:int):
		count=len(self.Get_Tree())
		for i in range(count,len(self.__nodes)):
			self.__nodes[i].close()
		del self.__nodes[count:]
		pix=QPixmap(w,h)
		pix.fill(QColor(0,0,0,0))#将alpha改为50可以清晰看到线条绘制区域
		ptr=self.__ptr
		ptr.begin(pix)
		pen=ptr.pen()
		pen.setWidth(self.__lineWidth)
		ptr.setPen(pen)
		ptr.translate(-x,-y)
		self.__pix=pix
		self.__lines.setLGeometry(QRect(x,y,w,h))
		self.__treeSize=(w,h)
	def _DrawEnd(self):
		self.__ptr.end()
		self.__lines.setPixmap(self.__pix)
		self.__canvas.Opt_Update()
	def _DrawLine(self,x1:int,y1:int,x2:int,y2:int,rgba:Tuple[int,int,int,int]):
		ptr=self.__ptr
		pen=ptr.pen()
		pen.setColor(QColor(*rgba))
		ptr.setPen(pen)
		ptr.drawLine(x1,y1,x2,y2)
	def _DrawNode(self,x:int,y:int,w:int,h:int,nodeID:int):
		nodes=self.__nodes
		smp=self.__smp
		for i in range(len(nodes),nodeID+1):
			node=PushButton(self.__canvas)
			node.clicked.connect(smp.map)
			smp.setMapping(node,i)
			nodes.append(node)
			node.show()
		node:PushButton=nodes[nodeID]
		node.setLGeometry(QRect(x,y,w,h))
	def _Clear(self):
		for node in self.__nodes[1:]:
			node.setParent(None)
			node.close()
		del self.__nodes[1:]

