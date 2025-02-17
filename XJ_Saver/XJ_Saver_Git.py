

from .XJ_Saver_Base import XJ_Saver_Base
# from .XJQ_Thread import XJQ_Thread
from .XJ_Git import XJ_Git
from .XJ_GitRecord import XJ_GitRecord
from typing import List,Dict,Callable
from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
from XJ.Widgets.XJQ_LoadingAnimation import XJQ_LoadingAnimation
from XJ.Widgets.XJQ_TextInputDialog import XJQ_TextInputDialog

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from XJ.Widgets.XJQ_Mask import XJQ_Mask
from threading import Thread


class GitOperator:
	'''
		将git相关的各种耗时操作移至此处完成(开辟一条线程单独执行任务)
	'''
	__th:Thread
	__msk:XJQ_Mask
	__vtree:XJQ_VisibleTree
	__gr:XJ_GitRecord
	__dlg_pathChange:QMessageBox
	__dlg_textInput:XJQ_TextInputDialog
	__loop:QEventLoop
	def __init__(self,vtree:XJQ_VisibleTree,gr:XJ_GitRecord):
		self.__th=Thread()
		self.__msk=XJQ_Mask(vtree.Get_Canvas())

		self.__vtree=vtree
		self.__gr=gr
		self.__dlg_pathChange=QMessageBox(QMessageBox.Icon.Question,"切换路径","是否切换仓库路径？")
		self.__dlg_textInput=XJQ_TextInputDialog(parent=vtree.Get_Canvas())
		self.__loop=QEventLoop()
		
		dlg=self.__dlg_pathChange
		dlg.addButton("取消",QMessageBox.ButtonRole.NoRole)
		dlg.addButton("确认",QMessageBox.ButtonRole.YesRole)

		msk=self.__msk
		la=XJQ_LoadingAnimation()
		msk.Set_CenterWidget(la)
	def Opt_SetPath(self,path:str):
		'''
			设置仓库路径。
			如果path为空则运行时会打开文件选择窗口
		'''
		if(not self.Get_IsRunning()):
			self.__th=Thread(target=self.__Th_Run,args=(self.__Load,path))
			self.__th.start()
	def Opt_AddCommit(self,commit:str):
		'''
			添加提交。
			如果info为空则弹出文本输入框
		'''
		if(not self.Get_IsRunning()):
			self.__th=Thread(target=self.__Th_Run,args=(self.__AddCommit,commit))
			self.__th.start()
	def Opt_AddBranch(self,branch:str):
		'''
			添加分支。
			如果branch为空则弹出文本输入框
		'''
		if(not self.Get_IsRunning()):
			self.__th=Thread(target=self.__Th_Run,args=(self.__AddBranch,branch))
			self.__th.start()
	def Opt_Merge(self,*commits:str):
		'''
			合并分支。
		'''
		if(not self.Get_IsRunning()):
			self.__th=Thread(target=self.__Th_Run,args=(self.__Merge,*commits))
			self.__th.start()
	def Opt_Checkout(self,commit:str):
		'''
			恢复备份
		'''
		if(not self.Get_IsRunning()):
			self.__th=Thread(target=self.__Th_Run,args=(self.__Checkout,commit))
			self.__th.start()
	def Get_IsRunning(self):
		return self.__th.is_alive()
	def __Load(self,path:str):
		'''
			加载git信息。
			如果path为空则弹出路径选择框
		'''
		print("!!!",path)
		gr=self.__gr
		if(path==None):
			print("A")
			if(self.__dlg_pathChange.exec()):
				print("B")
				path=QFileDialog.getExistingDirectory()
			print("C")
		return
		if(path):
			if(gr.Opt_LoadFromLocal(path)):
				self.__vtree.Opt_Update()
				btn=self.__vtree.Get_Node(0)
				btn.setText(path)
			else:
				QMessageBox.about(None,"失败","无效的git路径")
	def __AddCommit(self,info:str=None):
		'''
			添加提交。
			如果info为空则弹出文本输入框
		'''
		if(not info):
			self.__dlg_textInput.setWindowTitle("输入")
		info=self.__dlg_textInput.exec()
		if(info):
			XJ_Git.Opt_AddCommit(info,self.__gr.path)
			self.__gr.Opt_AddCommit()
	def __AddBranch(self,branch:str=None):
		'''
			添加分支。
			如果branch为空则弹出文本输入框
		'''
		if(not branch):
			self.__dlg_textInput.setWindowTitle("输入")
		branch=self.__dlg_textInput.exec()
		if(branch):
			XJ_Git.Opt_AddBranch(branch,self.__gr.path)
			self.__gr.Opt_AddBranch()
	def __Merge(self,*commits:str):
		'''
			合并分支。
			如果commits为空则弹出选择框(?)
		'''
		pass
	def __Checkout(self,commit:str):
		'''
			恢复备份
		'''
		if(commit):
			XJ_Git.Opt_Recover(commit,True,self.__gr.path)
			self.__gr.Opt_Checkout()
	def __Th_Run(self,func:Callable,*args):
		'''
			给线程使用
		'''
		self.__msk.show()
		self.__msk.setGeometry(-1000,-1000,1500,1500)
		func(*args)
		self.__msk.hide()



class XJ_Saver_Git(XJ_Saver_Base):
	'''
		基于Git的数据存储恢复器
	'''
	def __init__(self):
		super().__init__()
		self.__gr=XJ_GitRecord(self._vtree.Get_Tree())
		btn=self._vtree.Get_Node(0)
		self._vtree.Get_Tree().Set_NodeSize(0,400,50)
		btn.setText('选择路径')
		self.__go=GitOperator(self._vtree,self.__gr)

		btn.clicked.connect(lambda:self.Set_Path())
		# btn.clicked.connect(self.Dlg_SelectPath)
		self.Opt_Update()
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		cmd='git status -s'
	def Opt_CreateBackup(self,info:str):
		cmd='git commit'
	def Set_Path(self,path:str=None):
		'''
			设置路径。
			如果path为None则打开对话框进行选择
		'''
		self.__go.Opt_SetPath(path)
		# self.__go.Opt_Run()
	def Opt_Recover(self,id:int):
		if(0<=id<len(self.__gr.commits)):
			XJ_Git.Opt_Recover(self.__gr.commits[id],True,self._path)
			self.__gr.Opt_Checkout()
			self.Opt_Update()
	def Opt_Update(self):
		super().Opt_Update()
		# gr=self.__gr
		# path=self._path



