


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
from XJ.Widgets.XJQ_Mask import XJQ_Mask
from XJ.Widgets.XJQ_Resizable.Widgets.PushButton import PushButton

class XJQ_Saver_Base(QWidget):
	'''
		数据存储恢复器基类。
		图形化显示基于Qt和控件XJ.Widgets.XJQ_VisibleTree
	'''
	def __init__(self):
		super().__init__()
		vtree=XJQ_VisibleTree()
		canvas=vtree.Get_Canvas()
		mskOption=XJQ_Mask(canvas,QColor(0,0,0,128))
		btnBackup=PushButton("创建",canvas)
		btnRecover=PushButton("恢复",canvas)

		vbox=QVBoxLayout(self)
		vbox.addWidget(vtree.Get_Canvas())
		vbox.setContentsMargins(0,0,0,0)
		self.resize(1200,800)
		canvas.Set_WidFixed(mskOption,True)
		mskOption.clicked.connect(self.__Msk_Hide)
		mskOption.move(0,0)
		mskOption.hide()
		vtree.Get_ClickedSignal().connect(self.__Btn_Node)
		btnBackup.clicked.connect(self.__Btn_Backup)
		btnRecover.clicked.connect(self.__Btn_Recover)

		self._vtree=vtree
		self._path='.'
		self.__nodeID=0
		self.__mskOption=mskOption
		self.__btnBackup=btnBackup
		self.__btnRecover=btnRecover
	def Set_Path(self,path:str):
		'''
			切换路径。
			设置成功将返回True
		'''
		self._path=path
		return True
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
	def Opt_ShowNodeOption(self,id:int,show:bool=True):
		'''
			显示/隐藏节点菜单
		'''
		vtree=self._vtree
		btnBackup=self.__btnBackup
		btnRecover=self.__btnRecover
		mskOption=self.__mskOption
		if(id>0 and vtree.Get_Tree().Get_IndexIsExist(id)):
			node=vtree.Get_Node(id)
			rect=node.lgeometry()
			interval=(50,15)
			size=(100,50)
			btns=[btnBackup,btnRecover]
			if(show):#调整位置
				self.__nodeID=id
				T=rect.bottom()+interval[1]
				L=rect.center().x()-(size[0]*len(btns)+interval[0])/2
				mskOption.raise_()
				for btn in btns:
					btn.setLGeometry(QRect(L,T,size[0],size[1]))
					btn.raise_()
					L+=size[0]+interval[0]
				node.raise_()
				self._vtree.Opt_Update()
		if(not show or id>0):
			btnBackup.setVisible(show)
			btnRecover.setVisible(show)
			mskOption.setVisible(show)
	def __Btn_Recover(self):
		self.Opt_Recover(self.__nodeID)
		self.__Msk_Hide()
	def __Btn_Backup(self):
		self.Opt_CreateBackup()
		self.__Msk_Hide()
	def __Btn_Node(self,id:int):
		self.Opt_ShowNodeOption(id)
	def __Msk_Hide(self):
		self.Opt_ShowNodeOption(0,False)

