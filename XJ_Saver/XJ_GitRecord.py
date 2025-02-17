
from .XJ_Git import XJ_Git
from typing import List,Dict


class XJ_GitRecord:
	'''
		git信息记录
	'''
	def __init__(self,tree:List[List[int]]):
		self.path:str='.'#git路径
		self.tree:List[List[int]]=tree#数组树(首元素为根节点)
		self.branchCommits:Dict[str,List[str]]={}#分支名到commitID列表
		self.commitIndex:Dict[str,int]={}#commitID到节点索引
		self.commits:List[str]=[]#节点索引到commitID
		self.merges:Dict[str,List[str]]={}#合并的commitID以及相应的父commitID列表
		self.coincident:Dict[int,int]={}#逻辑节点索引到实际节点索引(将环打断成树)
		self.isDetached:bool=False#HEAD是否脱离(不指向分支)
		self.headIndex:int=0#HEAD对应的节点索引
		self.branchIndex:Dict[str,int]={}#分支对应的节点索引
	def Opt_LoadFromLocal(self,path:str):
		'''
			加载git信息。
			如果路径无效则返回False并且不做任何动作。
		'''
		if(not XJ_Git.Test_RepositoryExist(path).flag):
			return False
		self.path=path
		tree=self.tree
		commits=self.commits
		branchCommits=self.branchCommits
		commitIndex=self.commitIndex
		merges=self.merges
		coincident=self.coincident
		branchIndex=self.branchIndex
		headName=''
		if True:#更新self.isDetached、branchCommits、headName、merges
			rst=XJ_Git.Get_BranchNames(path=path)
			self.isDetached=rst.headIsDetached
			branchCommits.clear()
			for name in rst.nameLst:
				branchCommits[name]=XJ_Git.Get_BranchCommits(name,path=path).commits
			headName=rst.headName if self.isDetached else branchCommits[rst.headName][0]
			merges.clear()
			for merge in XJ_Git.Get_Merges(path=path).mergeLst:
				merges[merge.id]=merge.parents
		if True:#更新tree、commits、commitIndex、branchIndex、self.headIndex
			commitIndex.clear()
			commits.clear()
			del tree[1:]
			del tree[0][1:]
			for branch in branchCommits:
				n:list=tree[0]
				for id in reversed(branchCommits[branch]):#由旧到新
					if(id not in commitIndex):
						tree.append([-1])
						commits.append(id)
					i=commitIndex.setdefault(id,len(commits))
					if(i not in n[1:]):
						n.append(i)
					n=tree[i]
			branchIndex.clear()
			for name in branchCommits:
				branchIndex[name]=commitIndex[branchCommits[name][0]]
			self.headIndex=commitIndex[headName]
		if True:#更新coincident
			coincident.clear()
			for merge,parents in merges.items():#更新tr，处理成环点
				i=commitIndex[merge]
				for n in parents[1:]:#新增节点
					j=commitIndex[n]
					tree[j].append(len(tree))
					coincident[len(tree)]=i
					tree.append([-1])
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
			self.headIndex=index
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
			id=merge.id
			if(id not in self.merges):
				parents=[self.commitIndex[p] for p in merge.parents]
				i=commitIndex[id]
				for n in parents[1:]:#新增节点
					j=commitIndex[n]
					tree[j].append(len(tree))
					coincident[len(tree)]=i
					tree.append([-1])
		return True
	def Opt_AddBranch(self):
		'''
			同步新增分支动作
		'''	
		for name in XJ_Git.Get_BranchNames().nameLst:
			if(name not in self.branchCommits):
				self.branchCommits[name]=XJ_Git.Get_BranchCommits(name,path=self.path).commits
				self.branchIndex[name]=self.commitIndex[self.branchCommits[name][0]]
		return True
	def Opt_Checkout(self):
		'''
			同步恢复操作（切换HEAD)
		'''
		rst=XJ_Git.Get_BranchNames()
		self.headIndex=self.commitIndex[rst.headName] if rst.headIsDetached else self.branchIndex[rst.headName]
		self.isDetached=rst.headIsDetached
		return True
	

	