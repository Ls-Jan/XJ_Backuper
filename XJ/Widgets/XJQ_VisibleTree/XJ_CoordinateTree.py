
__version__='1.1.1'
__author__='Ls_Jan'
__all__=['XJ_CoordinateTree']

from typing import List
from .TreeNode import TreeNode

from ...Structs.XJ_ArrayTree import XJ_ArrayTree
from typing import List,Tuple,Type

#TODO:完成strecth以实现高级对齐
#TODO:没处理成环的情况
class XJ_CoordinateTree(XJ_ArrayTree):
	'''
		简单的坐标化树，会返回节点的位置信息，隐去根节点则成为森林。
		根节点的id为0，可设置根节点坐标。
		不支持节点删除，但可以设置节点是否可见。
		对树进行修改/设置后，需要重新调用Opt_Update进行更新，以获取准确的节点位置信息。

		该类继承XJ_ArrayTree，接受的节点类型为TreeNode及其派生类。
	'''
	__nodeSize=(50,50)#节点默认大小
	__interval=(25,50)#行列之间的间隔
	__alignment:int=0#左对齐(0)、居中(1)、右对齐(-1)
	__reversed:bool=False#是否反向排列
	__rootPos:Tuple[int,int]=(0,0)#根节点坐标
	__geometry:Tuple[int,int,int,int]=[0,0,0,0]#左上宽高
	__intervalStretch:Tuple[int,int]=(2**30,2**30)#行列对齐的允许增长量
	def __init__(self,nodeClass:Type[TreeNode]=TreeNode):
		super().__init__(nodeClass)
	def Set_NodeSize(self,nodeID:int,W:float=None,H:float=None):
		'''
			设置节点大小，节点高度不能过大，传入0值则使用默认大小。
			当nodeID为负值时视为设置默认大小。
		'''
		if(nodeID<0):
			self.__nodeSize=(W,H)
		else:
			node:TreeNode=self[nodeID]
			if(W!=None):
				node._w=W
			if(H!=None):
				node._h=H
		return True
	def Set_NodeVisible(self,nodeID:int,flag:int):
		'''
			设置目标节点及其子节点是否可见。
			完全可见(正数)、仅隐去子节点(0)、本节点及子节点不可见(负数)。
			操作对根节点无效。
		'''
		flag=-1 if flag<0 else 0 if flag==0 else 1
		node:TreeNode=self[nodeID]
		node._node_isVisible=flag
		return True
	def Set_Alignment(self,flag:int):
		'''
			设置对齐，左对齐(负数)、居中(0)、右对齐(正数)。
			根节点始终是居中的
		'''
		flag=0 if flag<0 else 1 if flag==0 else -1
		self.__alignment=flag
		return True
	def Set_Interval(self,row:int,col:int,StrecthRow:int,StretchCol:int):
		'''
			设置行列的间隔。
			strecth用于宏观对齐，当它为负数或无穷大数时表现为所有的节点的间距都是一致的，就仿若在一个表格中
		'''
		self.__interval=(row,col)
		if(StrecthRow<0):
			StrecthRow=2**30
		if(StrecthCol<0):
			StrecthCol=2**30
		self.__intervalStretch=(StrecthRow,StretchCol)
		return True
	def Set_RootNodePos(self,x:float,y:float):
		'''
			设置根节点坐标(默认0,0)
		'''
		self.__geometry[0]=x
		self.__geometry[1]=y
	def Get_NodesGeometry(self):
		'''
			获取所有节点的位置信息，返回的是一个形如[(x,y,w,h)]的列表。
		'''
		rst:List[Tuple[int,int,int,int]]=[]
		node:TreeNode=None
		for node in self:
			rst.append((node._x,node._y,self.__NodeWidth(node),self.__NodeHeight(node)))
		return rst
	def Get_Geometry(self):
		'''
			获取树的显示范围，返回左上宽高。
			调用Opt_Update更新过后才会返回正确结果
		'''
		return self.__geometry
	def Opt_Update(self):
		class Data:#一些过程变量，如果用list存的话就过于繁琐，特此结构化
			node:TreeNode#当前节点
			align:TreeNode#对齐的节点
			children:List[TreeNode]#未隐藏的子节点
			def __init__(self,node:TreeNode):
				self.node=node
				self.children=[]
				self.align=None
		super().Opt_Update()
		width=[-2**30]#深度对应宽度
		# rowInterval=[]#每行的间隔，若是当前行小于指定高度则会强制调整为该值
		stk=[[Data(self[0]),],]#长度即是当前深度。遍历方式是深度遍历
		coincidents=self.Get_CoincidentNodes()#成环的问题点，若不排除则会导致无限循环
		while(stk):#位置的确定是自底而上的，而非自顶而下。坐标是相对位置而非绝对位置
			group=stk[-1]
			if(group):#存在节点，继续向下探寻
				data=group[-1]
				if(data.node._node_isVisible==1):
					for id in data.node[1:]:
						if(id in coincidents):
							continue
						child:TreeNode=self[id]
						if(child._node_isVisible!=-1):
							child._y=self.__nodeSize[1]+self.__interval[1]#节点高度锁定为默认值而非data.node.h
							data.children.append(child)
				newGroup=[Data(node) for node in data.children]
				if(self.__alignment!=1 and newGroup):
					data.align=data.children[self.__alignment]
				if(not self.__reversed):
					newGroup.reverse()
				stk.append(newGroup)
			else:#子节点列表为空，反哺父节点(数据向上传递)，同时将父节点移除
				depth=len(stk)-1
				while(depth>=len(width)):
					width.append(width[-1])
				stk.pop()
				depth-=1
				if(not stk):
					break
				group=stk[-1]
				data=group[-1]
				node=data.node
				align=data.align
				children=data.children
				x=0
				nw=self.__NodeWidth(node)
				if(align!=None):#存在对齐
					x=align._x+self.__NodeWidth(align)/2
					node._cw=max(align._cw,nw)#最大列宽向上传递
				else:#无对齐，居中
					node._cw=nw
					if(children):
						x=(children[0]._x+children[-1]._x)/2+(self.__NodeWidth(children[0])+self.__NodeWidth(children[-1]))/4
				tx=x-nw/2#父节点理论位置(绝对位置)
				p=width[depth]#安全位置
				x=max(tx,p)#保证位置有效
				node._x=x
				width[depth]=x+nw+self.__interval[0]
				for d in range(depth+1,len(width)):#无脑更新depth后面的width
					width[d]=max(width[d],width[depth])
				for child in children:#将子节点的绝对位置重新调整为相对位置
					child._x=child._x-tx#由child._x-x+(x-tx)化简而来
				group.pop()#该节点的数据已确定，将其移除
		if True:#将根节点坐标设置为指定位置，并且将所有的节点由相对坐标改为绝对坐标
			node:TreeNode=self[0]
			L,T=self.__rootPos
			R,B=L+self.__NodeWidth(node),T+self.__NodeHeight(node)
			node._x,node._y=L,T
			stk=[node]
			while(stk):
				node=stk.pop()
				children=[self[id] for id in node[1:] if id not in coincidents and self[id]._node_isVisible!=-1]
				for child in children:
					child._x+=node._x
					child._y+=node._y
					R=max(child._x+self.__NodeWidth(child),R)
					B=max(child._y+self.__NodeHeight(child),B)
					L=min(child._x,L)
					T=min(child._y,T)
				stk.extend(children)
			self.__geometry=[int(L),int(T),int(R-L),int(B-T)]
	def __NodeWidth(self,node:TreeNode):
		return node._w if node._w else self.__nodeSize[0]
	def __NodeHeight(self,node:TreeNode):
		return node._h if node._h else self.__nodeSize[1]


