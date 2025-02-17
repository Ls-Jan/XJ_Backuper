
__author__='Ls_Jan'
__version__='1.0.0'
__all__=['XJ_Git']

from typing import List
from datetime import datetime
from .RunCMD import RunCMD
import os

class XJ_Git:
	class Get_BranchNames:
		'''
			获取所有的分支名。
		'''
		nameLst:List[str]#分支名列表
		headName:str#HEAD所在分支/提交
		headIsDetached:bool#HEAD是否游离
		success:bool
		def __init__(self,path:str='.'):
			cmd=f'git branch'
			lst=RunCMD(cmd,path)
			rst=[]
			head=""
			detached=False
			self.success='cannot find the path' not in lst[0]
			if(self.success):
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
			cmd_s=f'git log {branchName} --oneline --' if branchName else f'git log --oneline --all'
			lst=RunCMD(cmd_s,path,lambda row:row.split(maxsplit=1)[0])
			self.success='fatal:' not in lst[0]
			self.commits=[]
			if(self.success):
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
			cmd_s=f'git log --oneline -n {count}'
			lst=RunCMD(cmd_s,path,lambda row:row[:row.find(' ')])
			self.success='cannot find the path' not in lst[0]
			self.commits=lst if self.success else []
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
			self.success='cannot find the path' not in lst[0]
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
		flag:bool
		def __init__(self,path:str='.'):
			self.flag=os.path.isdir(os.path.join(path,'.git'))
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
		def __init__(self,info:str='',path:str='.'):
			'''
				info为空则使用当前时间(datetime.datetime.now())，注意不要使用英文双引号。
			'''
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
		def __init__(self,commitID:str,force:bool=False,path:str='.'):
			'''
				force为真则强制切换，
				会将当前改动全部丢失(请确保是不重要数据)
			'''
			cmd=f'git checkout {"-f" if force else ""} {commitID}'
			self.info='\n'.join(RunCMD(cmd,path))
			self.success='error:' not in self.info
	class Opt_AddBranch:
		'''
			在当前位置添加分支
		'''
		info:str
		success:bool
		def __init__(self,branchName:str,path:str='.'):
			cmd=f'git switch -c {branchName}'
			self.info='\n'.join(RunCMD(cmd,path))
			self.success='error:' not in self.info and 'fatal:' not in self.info






