
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['XJ_Git']

from typing import List,Dict,Tuple
from datetime import datetime
from .RunCMD import RunCMD

class XJ_Git:
	'''
		git的部分命令简单说明：
			- checkout【仅影响HEAD】：将HEAD指向指定的<commit>；
			- reset【影响HEAD以及所指分支】：将HEAD分支的位置搬到其他地方(非常简单暴力)，不一定只是回溯/回滚；
			- switch【仅影响HEAD】：将HEAD指向指定分支，是checkout的特化；
			- restore【不影响HEAD】：恢复文件，但不像checkout一样移动HEAD，使用--staged将撤回git add的行为(即重置“暂存区”)；
			- clean【不影响HEAD】：将工作区中未跟踪的文件全部清除(非常暴力)；
			- add【不影响HEAD】：记录工作区中的改动，它不仅作用于commit命令，也作用于stash命令；
			- commit【影响HEAD以及所指分支】：将改动记录进行提交；
			- stash save【不影响HEAD】：和commit一样，会进行记录提交，不同的是这个<commit>是临时的，并且HEAD不移动、工作区会还原到HEAD的状态，用于保存当前工作记录并将工作区还原至初始状态；
			- stash pop【不影响HEAD】：stash save的逆操作，哪里执行的save命令就在哪里调用pop(执行save和pop时HEAD尽量指向同一<commit>不然容易冲突)；
	'''
	class Get_BranchCommits:
		'''
			获取所有的分支名。
			branchCommit也包含'HEAD'
		'''
		branchCommit:Dict[str,str]#分支名对应的<commit>。包括HEAD
		headBranch:str#HEAD指向的分支。该值为空说明HEAD游离
		success:bool
		def __init__(self,path:str='.'):
			branchCommit={}
			headBranch=''
			self.success=XJ_Git.Test_CommitExist(None,path).valid
			if(self.success):
				cmd=f'git branch'
				lst=RunCMD(cmd,path)
				lst.append('HEAD')#HEAD也添加进其中
				for key in lst:
					if('*' in key):
						key=key[key.find('*')+1:].strip()#如果head指向分支那么会直接在分支名前打上星号
						if('(' in key):#游离HEAD特有的小括号标志，其中除了“at”之外还有“from”
							continue
						headBranch=key
					cmd=f'git rev-parse --short {key}'
					branchCommit[key]=RunCMD(cmd,path)[0]
			self.branchCommit=branchCommit
			self.headBranch=headBranch
	class Get_CommitChildren:
		'''
			获取所有提交的子提交。
			shortHashLen用于指定获取到的commitID的长度，该值通常为7
		'''
		children:Dict[str,List[str]]
		rootCommit:str
		success:bool
		def __init__(self,path:str='.',shortHashLen:int=7):
			self.children={}
			self.rootCommit=''
			self.success=XJ_Git.Test_CommitExist(None,path).valid
			if(self.success):
				cmd=f'git rev-list --children --all'#实在找不到短哈希相关的可选项，只能获取后手动截断
				lst=[row.split() for row in RunCMD(cmd,path)]
				for item in lst:
					item=[key[:shortHashLen] for key in item]
					curr,children=item[0],item[1:]
					self.children[curr]=children
				cmd='git log --children --oneline HEAD --format="%h"'
				self.rootCommit=RunCMD(cmd,path)[-1]
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
			self.success=XJ_Git.Test_CommitExist(None,path).valid
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
			self.success=XJ_Git.Test_CommitExist(None,path).valid
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
	class Get_ChangedFiles:
		'''
			获取发生变化的文件
		'''
		add:List[str]
		modify:List[str]
		delete:List[str]
		rename:List[Tuple[str,str]]
		unknown:Dict[str,List[str]]#未知改动
		success:bool
		changed:bool
		def __init__(self,commitSource:str=None,commitTarget:str=None,path:str='.'):
			'''
				提供源commit和目标commit进行比较，获取文件变化。
				如果commitTarget=None则默认当前工作区；
				如果commitSource=None则默认HEAD；
			'''

			self.success=XJ_Git.Test_CommitExist(None,path).valid
			self.changed=False
			self.unknown={}
			record={
				'A':[],
				'M':[],
				'D':[],
				'R':[],
			}
			if(self.success):
				if(commitSource==None):
					commitSource='HEAD'
				if(commitTarget==None):
					commitTarget=''
				cmd=f'git add . && git diff {commitSource} {commitTarget} --name-status'
				lst=RunCMD(cmd,path)
				self.success=lst[0].find('fatal:')!=0
				if(self.success):
					self.changed=bool(lst[0])
					if(self.changed):
						for row in lst:
							mark,file=row.split(maxsplit=1)
							if(mark in record):
								record[mark].append(file)
							else:
								if(mark[0]=='R'):
									fileOld,fileNew=file.split('\t')
									if(mark[1]!='1'):#不是100%
										record['D'].append(fileOld)
										record['A'].append(fileNew)
									else:
										record['R'].append((fileOld,fileNew))
								else:
									self.unknown.setdefault(mark,[]).append(file)
			self.add=record['A']
			self.modify=record['M']
			self.rename=record['R']
			self.delete=record['D']
	class Test_CommitExist:
		'''
			判断路径下的仓库是否存在
		'''
		info:str
		valid:bool
		def __init__(self,commitID:str=None,path:str='.'):
			'''
				commitID为None视为HEAD，
				即则可用于判断仓库路径是否有效
			'''
			if(commitID==None):
				commitID='HEAD'
			cmd=f'git rev-parse --short {commitID}'
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
			rst=XJ_Git.Test_CommitExist(None,path)
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
			rst=XJ_Git.Test_CommitExist(None,path)
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
			rst=XJ_Git.Test_CommitExist(None,path)
			self.info=rst.info
			self.success=rst.valid
			if(self.success):
				cmd=f'git switch -c {branchName}'
				self.info='\n'.join(RunCMD(cmd,path))
	class Opt_ChangeBranch:
		'''
			改变HEAD指向的分支。
			不会改变工作区文件。
			亦可传入commit哈希进行切换。
			采用git stash、git checkout、git restore组合拳实现该功能。
			虽然git reset --soft一样可以只移动HEAD但它只能移至提交而没法指向分支。
		'''
		info:str
		success:bool
		def __init__(self,branchName:str,path:str='.'):
			rst=XJ_Git.Test_CommitExist(None,path)
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






