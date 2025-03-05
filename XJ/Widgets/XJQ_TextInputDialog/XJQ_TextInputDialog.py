__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJQ_TextInputDialog']

from PyQt5.QtWidgets import QWidget,QTextEdit,QPushButton,QGridLayout,QScrollArea,QLabel,QFrame
from PyQt5.QtGui import QShowEvent,QHideEvent
from PyQt5.QtCore import Qt,pyqtSignal,QObject,QEvent,QEventLoop


class XJQ_TextInputDialog(QWidget):
	'''
		文本输入框，带有确认按钮。
		按下Alt+Enter可执行“确认”操作。
		新增阻塞操作exec。
	'''
	textSent=pyqtSignal(str)#发送文本
	def __init__(self,parent:QWidget=None,*,title:str='文本输入',tx:QTextEdit=None,btnOK:QPushButton=None):
		'''
			可指定具体的文本框控件tx和确认按钮控件btnOK
		'''
		super().__init__(parent)
		if(tx==None):
			tx=QTextEdit(self)
		if(btnOK==None):
			btnOK=QPushButton(self)
			btnOK.setText('确认')
		sa=QScrollArea()
		sa.setFrameStyle(QFrame.Shape.NoFrame)
		self.__tx=tx
		self.__ok=btnOK
		self.__dialogMode=True
		self.__txData=""
		self.__hint=sa#不使用QTextEdit是因为显示的效果不佳
		self.__closeSend=False#弹窗模式下用该变量判断窗口关闭时是否需要发送文本，非弹窗模式下该值总为False
		self.__loop=QEventLoop(self)

		grid=QGridLayout(self)
		grid.addWidget(sa,0,0,1,2)
		grid.addWidget(tx,1,0,1,2)
		grid.addWidget(btnOK,2,1)
		tx.setAcceptRichText(False)#禁止富文本
		tx.setParent(self)
		btnOK.setParent(self)
		btnOK.clicked.connect(self.__SendText)
		tx.installEventFilter(self)#要拦截Alt+Enter按键
		
		sa.setWidget(QLabel())
		sa.hide()
		sa.setWidgetResizable(True)
		self.setWindowTitle(title)
		self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint,False)#隐藏最大最小化按钮
		self.setWindowModality(Qt.WindowModality.ApplicationModal)#模态，屏蔽其他窗口
		self.Set_DialogMode(True)
	def Set_DialogMode(self,flag:bool):
		'''
			是否设置成弹窗模式。
			弹窗模式下：
				- 发送文本后自动关闭窗口；
				- 直接关闭窗口(不发送文本)会清空文本框；
			非弹窗模式与上面相反。
		'''
		self.__dialogMode=flag
		if(flag):
			self.setWindowFlag(Qt.WindowType.Dialog)#弹窗
		else:
			self.setWindowFlag(Qt.WindowType.Dialog,False)#取消弹窗弹窗
		self.__closeSend=flag
	def Set_Hint(self,tx:str):
		'''
			设置提示内容，
			为空则隐藏
		'''
		hint:QLabel=self.__hint.widget()
		hint.setText(tx)
		hint.setVisible(bool(tx))
		self.__hint.setVisible(bool(tx))
	def Set_Text(self,tx:str):
		'''
			设置文本框内容
		'''
		self.__tx.clear()
		self.__tx.append(tx)#使用该操作会顺带移动光标到文末，而setText仅会让光标停留原处
	def Get_TextEdit(self):
		'''
			获取文本输入框控件(QTextEdit)以进行更加细化的操作
		'''
		return self.__tx
	def Get_OKButton(self):
		'''
			获取确认按钮(QPushButton)以进行更为细化的操作
		'''
		return self.__ok
	def Get_HintWidget(self):
		'''
			获取提示内容控件(QLabel)以进行进一步的细化设置
		'''
		hint:QLabel=self.__hint.widget()
		return hint
	def exec(self):
		'''
			以阻塞的方式获取文本内容，不发送textSent信号
		'''
		if(not self.__loop.isRunning()):
			self.show()
			self.__loop.exec()
		return self.__txData
	def __SendText(self):
		'''
			发送当前文本内容，信号为textSent。
			如果使用了消息循环则不发送信号。
		'''
		self.__txData=self.__tx.toPlainText()
		if(self.__loop.isRunning()):
			self.__loop.quit()
		else:
			self.textSent.emit(self.__txData)
		if(self.__dialogMode):
			self.__closeSend=False
			self.close()
	def showEvent(self,event:QShowEvent):
		if(self.__dialogMode):
			self.__tx.clear()
		self.__closeSend=self.__dialogMode
		return super().showEvent(event)
	def hideEvent(self,event:QHideEvent):
		if(self.__closeSend):
			self.__SendText()
		return super().hideEvent(event)
	def eventFilter(self,obj:QObject,event:QEvent):
		if(event.type()==event.Type.KeyPress):#按键事件
			mod=event.modifiers()
			if(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter):#按下回车键
				if(mod&Qt.KeyboardModifier.AltModifier):#按着ALT键
					self.__SendText()
					return True#已将该事件完成(拦截)，不向下传递
		return False#不做处理，交由下级完成



