__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ..XJ_MouseStatus import XJ_MouseStatus

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

__all__=['Test']

class TestWidget(QLabel):
	__mouseStatus=None
	def __init__(self,*arg):
		super().__init__(*arg)
		self.setText('请尝试点击、拖拽、长按窗体查看效果')
		self.setStyleSheet('background:#222222;color:#AAAAAA')
		self.setAlignment(Qt.AlignCenter)
		ms=XJ_MouseStatus()
		ms.longClick.connect(lambda:print("<LongClick!>"))
		self.__mouseStatus=ms
		self.resize(400,200)
	def __EasyPrint(self):
		press={
			QMouseEvent.MouseButtonRelease:"Release",
			QMouseEvent.MouseButtonPress:"Press",
			QMouseEvent.MouseButtonDblClick:"DblClick",}
		button={
			Qt.LeftButton:'Left',
			Qt.MidButton:'Middle',
			Qt.RightButton:'Right',}
		tPoint=lambda point:(point.x(),point.y())
		tBtn=lambda btn:[button[key] for key in button if key&btn]
		tBtnStatus=lambda status:(tBtn(status[0]),press[status[1]])

		ms=self.__mouseStatus
		pos=tPoint(self.mapFromGlobal(ms.Get_Position()))
		moveDelta=tPoint(ms.Get_MoveDelta())
		btnStatus=tBtnStatus(ms.Get_PressButtonStatus())
		print(f'pos{pos},\tdelta{moveDelta},\t{btnStatus[0]}-{btnStatus[1]}')
		if(btnStatus[1]=='Release'):
			print()
	def mousePressEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()
	def mouseMoveEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()
	def mouseReleaseEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()


class Test(XJQ_Test):
	def __init__(self) -> None:
		super().__init__()
		self.__wid=TestWidget()
	def Opt_Run(self):
		self.__wid.resize(800,400)
		self.__wid.show()
		super().Opt_Run()
		return self.__wid


