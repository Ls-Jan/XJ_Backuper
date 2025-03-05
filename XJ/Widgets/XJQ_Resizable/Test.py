
__version__='1.0.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .Canvas import Canvas
from .Widgets.Label import Label
from .Widgets.PushButton import PushButton

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap


__all__=['Test']
class Test(XJQ_Test):
	def Opt_Run(self):
		cv=Canvas()
		lst=[]
		for i in range(5):
			for j in range(5):
				b=PushButton(str((i,j)))
				b.setGeometry(QRect(i*100,j*50,80,40))
				b.clicked.connect((lambda info:lambda :print("CLICK!!!",info))((i,j)))
				b.setParent(cv)
				b.show()
				lst.append(b)
		lb=Label('ABC')
		lb.setPixmap(QPixmap(self.Get_RealPath('../Icons/回收站.ico')).scaled(96,96))
		lb.setGeometry(QRect(100,-100,100,100))
		lb.setParent(cv)
		lb.show()
		cv.resize(1200,800)
		cv.Set_ScaleRate(2.5)
		cv.Opt_MoveCenterTo(lst[len(lst)>>1])
		cv.show()
		super().Opt_Run()







