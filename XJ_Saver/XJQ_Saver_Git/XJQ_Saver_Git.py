
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['XJQ_Saver_Git']

from ..XJQ_Saver_Base import XJQ_Saver_Base
from ..XJ_GitRecord import XJ_GitRecord
from .XJQ_GitOperator import XJQ_GitOperator
from ._Record import _Record
from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
from XJ.Widgets.XJQ_Resizable.Widgets.PushButton import PushButton

from PyQt5.QtWidgets import QMessageBox
import os

class XJQ_Saver_Git(XJQ_Saver_Base):
	'''
		基于Git的数据存储恢复器
	'''
	__rec:_Record
	__dlg_pathChange:QMessageBox
	def __init__(self,vtree:XJQ_VisibleTree=None):
		super().__init__(vtree)
		self.__rec=_Record(self,XJQ_GitOperator(XJ_GitRecord(self._vtree.Get_Tree())))
		self.__dlg_pathChange=QMessageBox(QMessageBox.Icon.Question,"切换路径","是否切换仓库路径？")
		self._btn_branchSelect=PushButton('调整HEAD',self._vtree.Get_Canvas())

		dlg=self.__dlg_pathChange
		dlg.addButton("取消",QMessageBox.ButtonRole.NoRole)
		dlg.addButton("确认",QMessageBox.ButtonRole.YesRole)
		btn=self._btn_branchSelect
		btn.hide()
		btn.clicked.connect(lambda:self.__rec.op.Git_SwitchBranch(None))
		self._optionBtns.insert(0,btn)
		vtree=self._vtree
		vtree.Get_Node(0).setText('选择路径')
		vtree.Get_Tree().Set_NodeSize(0,400,50)
		# vtree.Get_Tree().Set_NodeSize(-1,100,50)
		vtree.Get_ClickedSignal().connect(lambda index:self.Set_Path(None) if index==0 else None)
		self.Opt_Update()
	def Set_RecoverMode(self,strict:bool=None,moveHead:bool=None):
		'''
			设置恢复模式。
			- strict[严格模式](默认启用)：会删除多余(未跟踪)文件以保证恢复结果与备份完全一致。
			- moveHead[移动HEAD](默认启用)：恢复备份并移动当前位置。
		'''
		return self.__rec.op.Set_RecoverMode(strict,moveHead)
	def Set_Path(self,path):
		with self.__rec:
			return self.__rec.op.Git_LoadPath(path)
	def Get_DifferentWith(self,targetID:int,sourceID:int=None):
		cmd='git status -s'
	def Opt_CreateBackup(self,info:str):
		with self.__rec:
			return self.__rec.op.Git_AddCommit(info)
	def Opt_Recover(self,id:int):
		with self.__rec:
			op=self.__rec.op
			return op.Git_Recover(op.gr.commitID[id])
	def Opt_Update(self):
		gr=self.__rec.op.gr
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
			btn.setText(f'->{merge}')
		for lid,rid in gr.coincident.items():#设置逻辑点
			btn=vtree.Get_Node(lid)
			btn.setText(f'-{rid}-')
			# btn.setStyleSheet('background:#44444444')
		for branch,id in gr.branchIndex.items():#设置分支
			btn=vtree.Get_Node(id)
			vtree.Get_Tree().Set_NodeSize(id,200,50)
			btn.setText(f'{btn.text()}\n{branch}')
		if True:#设置HEAD
			btn=vtree.Get_Node(gr.headIndex)
			btn.setText(f"H*{btn.text()}")
		vtree.Opt_Update()#这一步是为了更新布局
	def UI_ShowNodeOption(self,id:int,show:bool=True):
		gr=self.__rec.op.gr
		isCurr=id==gr.headIndex
		self._btnBackup.setProperty('hide',not isCurr)#仅允许当前节点存在“创建备份”的行为
		self._btn_branchSelect.setProperty('hide',not isCurr)#仅允许当前节点存在“分支切换”操作
		super().UI_ShowNodeOption(id,show)











