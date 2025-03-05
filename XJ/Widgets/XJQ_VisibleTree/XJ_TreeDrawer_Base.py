
__version__='1.1.1'
__author__='Ls_Jan'
__all__=['XJ_TreeDrawer_Base']

from .XJ_CoordinateTree import XJ_CoordinateTree
from typing import Tuple,List,Dict

class XJ_TreeDrawer_Base:
	'''
		基于XJ_CoordinateTree的可视树绘制器基类。
		派生类需重写：
			- _DrawLine；
			- _DrawNode；
			- _DrawStart；
			- _DrawEnd；
			_ _Clear；
	'''
	def __init__(self,tree:XJ_CoordinateTree=None):
		self.__colLine:Dict[Tuple[int,int],Tuple[int,int,int,int]]={(0,0):(0,0,0,255)}#特殊照顾(以其他颜色绘制线条)
		self.__tree:XJ_CoordinateTree=tree if tree else XJ_CoordinateTree()
	def Set_LineColor(self,col:Tuple[int,int,int],*links:Tuple[int,int],clear:bool=False):
		'''
			为指定的节点连线设置颜色。
			如果links为空则视为修改默认颜色(初始颜色为纯黑(0,0,0))。
			clear为真则清除之前的颜色设置。
			同时设置多种不同颜色的线时需要尽量避免出现重合的情况
		'''
		col=(*col,255)
		if(clear):
			self.__colLine.clear()
			self.__colLine[(0,0)]=(0,0,0,255)
		if(links):
			for link in links:
				if(link[0]>link[1]):
					link=(link[1],link[0])
				self.__colLine[link]=col
		else:
			self.__colLine[(0,0)]=col
		self.Opt_Update()
	def Get_Tree(self)->XJ_CoordinateTree:
		'''
			获取坐标树
		'''
		return self.__tree
	def Opt_Clear(self):
		'''
			清除记录，同时更新画布
		'''
		self.__tree.Opt_TreeClear()
		self._Clear()
		self.Opt_Update()
	def Opt_Update(self):
		'''
			更新画布
		'''
		class Node:
			posLTWH:Tuple[float,float,float,float]#节点位置(左上宽高)
			nexts:List[int]#子节点索引
		nodes:List[Node]=[]
		self.__tree.Opt_Update()
		geometryLst=self.__tree.Get_NodesGeometry()
		for index in range(len(self.__tree)):
			node=Node()
			node.posLTWH=geometryLst[index]
			node.nexts=self.__tree[index][1:]
			nodes.append(node)
		L,T,W,H=self.__tree.Get_Geometry()
		self._DrawStart(int(L),int(T),int(W),int(H))
		for index in range(len(nodes)):
			node=nodes[index]
			x,y,w,h=node.posLTWH
			nexts=node.nexts
			self._DrawNode(x,y,w,h,index)
			if(nexts):
				node=nodes[nexts[-1]]
				y0=y+h-1
				y2=node.posLTWH[1]
				y1=(y0+y2)>>1
				x0=x+(w>>1)
				xs=[]
				colx:List[Tuple[float,tuple]]=[]
				for nIndex in nexts:
					col=self.__colLine.get((index,nIndex),None)
					node=nodes[nIndex]
					x,y,w,h=node.posLTWH
					xs.append(x+(w>>1))
					if(col):
						colx.append((xs[-1],col))
				col=self.__colLine[(0,0)]
				self._DrawLine(x0,y0,x0,y1,col)
				if(xs):
					self._DrawLine(xs[0],y1,xs[-1],y1,col)
					for x in xs:
						self._DrawLine(x,y1,x,y2,col)
				if(colx):#存在彩线
					for xc in reversed(colx):
						x,col=xc
						self._DrawLine(x0,y0,x0,y1,col)
						self._DrawLine(x0,y1,x,y1,col)
						self._DrawLine(x,y1,x,y2,col)
		self._DrawEnd()
	def _DrawStart(self,x:int,y:int,w:int,h:int):
		'''
			绘制开始，传入绘制区域
		'''
		pass
	def _DrawEnd(self):
		'''
			绘制结束
		'''
		pass
	def _DrawLine(self,x1:int,y1:int,x2:int,y2:int,rgba:Tuple[int,int,int,int]):
		'''
			绘制线条
		'''
		pass
	def _DrawNode(self,x:int,y:int,w:int,h:int,nodeID:int):
		'''
			绘制节点
		'''
		pass
	def _Clear(self):
		'''
			清除记录
		'''
		pass
