
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_ArrayTree']

from typing import List,Dict,Set,Type,Iterable

class XJ_ArrayTree(list):
	'''
		简单的数组树，第0个元素是根节点。
		节点类型为List[int](以及派生类)，其中第0个元素为父节点索引(-1为无效索引，即父节点不存在)，其余为子节点索引。

		允许逻辑成环，但会记录重合点位置
	'''
	class __Position:
		'''
			间接记录问题节点的位置
		'''
		parent:int#父节点索引
		index:int#所在位置
		def __init__(self,p:int,i:int):
			self.parent=p
			self.index=i
	__invalid:List[__Position]#无效点位置
	__coincident:Dict[int,List[__Position]]#汇集点/重合点位置
	__detached:Set[int]#游离节点索引
	def __init__(self,nodeClass:Type[List[int]]=list):
		'''
			传入节点类型，
			后续调用append和insert时会将元素转为该类型，并且节点(List[int])长度为0时自动追加-1
		'''
		self.__invalid=[]
		self.__coincident={}
		self.__detached=set()
		self.__nodeClass=nodeClass
		self.append([])
	def append(self,obj:object):
		if(isinstance(obj,list)):
			super().append(self.__NewNode(obj))
			return True
		return False
	def extend(self,lst:Iterable[object]):
		for obj in lst:
			self.append(obj)
	def insert(self,index:int,obj:object):
		if(isinstance(obj,list)):
			super().insert(index,self.__NewNode(obj))
			return True
		return False
	def Get_CoincidentNodes(self):
		'''
			获取重合点位置。
			返回的是Dict[int,List[Position]]，其中int代表重合点索引值，List[Position]记录那些重合的问题节点的位置
		'''
		return self.__coincident
	def Get_InvalidNodes(self):
		'''
			获取无效点位置(索引对应节点不存在)。
			返回的是List[Position]
		'''
		return self.__invalid
	def Get_DetachedNodes(self):
		'''
			获取游离点(不与根节点有任何联系)索引。
		'''
		return self.__detached
	def Get_NodeCount(self):
		'''
			获取节点个数(实际是返回len(tree))
		'''
		return len(self)
	def Get_IndexIsExist(self,index:int):
		'''
			判断索引是否有效(实际是返回0<=index<len(tree))
		'''
		return 0<=index<len(self)
	def Get_NodeChild(self,index:int):
		'''
			获取子节点索引列表(实际是返回tree[index][1:])
		'''
		return self[index][1:]
	def Get_NodeParent(self,index:int):
		'''
			获取父节点索引(实际是返回tree[index][0])
		'''
		return self[index][0]
	def Opt_Update(self):
		'''
			在数据发生变动后都需要进行手动更新。
			会更新每个节点的父索引。
		'''
		self.__coincident.clear()
		self.__invalid.clear()
		self.__detached.clear()
		length=len(self)
		if(length==0):
			return False
		self.__detached=set(range(1,length))
		stk=[0]
		while(stk):
			i=stk.pop()
			j=0
			children=self[i][:0:-1]#倒序(已去除父索引)，以便深度遍历
			for n in children:
				j+=1
				if(n>=length):
					self.__invalid.append(self.__Position(i,j))
				else:
					c=self[n]
					if(len(c)==0):
						c.append(-1)
					c[0]=i#设置父索引
					if(n in self.__detached):
						self.__detached.discard(n)
						stk.append(n)
				self.__coincident.setdefault(n,[]).append(self.__Position(i,j))
		key=[]
		for i in self.__detached:
			for n in self[i][1:]:
				if(n>=length):
					self.__invalid.append(self.__Position(i,j))
				else:
					c=self[n]
					if(len(c)==0):
						c.append(-1)
					c[0]=i#设置父索引
		for i in self.__coincident:
			lst=self.__coincident[i]
			if(len(lst)==1 and i>0):
				key.append(i)
			else:
				lst.reverse()
		for k in key:
			self.__coincident.pop(k)
		return True
	def Opt_TreeClear(self):
		'''
			清除树，只留下根节点。
		'''
		del self[1:]
		del self[0][1:]
		return True
	def Opt_NodeNewChild(self,index_target:int,index_child:int=-1,pos:int=-1):
		'''
			在目标节点的子节点列表指定位置中插入索引index_child。
			如果index_child为负值则自动创建新节点(节点类型已在初始化时确定)，
			在此基础上index_target也为负值的话将创建游离的点，效果等同于tree.append([])；
			返回子节点。
		'''
		length=len(self)
		if(index_target<length):
			if(pos<0):
				pos=2**30
			if(index_child<0):
				index_child=length
				self.append([])
			if(index_target>=0):
				self[index_target].insert(pos+1,index_child)
			return self[index_child]
		return None
	def Opt_NodeMove(self,index_src:int,index_target:int,pos:int=-1):
		'''
			在进行该操作前务必调用Opt_Update进行更新。
			将src节点移动到target节点下，可指定是第几个子节点(默认最右)。
			明显的，如果src是target的父节点那么将移动失败。
			如果节点不存在也将移动失败。
		'''
		t=index_target
		length=len(self)
		if(index_src>=length):#不处理节点不存在的情况
			return False
		if(index_src==0):#不移动根节点
			return False
		while(t>0):#避免src移至src子节点下(要这么做也不是不行，就是没什么意义，搞出一堆游离点并没有什么好处)
			if(t==index_src or t>=length):
				return False
			t=self[t][0]
		if(pos<0):
			pos=2**30
		nodeSrc=self[index_src]
		nodeTarget=self[index_target]
		index_parent=[item[0] for item in self.__coincident.get(index_src,[nodeSrc[0],-1])]
		for p in index_parent:
			if(0<=p<length):
				i=self[p].index(nodeSrc,1)
				if(i>0):
					self[p].pop(i)
		nodeSrc[0]=index_target
		nodeTarget.insert(pos,index_src)
		return True
	def __NewNode(self,lst:list):
		node=self.__nodeClass(lst)
		if(len(node)==0):
			node.append(-1)
		return node		


