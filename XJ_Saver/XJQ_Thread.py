
from PyQt5.QtWidgets import QWidget
from threading import Thread

from XJ.Widgets.XJQ_LoadingAnimation import XJQ_LoadingAnimation
from XJ.Widgets.XJQ_Mask import XJQ_Mask

class XJQ_Thread:
	'''
		用于处理耗时操作。
		需继承使用。
		会有个加载遮罩阻挡目标控件。
		派生类需重写：
			- _Task(self)
	'''
	__th:Thread
	__msk:XJQ_Mask
	def __init__(self,target:QWidget):
		self.__th=Thread()
		self.__msk=XJQ_Mask(target)
		if(la==None):
			la=XJQ_LoadingAnimation()
		self.__msk.Set_CenterWidget(la)
	def Get_Mask(self):
		'''
			返回遮罩控件
		'''
		return self.__msk
	def Opt_Run(self):
		'''
			开始执行。
			如果上次的操作还未完成则执行失败。
		'''
		if(not self.__th.is_alive()):
			self.__th=Thread(target=self.__Th_Run)
			return True
		return False
	def __Th_Run(self):
		'''
			给线程使用
		'''
		msk=self.__msk
		msk.show()
		self._Task()
		msk.hide()
	def _Task(self):
		'''
			派生类需重写的函数
		'''
		pass

