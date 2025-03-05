
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_TextInputDialog import XJQ_TextInputDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		btn=QPushButton("点击弹出窗口")
		ti=XJQ_TextInputDialog(parent=btn)
		ti.Set_Text("ABC")
		ti.textSent.connect(lambda tx:print(tx))
		ti.resize(300,200)
		btn.resize(700,400)
		btn.clicked.connect(lambda:print(">",ti.exec()))#这个是不通过信号槽并立即返回结果
		# btn.clicked.connect(lambda:ti.show())
		ti.Set_DialogMode(False)
		ti.Set_DialogMode(True)
		ti.Set_Hint('<br>'.join([f'<font color={QColor(31*i,0,255-31*i).name()} size=5>HINT</font>' for i in range(0,9)]))
		self.__ti=ti
		self.__btn=btn
	def Opt_Run(self):
		self.__btn.show()
		self.__btn.click()
		super().Opt_Run()

		return self.__ti











