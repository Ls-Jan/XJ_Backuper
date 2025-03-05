__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJQ_StringSelector']

from PyQt5.QtWidgets import QLineEdit,QListView,QLabel,QStyle,QWidget,QVBoxLayout
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QPixmap,QHideEvent
from PyQt5.QtCore import pyqtSignal,QModelIndex,Qt,QEventLoop

from typing import List,Set
from .TextEditDelegate import TextEditDelegate

class XJQ_StringSelector(QWidget):
	'''
		字串选择器，基于QListView，
		选择的途中可新增选项。
		可调用exec以阻塞获取字串。
	'''
	createNewString=pyqtSignal(str)
	__lv:QListView
	__le:QLineEdit
	__disableSet:Set[str]
	__selectableLst:List[str]
	__appendHint:str
	__disableMark:QLabel
	__loop:QEventLoop
	__appendValid:bool
	def __init__(self,parent:QWidget=None,lv:QListView=None,*,title:str="字串选择器"):
		super().__init__(parent)
		lv=lv if lv else QListView()
		model=QStandardItemModel()
		lv.setModel(model)
		self.__lv=lv
		self.__le=None
		self.__disableSet=set()
		self.__selectableLst=[]
		self.__appendHint='<新增字串>'
		self.__disableMark=QLabel(lv)
		self.__loop=QEventLoop(self)
		self.__doubleClick=False
		self.__appendValid=True

		vbox=QVBoxLayout(self)
		vbox.addWidget(lv)
		ted=TextEditDelegate()
		lv.setItemDelegate(ted)
		# lv.setItemAlignment(Qt.AlignmentFlag.AlignCenter)#莫名其妙，用了就出事的玩意儿
		lv.doubleClicked.connect(self.__DoubleClick)
		ted.newEditor.connect(self.__InitEditor)
		ted.closeEditor.connect(self.__CloseEditor)
		ted.alignCenter=True
		lb=self.__disableMark
		lb.setPixmap(lb.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning).pixmap(24,24))
		lb.setScaledContents(True)
		self.setWindowTitle(title)
		self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint,False)#隐藏最大最小化按钮
		self.setWindowModality(Qt.WindowModality.ApplicationModal)#模态，屏蔽其他窗口
		self.Set_SelectableList([])
	def Set_AppendValid(self,flag:bool):
		'''
			是否允许显示末行添加项
		'''
		if(self.__appendValid!=flag):
			self.__appendValid=flag
		return True
	def Set_SelectableList(self,lst:List[str]):
		'''
			设置可选项
		'''
		self.__selectableLst=lst.copy()
		model:QStandardItemModel=self.__lv.model()
		model.clear()
		if(self.__appendValid):
			lst.append('')
		i=0
		for key in lst:
			item=QStandardItem(key)
			model.setItem(i,0,item)
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
			item.setEditable(False)
			i+=1
		self.__UpdateLastRow()
	def Set_SelectedRow(self,index:int):
		'''
			设置选中的行，选择失败则返回False
		'''
		model:QStandardItemModel=self.__lv.model()
		if(index<len(self.__selectableLst)-(1 if self.__appendValid else 0)):
			index=model.index(index,0)
			self.__lv.setCurrentIndex(index)
			return True
		return False
	def Set_SelectedString(self,key:str):
		'''
			设置选中的字串，选择失败则返回False
		'''
		if(key in self.__selectableLst):
			index=self.__selectableLst.index(key)
			return self.Set_SelectedRow(index)
		return False
	def Set_AdditionHint(self,hint:str):
		'''
			设置末行“新增项”的文本内容
		'''
		self.__appendHint=hint
		self.__UpdateLastRow()
	def Set_DisableMark(self,pix:QPixmap):
		'''
			设置不可用时显示的标志(尽量正方形的小图标)
		'''
		self.__disableMark.setPixmap(pix)
		self.__UpdateLastRow()
	def Set_DisableList(self,lst:List[str]):
		'''
			设置不可用的内容
		'''
		self.__disableSet=set(lst)
		self.__UpdateLastRow()
	def Get_ListView(self):
		'''
			返回列表控件
		'''
		return self.__lv
	def Get_SelectedString(self):
		'''
			返回当前选中的内容。
			未选中则返回空串
		'''
		model:QStandardItemModel=self.__lv.model()
		index=self.__lv.currentIndex()
		return model.itemFromIndex(index).text() if index.isValid() else ''
	def Opt_CancelLastString(self):
		'''
			可以通过该函数来撤回最近一次添加的字串(与信号createNewString组合使用)(仅限AppendValid为真时有效)
		'''
		model:QStandardItemModel=self.__lv.model()
		count=len(self.__selectableLst)
		if(self.__appendValid and count>1):
			self.__disableSet.discard(self.__selectableLst.pop())
			model.removeRow(count-1)
	def hideEvent(self,event:QHideEvent):
		if(self.__loop.isRunning()):
			if(not self.__doubleClick):
				self.__lv.setCurrentIndex(QModelIndex())
			self.__loop.quit()
		return super().hideEvent(event)
	def exec(self):
		'''
			以阻塞的方式获取选择的内容
		'''
		if(not self.__loop.isRunning()):
			if(self.isHidden()):
				self.__lv.setCurrentIndex(QModelIndex())
			self.__doubleClick=False
			self.show()
			self.__loop.exec()
		return self.Get_SelectedString()
	def __UpdateLastRow(self):
		'''
			更新末行的内容
		'''
		model:QStandardItemModel=self.__lv.model()
		mark=self.__disableMark
		if(self.__le):
			margin=2
			le=self.__le
			tx=le.text()
			if True:#手动居中编辑框
				w=le.width()
				W=le.parent().width()
				le.move((W-w)>>1,le.y())
			if(tx in self.__disableSet):
				sz=le.size()
				w,h=sz.width(),sz.height()-margin*2
				mark.setGeometry(w-h,margin,h,h)
				mark.show()
			else:
				mark.hide()
		elif(self.__appendValid):
			item=model.item(model.rowCount()-1,0)
			item.setText(self.__appendHint)
			item.setEditable(True)
			mark.hide()
	def __DoubleClick(self,index:QModelIndex):
		'''
			双击行为
		'''
		model:QStandardItemModel=self.__lv.model()
		if(index.row()!=len(self.__selectableLst)):#双击的不是末行
			self.__doubleClick=True
			if(self.__loop.isRunning()):
				self.close()	
	def __InitEditor(self,le:QLineEdit,index:QModelIndex):
		'''
			对弹出的文本框进行编辑
		'''
		model:QStandardItemModel=self.__lv.model()
		model.itemFromIndex(index).setText('')
		le.textChanged.connect(self.__UpdateLastRow,Qt.ConnectionType.UniqueConnection)
		self.__disableMark.setParent(le)
		self.__le=le
		self.__UpdateLastRow()
	def __CloseEditor(self):
		'''
			关闭编辑器		
		'''
		tx=self.__le.text()
		if(tx and tx not in self.__disableSet):
			self.__disableSet.add(tx)
			self.__selectableLst.append(tx)
			model:QStandardItemModel=self.__lv.model()
			count=len(self.__selectableLst)
			item=model.itemFromIndex(self.__lv.currentIndex())
			item.setEditable(False)
			if(self.__appendValid):
				item=QStandardItem('')
				item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
				model.setItem(count,0,item)#追加新行
			self.createNewString.emit(tx)
		self.__le=None
		self.__disableMark.setParent(self.__lv)
		self.__UpdateLastRow()






