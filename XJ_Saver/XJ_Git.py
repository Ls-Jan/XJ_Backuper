
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['XJ_Git']

from typing import List
from datetime import datetime
from .RunCMD import RunCMD

class XJ_Git:
	'''
		git的部分命令简单说明：
			- checkout【仅影响HEAD】：将HEAD指向指定的<commit>；
			- reset【影响HEAD以及所指分支】：将HEAD分支的位置搬到其他地方(非常简单暴力)，不一定只是回溯/回滚；
			- switch【仅影响HEAD】：将HEAD指向指定分支，是checkout的特化；
			- restore【不影响HEAD】：恢复文件，但不像checkout一样移动HEAD；
			- clean【不影响HEAD】：将工作区中未跟踪的文件全部清除(非常暴力)；
			- add【不影响HEAD】：记录工作区中的改动，它不仅作用于commit命令，也作用于stash命令；
			- commit【影响HEAD以及所指分支】：将改动记录进行提交；
			- stash save【不影响HEAD】：和commit一样，会进行记录提交，不同的是这个<commit>是临时的，并且HEAD不移动、工作区会还原到HEAD的状态，用于保存当前工作记录并将工作区还原至初始状态；
			- stash pop【不影响HEAD】：stash save的逆操作，哪里执行的save命令就在哪里调用pop(执行save和pop时HEAD尽量指向同一<commit>不然容易冲突)；
	'''
	class Get_BranchNames:
		'''
			获取所有的分支名。
		'''
		nameLst:List[str]#分支名列表
		headName:str#HEAD所在分支/提交
		headIsDetached:bool#HEAD是否游离
		success:bool
		def __init__(self,path:str='.'):
			rst=[]
			head=""
			detached=False
			self.success=XJ_Git.Test_RepositoryExist(path).valid
			if(self.success):
				cmd=f'git branch'
				lst=RunCMD(cmd,path)
				for row in lst:
					if('*' in row):
						row=row[row.find('*')+1:].strip()
						head=row
						if('(' in row):
							detached=True
							head=row[row.find('at')+3:-1]
							continue
					rst.append(row)
			self.nameLst=rst
			self.headName=head
			self.headIsDetached=detached
	class Get_BranchCommits:
		'''
			获取指定分支名下的所有提交(由新到旧排列)。
			pure为真时会排除掉merge引入的提交(注意，它并不同于git log --nomerge)。
		'''
		commits:List[str]
		success:bool
		def __init__(self,branchName:str='',pure:bool=True,path:str='.'):
			self.success=XJ_Git.Test_RepositoryExist(path).valid
			self.commits=[]
			if(self.success):
				cmd_s=f'git log {branchName} --oneline --' if branchName else f'git log --oneline --all'
				lst=RunCMD(cmd_s,path,lambda row:row.split(maxsplit=1)[0])
				if(pure and lst):
					target=lst[0]
					self.commits=[target]
					while(target!=lst[-1]):
						cmd_p=f'git rev-parse --short {target}~'
						target=RunCMD(cmd_p,path)[0]
						self.commits.append(target)
	class Get_RecentCommits:
		'''
			获取最近的提交。
		'''
		commits:List[str]
		success:bool
		def __init__(self,count:int=1,path:str='.'):
			'''
				count指定数量，
				count<0时将获取所有提交。
			'''
			self.success=XJ_Git.Test_RepositoryExist(path).valid
			self.commits=[]
			if(self.success):
				cmd_s=f'git log --simplify-merges --oneline --all -n {count}'
				# cmd_s=f'git log --oneline --all -n {count}'#因为提交的时间精度是秒，在一秒内如果出现多个提交(使用脚本可以达到该效果)那么将无法正确区分先后顺序
				lst=RunCMD(cmd_s,path,lambda row:row[:row.find(' ')])
				self.commits=lst
	class Get_Merges:
		'''
			获取所有merge提交。
		'''
		class Merge:
			'''
				parents的首个提交是直接父节点
			'''
			id:str
			parents:List[str]
		mergeLst:List[Merge]
		success:bool
		def __init__(self,path:str='.'):
			cmd_m=f'git log --merges --oneline --all'
			lst=RunCMD(cmd_m,path,lambda row:row.split(maxsplit=1)[0])
			rst=[]
			self.success=XJ_Git.Test_RepositoryExist(path).valid
			if(self.success):
				for id in lst:
					cmd_s=f'git show {id}'
					tmp=RunCMD(cmd_s,path,lambda row:row[row.find('Merge:'):].split()[1:])
					if(tmp):
						tmp=tmp[0]
						cmd_p=f'git rev-parse --short {id}~'
						pid=RunCMD(cmd_p,path)[0]
						i=tmp.index(pid)
						tmp[i],tmp[0]=tmp[0],tmp[i]
						mg=self.Merge()
						mg.id=id
						mg.parents=tmp
						rst.append(mg)
			self.mergeLst=rst
	class Test_RepositoryExist:
		'''
			判断路径下的仓库是否存在
		'''
		info:str
		valid:bool
		def __init__(self,path:str='.'):
			cmd='git rev-parse --short HEAD'
			rst=RunCMD(cmd,path)[0]
			self.valid=rst.find('fatal:')!=0
			self.info='' if self.valid else rst
	class Opt_InitRepository:
		'''
			指定路径下创建仓库。
		'''
		info:str
		def __init__(self,path:str='.'):
			cmd='git init'
			self.info='\n'.join(RunCMD(cmd,path))
	class Opt_AddCommit:
		'''
			创建提交
		'''
		info:str
		success:bool
		def __init__(self,info:str='',path:str='.'):
			'''
				info为空则使用当前时间(datetime.datetime.now())，注意不要使用英文双引号。
			'''
			rst=XJ_Git.Test_RepositoryExist(path)
			self.info=rst.info
			self.success=rst.valid
			if(self.success):
				if(not info):
					info=datetime.now()
				cmd=f'git add . && git commit -m "{info}"'
				lst=RunCMD(cmd,path)
				self.info='\n'.join(lst)
	class Opt_Recover:
		'''
			恢复备份。
			会使HEAD游离。
			会丢失当前改动。
		'''
		info:str
		success:bool
		def __init__(self,commitID:str,moveHead:bool=True,strict:bool=False,path:str='.'):
			'''
				会将当前改动全部丢失(请确保是不重要数据)。
				默认使用checkout(指定moveHead=True)，如果不需要移动HEAD则指定moveHead=False以使用restore进行文件恢复。
				严格模式(指定strict=True)会保证目录结构与指定commit的保持一致。
			'''
			rst=XJ_Git.Test_RepositoryExist(path)
			self.info=rst.info
			self.success=rst.valid
			if(self.success):
				rst=[]
				if(strict):
					cmd=f'git add .'
					RunCMD(cmd,path)
				if(moveHead):
					cmd=f'git checkout -f {commitID}'
				else:
					cmd=f'git restore --source {commitID} .'
				rst.extend(RunCMD(cmd,path))
				self.info='\n'.join(rst)
	class Opt_AddBranch:
		'''
			在当前位置添加分支
		'''
		info:str
		success:bool
		def __init__(self,branchName:str,path:str='.'):
			rst=XJ_Git.Test_RepositoryExist(path)
			self.info=rst.info
			self.success=rst.valid
			if(self.success):
				cmd=f'git switch -c {branchName}'
				self.info='\n'.join(RunCMD(cmd,path))
	class Opt_ChangeBranch:
		'''
			改变HEAD指向的分支。
			不会改变工作区文件。
			采用git stash、git checkout、git restore组合拳实现该功能
		'''
		info:str
		success:bool
		def __init__(self,branchName:str,path:str='.'):
			rst=XJ_Git.Test_RepositoryExist(path)
			self.info=rst.info
			self.success=rst.valid
			if(self.success):
				cmd=f'git show-branch {branchName}'
				rst=RunCMD(cmd,path)[0]
				if(rst.find('fatal:')==0):
					self.success=False
					self.info=rst
				else:
					lst=[]
					cmd='git rev-parse --short HEAD'
					cmds=[#组合拳
						'git add .',
						'git stash',
						f'git checkout -f {branchName}',
						f'git restore --source {RunCMD(cmd,path)[0]} .',
						'git add .',
						'git stash pop',
						'git reset .',
					]
					for cmd in cmds:
						rst=RunCMD(cmd,path)
						lst.extend([f'>{cmd}',rst[0]])
					self.info='\n'.join(lst)






