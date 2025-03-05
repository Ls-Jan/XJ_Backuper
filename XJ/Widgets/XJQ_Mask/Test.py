
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_Mask import XJQ_Mask
from ..XJQ_LoadingAnimation import XJQ_LoadingAnimation

from PyQt5.QtWidgets import QListView,QPushButton,QVBoxLayout,QWidget,QLabel
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QColor

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		wid=QWidget()
		lv=QListView()
		btn=QPushButton('切换遮罩')
		lb=QLabel("Test",lv)
		vbox=QVBoxLayout(wid)
		vbox.addWidget(lv)
		vbox.addWidget(btn)

		lv.setModel(QStringListModel([str(i) for i in range(10)]))
		btn.clicked.connect(self.__SwitchMask)
		lb.setGeometry(200,200,50,50)
		lb.setStyleSheet('background:#BBFFFF')

		la=XJQ_LoadingAnimation()
		mk=XJQ_Mask(lv,centerWidget=la)
		mk.clicked.connect(lambda:print('遮罩被点击'))
		mk.Set_MaskColor(QColor(0,0,0,192))
		mk.Set_UncoverWidgets(lb)
		mk.hide()
		# mk.show()

		self.__wid=wid
		self.__mk=mk
	def __SwitchMask(self):
		self.__mk.setVisible(not self.__mk.isVisible())
	def Opt_Run(self):
		self.__wid.resize(600,400)
		self.__wid.show()
		super().Opt_Run()
		return self.__wid



