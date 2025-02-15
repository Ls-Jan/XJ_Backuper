

from .XJ_Saver_Base import XJ_Saver_Base
from . import XJ_Git
from .XJ_Git import XJ_Git
from .XJ_GitRecord import XJ_GitRecord
from typing import List,Dict

class XJ_Saver_Git(XJ_Saver_Base):
	'''
		基于Git的数据存储恢复器
	'''
	def __init__(self):
		super().__init__()
		self.__gr=XJ_GitRecord(self._vtree.Get_Tree())
	def Set_Path(self,path:str):
		super().Set_Path(path)
		gr=self.__gr
		if(gr.Opt_LoadFromLocal(path)):
			self._vtree.Opt_Update()
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		cmd='git status -s'
	def Opt_CreateBackup(self,info:str):
		cmd='git commit'
	def Opt_Recover(self,id:int):
		XJ_Git.Opt_Recover()
		cmd='git reset HEAD'
	def Opt_Update(self):
		pass
		# gr=self.__gr
		# path=self._path



