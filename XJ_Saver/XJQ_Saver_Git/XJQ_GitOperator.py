
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['XJQ_GitOperator']

from ..XJ_Git import XJ_Git
from ..XJ_GitRecord import XJ_GitRecord
from XJ.Widgets.XJQ_TextInputDialog import XJQ_TextInputDialog
from XJ.Widgets.XJQ_StringSelector import XJQ_StringSelector

from PyQt5.QtWidgets import QWidget,QMessageBox,QFileDialog,QCheckBox,QGridLayout,QSpacerItem,QSizePolicy
from PyQt5.QtCore import QEventLoop
from typing import Callable
from threading import Thread
from time import sleep


class XJQ_GitOperator:
	'''
		对Git相关操作进行简单的封装，以避免操作阻塞UI。
	'''
	success:bool
	gr:XJ_GitRecord
	dlg_busy:QMessageBox
	dlg_fail:QMessageBox
	dlg_recover:QMessageBox
	dlg_textInput:XJQ_TextInputDialog
	dlg_branchSelect:XJQ_StringSelector
	__th:Thread
	__loop:QEventLoop
	__cb_recoverStrict:QCheckBox
	__cb_recoverMoveHead:QCheckBox
	def __init__(self,gr:XJ_GitRecord):
		self.success=False
		self.gr=gr
		self.dlg_busy=QMessageBox(QMessageBox.Icon.NoIcon,"失败","当前操作正忙")
		self.dlg_fail=QMessageBox(QMessageBox.Icon.NoIcon,"失败","操作失败")
		self.dlg_textInput=XJQ_TextInputDialog()
		self.dlg_branchSelect=XJQ_StringSelector(title="选择分支")
		self.dlg_recover=QMessageBox(QMessageBox.Icon.Question,"设置恢复模式","")
		self.__th=Thread()
		self.__loop=QEventLoop()
		self.__cb_recoverStrict=QCheckBox('严格恢复')
		self.__cb_recoverMoveHead=QCheckBox('位置同步')

		grid=QGridLayout()
		grid.addItem(QSpacerItem(20,0,QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred),1,0)
		grid.addWidget(self.__cb_recoverStrict,1,1)
		grid.addWidget(self.__cb_recoverMoveHead,2,1)
		dlg=self.dlg_recover
		dlg.layout().addLayout(grid,0,1)
		# box.layout().addLayout(grid,1,1)
		dlg.addButton("取消",QMessageBox.ButtonRole.NoRole)
		dlg.addButton("确认",QMessageBox.ButtonRole.YesRole)
		dlg=self.dlg_textInput
		dlg.Set_DialogMode(True)
		dlg=self.dlg_branchSelect
		dlg.Set_AdditionHint("<创建分支>")
		dlg.createNewString.connect(lambda branch:self.Git_AddBranch(branch))
		dlg.Set_AppendValid(True)
	def __CheckBranchName(self,tx:str=None):
		'''
			检查tx是否为有效分支名，
			tx为None则使用dlg_textInput中的文本内容。
			考虑到tx有可能存在使用换行以及缩进，返回值使用的是str代表分支名，为空则说明tx对应分支名无效。
			会改动dlg_textInput的hint内容。
		'''
		ti:XJQ_TextInputDialog=self.dlg_textInput
		if(tx==None):
			tx=ti.Get_TextEdit().toPlainText()
		if True:#处理tx中的换行以及空白符
			tx=tx
		if(tx in self.gr.branchIndex):
			ti.Set_Hint(f'分支名 {tx} 已存在')
		elif(tx):
			ti.Set_Hint(f'分支名有效')
			return tx
		else:
			ti.Set_Hint(f'请输入分支名')
		return ''
	def __exec(self,func:Callable,*args):
		'''
			阻塞执行非UI的func函数(同时不影响UI)，并返回执行结果(True/False)
			其中func以Git开头，例如go.exec(go.Git_AddCommit,"Msg")。
			执行完毕后会将结果赋值给go.success。
			failText用于设置执行失败时的弹窗内容。
		'''
		def ThRun(func:Callable,*args):
			'''
				将耗时操作传入单独线程中完成。
			'''
			sleep(0.1)
			self.success=func(*args)
			self.__loop.quit()
		self.success=False
		if(not self.busy(True)):
			self.__th=Thread(target=ThRun,args=(func,*args))
			self.__th.start()
			self.__loop.exec()
		if(not self.success):
			self.dlg_fail.exec()
		return self.success
	def busy(self,dialog:bool=False):
		'''
			获取是否正忙。
			指定dialog=True时如果正忙则会弹出一个弹窗提示
		'''
		busy=self.__th.is_alive()
		if(busy and dialog):
			self.dlg_busy.exec()
		return busy

	def Set_RecoverMode(self,strict:bool=None,moveHead:bool=None,dialog:bool=False):
		'''
			设置恢复模式。
			- strict[严格模式](默认启用)：会删除多余(未跟踪)文件以保证恢复结果与备份完全一致。
			- moveHead[移动HEAD](默认启用)：恢复备份并移动当前位置。
			dialog为真则弹出弹窗进行设置，此时如果取消弹窗则会返回False，其余情况(包括dialog=False不使用弹窗)均返回True。
		'''
		cbStrict:QCheckBox=self.__cb_recoverStrict
		cbMoveHead:QCheckBox=self.__cb_recoverMoveHead
		if(strict==None):
			strict=cbStrict.isChecked()
		if(moveHead==None):
			moveHead=cbMoveHead.isChecked()
		if(dialog):
			dlg:QMessageBox=self.dlg_recover
			apply=dlg.exec()
			if(apply):
				return True
		cbStrict.setChecked(strict)
		cbMoveHead.setChecked(moveHead)
		return not dialog
	def Git_LoadPath(self,path:str):
		'''
			加载路径。
			path=None则弹出对话框进行选择。
		'''
		if(not self.busy(True)):
			if(path==None):
				path=QFileDialog.getExistingDirectory()
			if(path):
				self.dlg_fail.setText('无效的git路径')
				return self.__exec(lambda:self.gr.Opt_LoadFromLocal(path))
		return False
	def Git_AddCommit(self,info:str):
		'''
			添加提交。
			info=None则弹出文本输入框。
		'''
		if(not self.busy(True)):
			if(info==None):
				dlg:XJQ_TextInputDialog=self.dlg_textInput
				dlg.setWindowTitle('创建提交')
				dlg.Set_Hint('输入提交信息')
				info=dlg.exec()
			if(info):
				self.dlg_fail.setText('提交失败')
				return self.__exec(lambda:self.gr.Opt_AddCommit() if XJ_Git.Opt_AddCommit(info,self.gr.path).success else None)
		return False
	def Git_AddBranch(self,branch:str):
		'''
			添加分支。
			如果branch=None则弹出分支输入框
		'''
		if(not self.busy(True)):
			if(branch==None):
				dlg:XJQ_TextInputDialog=self.dlg_textInput
				dlg.setWindowTitle('新建分支')
				self.__CheckBranchName('')
				dlg.Get_TextEdit().textChanged.connect(self.__CheckBranchName)
				branch=dlg.exec()
				dlg.Get_TextEdit().textChanged.disconnect(self.__CheckBranchName)
			branch=self.__CheckBranchName(branch)
			if(branch):
				self.dlg_fail.setText('分支创建失败')
				return self.__exec(lambda:self.gr.Opt_AddBranch() if XJ_Git.Opt_AddBranch(branch,self.gr.path).success else None)
		return False
	def Git_SwitchBranch(self,branch:str):
		'''
			切换分支，
			只允许同个<commit>内的分支切换。
			如果branch=None则弹出分支选择框
		'''
		if(not self.busy(True)):
			if(branch==None):
				dlg:XJQ_StringSelector=self.dlg_branchSelect
				dlg.Set_DisableList(self.gr.branchIndex.keys())
				dlg.Set_SelectableList(['<游离>']+[key for key,index in self.gr.branchIndex.items() if index==self.gr.headIndex])
				if(not dlg.Set_SelectedString(self.gr.headBranch)):
					dlg.Set_SelectedRow(0)
				branch=dlg.exec()
			if(branch):
				self.dlg_fail.setText('分支切换失败')
				return self.__exec(lambda:self.gr.Opt_Checkout() if XJ_Git.Opt_ChangeBranch(branch,self.gr.path).success else None)
		return False
	def Git_Merge(self,*commits:str):
		'''
			合并分支。
		'''
		return False
	def Git_Recover(self,commit:str,dialog:bool=True):
		'''
			恢复备份。
			如果dialog为真则弹出确认框以避免误操作
		'''
		if(not self.busy(True)):
			dlg:QMessageBox=self.dlg_recover
			title=dlg.windowTitle()
			dlg.setWindowTitle('恢复备份')
			if(self.Set_RecoverMode(dialog=True)):#点击确认
				cbStrict:QCheckBox=self.__cb_recoverStrict
				cbMoveHead:QCheckBox=self.__cb_recoverMoveHead
				strict=cbStrict.isChecked()
				moveHead=cbMoveHead.isChecked()
				if(commit):
					self.dlg_fail.setText('恢复失败')
					return self.__exec(lambda:self.gr.Opt_Checkout() if XJ_Git.Opt_Recover(commit,moveHead,strict,self.gr.path).success else None)
			dlg.setWindowTitle(title)
		return False




