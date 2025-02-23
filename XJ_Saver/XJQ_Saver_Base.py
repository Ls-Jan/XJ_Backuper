
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_Saver_Base']

from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRect
from typing import List,Tuple

from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
from XJ.Widgets.XJQ_Mask import XJQ_Mask
from XJ.Widgets.XJQ_Resizable.Widgets.PushButton import PushButton

class XJQ_Saver_Base(QWidget):
	'''
		数据存储恢复器基类。
		图形化显示基于Qt和控件XJ.Widgets.XJQ_VisibleTree。

		派生类需重写：
			- Set_Path(self,path:str)；
			- Get_DifferentWith(self,targetID:int,sourceID:int=None)；
			- Opt_CreateBackup(self,info:str)；
			- Opt_Recover(self,id:int)；	
			- Opt_Update(self)；
		派生类可选择性重写：
			-Opt_ShowNodeOption(self,id:int,show:bool=True)：用于调整_optionBtns中按钮是否可视(或者直接修改_optionBtns)，以实现不同节点的菜单内容
		派生类可调整和增加_optionBtns中的PushButton以改变点击节点时弹出的菜单按钮(数量不建议过多)；
	'''
	_vtree:XJQ_VisibleTree#可视树
	_optionBtns:List[PushButton]#节点菜单按钮，默认注册“创建”和“恢复”，派生类可进行调整和增加
	_optionBtnInterval:Tuple[int,int]#(实际使用的是列表)。第一个是菜单按钮之间的间隔，第二个是菜单按钮与节点之间的间隔
	_optionBtnSize:Tuple[int,int]#(实际使用的是列表)。菜单按钮大小
	__nodeID:int#记录弹出菜单的节点
	__mskOption:XJQ_Mask#遮罩，弹出菜单时只显示菜单和相应节点
	def __init__(self,vtree:XJQ_VisibleTree=None):
		super().__init__()
		if(not vtree):
			vtree=XJQ_VisibleTree()
		canvas=vtree.Get_Canvas()
		mskOption=XJQ_Mask(canvas,QColor(0,0,0,128))
		btnBackup=PushButton("创建备份",canvas)
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
		btnBackup.show()
		btnRecover.clicked.connect(self.__Btn_Recover)
		btnRecover.show()

		self._vtree=vtree
		self._optionBtns=[btnBackup,btnRecover]
		self._optionBtnInterval=[50,15]
		self._optionBtnSize=[100,50]
		self.__nodeID=0
		self.__mskOption=mskOption
	def Set_Path(self,path:str):
		'''
			切换路径。
			设置成功将返回True
		'''
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
		mskOption=self.__mskOption
		btns=[btn for btn in self._optionBtns if btn.isVisible()]
		size=self._optionBtnSize
		interval=self._optionBtnInterval
		if(id>0 and vtree.Get_Tree().Get_IndexIsExist(id)):
			node=vtree.Get_Node(id)
			rect=node.lgeometry()
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
			for btn in btns:
				btn.setVisible(show)
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

