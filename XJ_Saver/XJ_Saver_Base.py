


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from XJ.Structs.XJ_ArrayTree import XJ_ArrayTree
from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree

class XJ_Saver_Base:
	'''
		数据存储恢复器基类。
		图形化显示基于Qt和控件XJ.Widgets.XJQ_VisibleTree
	'''
	def __init__(self):
		self._vtree=XJQ_VisibleTree()
		self._path='.'
	def Set_Path(self,path:str):
		'''
			切换路径
		'''
		self._path=path
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		'''
			source与target进行比较，获取文件变化信息。
			如果source为空则默认当前节点位置；
			如果target为空则与目标路径进行比较；
		'''
		pass
	def Opt_CreateBackup(self,info:str):
		'''
			在当前位置创建备份(commit)
		'''
		pass
	def Opt_Recover(self,id:int):
		'''
			跳转到指定位置并恢复备份
		'''
		pass
	def Opt_Update(self):
		'''
			刷新界面
		'''
		self._vtree.Opt_Update()


