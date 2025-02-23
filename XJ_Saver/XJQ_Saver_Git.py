
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_Saver_Git']

from .XJQ_Saver_Base import XJQ_Saver_Base
from .XJ_Git import XJ_Git
from .XJ_GitRecord import XJ_GitRecord
from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
from XJ.Widgets.XJQ_LoadingAnimation import XJQ_LoadingAnimation
from XJ.Widgets.XJQ_TextInputDialog import XJQ_TextInputDialog
from XJ.Widgets.XJQ_Mask import XJQ_Mask

from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QEventLoop
from typing import Callable
from threading import Thread
from time import sleep
import os

class XJQ_Saver_Git(XJQ_Saver_Base):
	'''
		基于Git的数据存储恢复器
	'''
	__th:Thread
	__mskBusy:XJQ_Mask
	__gr:XJ_GitRecord
	__dlg_pathChange:QMessageBox
	__dlg_textInput:XJQ_TextInputDialog
	__loop:QEventLoop
	__optSuccess:bool
	def __init__(self,vtree:XJQ_VisibleTree=None):
		super().__init__(vtree)
		self.__th=Thread()
		self.__mskBusy=XJQ_Mask(self,QColor(0,0,0,128))

		self.__gr=XJ_GitRecord(self._vtree.Get_Tree())
		self.__dlg_pathChange=QMessageBox(QMessageBox.Icon.Question,"切换路径","是否切换仓库路径？")
		self.__dlg_textInput=XJQ_TextInputDialog(parent=self)
		self.__loop=QEventLoop()
		self.__dlg_busy=QMessageBox(QMessageBox.Icon.NoIcon,"失败","当前操作正忙")
		self.__dlg_fail=QMessageBox(QMessageBox.Icon.NoIcon,"失败","操作失败")
		
		dlg=self.__dlg_pathChange
		dlg.addButton("取消",QMessageBox.ButtonRole.NoRole)
		dlg.addButton("确认",QMessageBox.ButtonRole.YesRole)

		msk=self.__mskBusy
		la=XJQ_LoadingAnimation()
		la.Set_Text(textFunc=lambda arg:'正在处理中'+'.'*arg)
		msk.Set_CenterWidget(la)
		msk.hide()

		self.__gr=XJ_GitRecord(self._vtree.Get_Tree())
		self._vtree.Get_Node(0).setText('选择路径')
		# self._vtree.Get_Tree().Set_NodeSize(-1,100,50)
		self._vtree.Get_Tree().Set_NodeSize(0,400,50)
		self._vtree.Get_ClickedSignal().connect(lambda index:self.Set_Path(None) if index==0 else None)
		self.Opt_Update()
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		cmd='git status -s'
	def Get_IsBusy(self):
		return self.__th.is_alive()
	def Opt_CreateBackup(self,info:str):
		return self.Git_AddCommit(info)
	def Set_Path(self, path):
		return self.Git_SetPath(path)
	def Opt_Recover(self,id:int):
		if(0<=id<len(self.__gr.commitID)):
			return self.Git_Checkout(self.__gr.commitID[id])
		return False
	def Opt_Update(self):
		super().Opt_Update()
		gr=self.__gr
		vtree=self._vtree
		vtree.Opt_Update()#这一步是为了生成节点(可考虑优化)
		if True:#设置根节点
			btn=vtree.Get_Node(0)
			btn.setText(os.path.split(os.path.abspath(gr.path))[-1])
		for i in range(1,len(vtree.Get_Tree())):#给节点进行编号
			btn=vtree.Get_Node(i)
			btn.setText(f'{i}')
		for merge in gr.merges:#设置合并点
			btn=vtree.Get_Node(merge)
			btn.setText(f'>{merge}')
		for lid,rid in gr.coincident.items():#设置逻辑点
			btn=vtree.Get_Node(lid)
			btn.setText(f'{rid}')
			# btn.setStyleSheet('background:#44444444')
		for branch,id in gr.branchIndex.items():#设置分支
			btn=vtree.Get_Node(id)
			vtree.Get_Tree().Set_NodeSize(id,200,50)
			btn.setText(f'{btn.text()}\n{branch}')
		if True:#设置HEAD
			btn=vtree.Get_Node(gr.headIndex)
			btn.setText(f"H*{btn.text()}")
		vtree.Opt_Update()#这一步是为了更新布局

	def Git_SetPath(self,path:str):
		'''
			设置仓库路径。
			如果path为None则打开对话框进行选择
		'''
		print(path)
		if(self.Get_IsBusy()):
			self.__dlg_busy.exec()
		else:
			if(path==None):
				if(self.__dlg_pathChange.exec()):
					path=QFileDialog.getExistingDirectory()
			if(path):
				self.__dlg_fail.setText('无效的git路径')
				return self.__RunFunc(self.__LoadPath,path)
		return False
	def Git_AddCommit(self,info:str):
		'''
			添加提交。
			如果info为空则弹出文本输入框
		'''
		if(self.Get_IsBusy()):
			self.__dlg_busy.exec()
		else:
			if(not info):
				self.__dlg_textInput.Set_Hint('')
				self.__dlg_textInput.setWindowTitle('输入')
				info=self.__dlg_textInput.exec()
			self.__dlg_fail.setText('无法提交更改')
			return self.__RunFunc(self.__AddCommit,info)
		return False
	def Git_AddBranch(self,branch:str):
		'''
			添加分支。
			如果branch为空则弹出文本输入框
		'''
		if(self.Get_IsBusy()):
			self.__dlg_busy.exec()
		else:
			if(not branch):
				hintLst=['当前已有的分支：']
				hintLst.extend(f'\t-{name}' for name in self.__gr.branchIndex)
				self.__dlg_textInput.Set_Hint('\n'.join(hintLst))
				self.__dlg_textInput.setWindowTitle('创建新分支')
				branch=self.__dlg_textInput.exec()
			self.__dlg_fail.setText('当前分支已存在')
			return self.__RunFunc(self.__AddBranch,branch)
		return False
	def Git_SwitchBranch(self,branch:str):
		'''
			切换HEAD指向的分支。
			仅限和HEAD处在同一提交下的分支。
		'''
	def Git_Merge(self,*commits:str):
		'''
			合并提交。
		'''
		if(self.Get_IsBusy()):
			self.__dlg_busy.exec()
		else:
			if(len(commits)<2):
				self.__dlg_fail.setText('请选择两个以上的提交进行合并')
				self.__dlg_fail.exec()
			else:
				self.__dlg_fail.setText('分支合并失败')
				return self.__RunFunc(self.__Merge,*commits)
		return False
	def Git_Checkout(self,commit:str):
		'''
			恢复备份
		'''
		if(self.Get_IsBusy()):
			self.__dlg_busy.exec()
		else:
			self.__dlg_fail.setText('备份恢复失败')
			return self.__RunFunc(self.__Checkout,commit)
		return False
	def __RunFunc(self,func:Callable,*args):
		'''
			运行函数
		'''
		def ThRun(func:Callable,*args):
			'''
				将耗时操作传入单独线程中完成。
			'''
			sleep(0.1)
			self.__optSuccess=False
			self.__optSuccess=func(*args)
			self.__loop.quit()
		mskVisible=self.__mskBusy.isVisible()
		if(not self.Get_IsBusy()):
			self.__mskBusy.show()
			self.__th=Thread(target=ThRun,args=(func,*args))
			self.__th.start()
			self.__loop.exec()
		else:
			self.__dlg_busy.exec()
			return False
		if(self.__optSuccess):
			self.Opt_Update()
		else:
			self.__dlg_fail.exec()
		self.__mskBusy.setVisible(mskVisible)
		return self.__optSuccess
	def __LoadPath(self,path:str):
		'''
			加载路径
		'''
		self.__gr.Opt_LoadFromLocal(path)
		return True
	def __AddCommit(self,info:str):
		'''
			添加提交。
		'''
		if(info):
			rst=XJ_Git.Opt_AddCommit(info,self.__gr.path)
			self.__gr.Opt_AddCommit()
			return True
		return False
	def __AddBranch(self,branch:str):
		'''
			添加分支。
		'''
		if(branch):
			rst=XJ_Git.Opt_AddBranch(branch,self.__gr.path)
			if(rst.success):
				self.__gr.Opt_AddBranch()
				return True
		return False
	def __Merge(self,*commits:str):
		'''
			合并分支。
		'''
		return False
	def __Checkout(self,commit:str):
		'''
			恢复备份
		'''
		if(commit):
			rst=XJ_Git.Opt_Recover(commit,True,self.__gr.path)
			if(rst.success):
				self.__gr.Opt_Checkout()
				return True
		return False






