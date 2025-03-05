
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['XJ_GitRecord']

from .XJ_Git import XJ_Git
from typing import List,Dict

class XJ_GitRecord:
	'''
		git信息记录
	'''
	def __init__(self,tree:List[List[int]],functonalRoot:bool=True):
		'''
			如果functionalRoot为真，则根节点用于特殊用途，真正的初始节点从1开始
		'''
		self.functonalRoot=functonalRoot#功能根节点
		self.path:str='.'#git路径
		self.tree:List[List[int]]=tree#数组树(首元素为根节点)
		self.commitID:List[str]=[]#节点索引到commitID(从旧到新排列)
		self.commitIndex:Dict[str,int]={}#commitID到节点索引
		self.branchIndex:Dict[str,int]={}#分支对应的节点索引
		self.merges:Dict[str,List[int]]={}#合并的commit对应的节点索引以及相应的父节点索引列表
		self.coincident:Dict[int,int]={}#逻辑节点索引到实际节点索引(将环打断成树)
		self.headIndex:int=0#HEAD对应的节点索引
		self.headBranch:str=''#HEAD对应的分支(为空则说明脱离)
	def Opt_LoadFromLocal(self,path:str):
		'''
			加载git信息。
			如果路径无效则返回False并且不做任何动作。
		'''
		if(not XJ_Git.Test_CommitExist(path=path).valid):
			return False
		self.path=path
		tree=self.tree
		commitID=self.commitID
		commitIndex=self.commitIndex
		merges=self.merges
		coincident=self.coincident
		if True:#更新commitID、commitIndex、tree
			commitIndex.clear()
			commitID.clear()
			if(self.functonalRoot):#保留根节点，同时commitID也塞进无效的首元素以便同步tree
				del tree[1:]
				del tree[0][1:]
				commitID.append("")#插入空数据
				tree[0].append(1)
			else:#不保留根节点
				tree.clear()
			commitID.extend(reversed(XJ_Git.Get_RecentCommits(-1,path).commits))
			for i in range(1 if self.functonalRoot else 0,len(commitID)):
				commitIndex[commitID[i]]=i
				tree.append([-1])
		if True:#更新self.headBranch、self.branchIndex、self.headIndex、merges
			rst=XJ_Git.Get_BranchCommits(path=path)
			self.headBranch=rst.headBranch
			self.branchIndex.clear()
			for branch,commit in rst.branchCommit.items():
				self.branchIndex[branch]=commitIndex[commit]
			self.headIndex=self.branchIndex.pop('HEAD')
			merges.clear()
			for merge in XJ_Git.Get_Merges(path=path).mergeLst:
				merges[commitIndex[merge.id]]=[commitIndex[p] for p in merge.parents]
		if True:#更新tree
			rst=XJ_Git.Get_CommitChildren(path)
			stk=[rst.rootCommit]
			children=rst.children
			while(stk):
				curr=stk.pop()
				n:list=tree[commitIndex[curr]]
				for key in children[curr]:
					i=commitIndex[key]
					if(i not in n[1:]):
						n.append(i)
				stk.extend(reversed(children[curr]))
			# for node in tree:
				# node[1:]=sorted(node[1:])
		if True:#更新coincident、tree、commitID
			coincident.clear()
			for merge,parents in merges.items():#更新tr，处理成环点
				for p in parents[1:]:#新增节点
					tree[p].remove(merge)
					tree[p].append(len(tree))
					coincident[len(tree)]=merge
					tree.append([-1])
					commitID.append(commitID[merge])#插入相应数据
		return True
	def Opt_AddCommit(self):
		'''
			同步提交动作。
		'''
		commitID=XJ_Git.Get_RecentCommits(1,self.path).commits[0]
		if(commitID not in self.commitIndex):
			index=len(self.tree)
			self.tree[self.headIndex].append(index)
			self.tree.append([self.headIndex])
			self.commitIndex[commitID]=index
			self.commitID.append(commitID)
			self.headIndex=index
			if(self.headBranch):
				self.branchIndex[self.headBranch]=index
		return True
	def Opt_Merge(self):
		'''
			同步合并动作。
		'''
		self.Opt_AddCommit()
		commitIndex=self.commitIndex
		tree=self.tree
		coincident=self.coincident
		for merge in XJ_Git.Get_Merges(self.path).mergeLst:
			id=commitIndex[merge.id]
			if(id not in self.merges):
				for p in merge.parents[1:]:#新增节点
					p=commitIndex[p]
					tree[p].append(len(tree))
					coincident[len(tree)]=id
					tree.append([-1])
		return True
	def Opt_AddBranch(self):
		'''
			同步新增分支动作
		'''	
		branchCommit=XJ_Git.Get_BranchCommits(self.path).branchCommit
		for branch in branchCommit:
			if(branch not in self.branchIndex):
				self.branchIndex[branch]=self.commitIndex[branchCommit[branch]]
		return True
	def Opt_Checkout(self):
		'''
			同步恢复操作（切换HEAD)
		'''
		rst=XJ_Git.Get_BranchCommits(self.path)
		branchCommit=rst.branchCommit
		self.headIndex=self.commitIndex[branchCommit['HEAD']]
		self.headBranch=rst.headBranch
		return True
	

	