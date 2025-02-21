

from .XJQ_Saver_Base import XJQ_Saver_Base
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
from time import sleep
import os

class GitOperator:
	'''
		将git相关的各种耗时操作移至此处完成(开辟一条线程单独执行任务)
	'''
	__th:Thread
	__mskBusy:XJQ_Mask
	__vtree:XJQ_VisibleTree
	__gr:XJ_GitRecord
	__dlg_pathChange:QMessageBox
	__dlg_textInput:XJQ_TextInputDialog
	__loop:QEventLoop
	__optSuccess:bool
	def __init__(self,parent:QWidget,vtree:XJQ_VisibleTree,gr:XJ_GitRecord):
		self.__th=Thread()
		self.__mskBusy=XJQ_Mask(parent,QColor(0,0,0,128))

		self.__vtree=vtree
		self.__gr=gr
		self.__dlg_pathChange=QMessageBox(QMessageBox.Icon.Question,"切换路径","是否切换仓库路径？")
		self.__dlg_textInput=XJQ_TextInputDialog(parent=parent)
		self.__loop=QEventLoop()
		
		dlg=self.__dlg_pathChange
		dlg.addButton("取消",QMessageBox.ButtonRole.NoRole)
		dlg.addButton("确认",QMessageBox.ButtonRole.YesRole)

		msk=self.__mskBusy
		la=XJQ_LoadingAnimation()
		la.Set_Text(textFunc=lambda arg:'处理中'+'.'*arg)
		msk.Set_CenterWidget(la)
		msk.hide()
	def Opt_SetPath(self,path:str):
		'''
			设置仓库路径。
			如果path为空则运行时会打开文件选择窗口
		'''
		if(self.Get_IsRunning()):
			return
		if(path==None):
			if(self.__dlg_pathChange.exec()):
				path=QFileDialog.getExistingDirectory()
		if(path):
			gr=self.__gr
			self.__mskBusy.show()
			self.__th=Thread(target=self.__Th_Run,args=(gr.Opt_LoadFromLocal,path))
			self.__th.start()
			self.__loop.exec()
			if(self.__optSuccess):
				vtree=self.__vtree
				vtree.Opt_Update()
				btn=vtree.Get_Node(0)
				btn.setText(os.path.split(os.path.abspath(path))[-1])
				for i in range(len(vtree.Get_Tree())):
					btn=vtree.Get_Node(i)
					btn.setText(f'{i}')
				for merge in gr.merges:
					btn=vtree.Get_Node(merge)
					btn.setText(f'>{merge}')
					# for p in parents[1:]:
					# 	btn=vtree.Get_Node(p)
					# 	btn.setText(f'{merge}>')
				for lid,rid in gr.coincident.items():
					btn=vtree.Get_Node(lid)
					btn.setText(f'*{rid}')
					# btn.setText(f'*{btn.text()}')
				for branch,id in gr.branchIndex.items():
					btn=vtree.Get_Node(id)
					vtree.Get_Tree().Set_NodeSize(id,200,50)
					btn.setText(f'{btn.text()}\n{branch}')
					# print(id,btn.text())
				vtree.Opt_Update()
			else:
				QMessageBox.about(self.__vtree.Get_Canvas(),"失败","无效的git路径")
			self.__mskBusy.hide()
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

	def __Th_Run(self,func:Callable,*args):
		'''
			将耗时操作传入单独线程中完成。
		'''
		sleep(0.1)
		self.__optSuccess=func(*args)
		self.__loop.quit()
	# def __Clicked(self):



	#废弃
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



class XJQ_Saver_Git(XJQ_Saver_Base):
	'''
		基于Git的数据存储恢复器
	'''
	def __init__(self):
		super().__init__()
		self.__gr=XJ_GitRecord(self._vtree.Get_Tree())
		self.__go=GitOperator(self,self._vtree,self.__gr)
		self._vtree.Get_Node(0).setText('选择路径')
		# self._vtree.Get_Tree().Set_NodeSize(-1,100,50)
		self._vtree.Get_Tree().Set_NodeSize(0,400,50)
		self._vtree.Get_ClickedSignal().connect(lambda index:self.Set_Path() if index==0 else print("AAA"))
		self.Opt_Update()
	# def _
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		cmd='git status -s'
	def Opt_CreateBackup(self,info:str):
		rst=XJ_Git.Opt_AddCommit(info,self._path)
	def Set_Path(self,path:str=None):
		'''
			设置路径。
			如果path为None则打开对话框进行选择
		'''
		self.__go.Opt_SetPath(path)
		# self.__go.Opt_Run()
	def Opt_Recover(self,id:int):
		return
		if(0<=id<len(self.__gr.commitID)):
			rst=XJ_Git.Opt_Recover(self.__gr.commitID[id],True,self._path)
			print(rst.info)
			self.__gr.Opt_Checkout()
			self.Opt_Update()
	def Opt_Update(self):
		super().Opt_Update()
		# gr=self.__gr
		# path=self._path



