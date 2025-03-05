
__version__='1.0.3'
__author__='Ls_Jan'

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint,Qt,QObject
from PyQt5.QtGui import QMouseEvent

__all__=['XJ_MouseStatus']

class XJ_MouseStatus(QObject):#鼠标状态记录
	'''
		鼠标状态记录，仅用于Qt场合(当然可以进一步提纯/抽象成通用算法使其脱离Qt，只不过懒得弄)，
		该类不单独使用，只处理单键(多键行为请在外部代码控制)
		用于简化mousePressEvent、mouseMoveEvent和mouseReleaseEvent的部分鼠标控制逻辑，

		包括鼠标长按(防抖)、鼠标双击、鼠标拖拽移动量(相对和绝对)、鼠标位置、鼠标拖拽时的移动判断
		可设置长按间隔、双击间隔、防抖距离(鼠标按下时移动量不超过该值时鼠标被视为未移动状态)
	'''
	longClick=pyqtSignal()#鼠标原地不动长按时触发

	__antiJitter=5#防抖，当鼠标点击位置与鼠标当前位置的曼哈顿距离不超过该值时仍将鼠标视为不动状态
	__doubleClickInterval=500#双击间隔(ms)
	__longPressInterval=500#长按间隔(ms)
	__record={
		'lastPress':None,#上一次按下时的信息
		'lastMouse':None,#上一次的鼠标信息
		'currMouse':None,#当前鼠标信息
		}
	__pressStatus={
		'Release':QMouseEvent.MouseButtonRelease,
		'SPress':QMouseEvent.MouseButtonPress,
		'DPress':QMouseEvent.MouseButtonDblClick,
	}
	__move=False#用于判断是否长按
	__triggerMove=False#用于判断Get_HasMoved(True)是否已经返回过一次True
	__timerID=0#鼠标按下时对应的定时器
	class __Data:
		pos=None#鼠标位置
		btn=None#鼠标按键(左中右)
		pressStatus=None#鼠标当前按下状态(单双击/抬起)
		timeStamp=None#鼠标事件时间刻
		def __init__(self,event):
			self.pos=event.globalPos()
			self.btn=event.button()
			self.pressStatus=event.type()
			# self.pressStatus=event.MouseButtonRelease
			self.timeStamp=event.timestamp()

	def __init__(self,parent:QObject=None):
		super().__init__(parent)
		record=self.__record.copy()
		fakeEvent=QMouseEvent(QMouseEvent.MouseButtonRelease,QPoint(0,0),Qt.NoButton,Qt.NoButton,Qt.NoModifier)
		data=self.__Data(fakeEvent)
		data.timeStamp-=self.__doubleClickInterval#小防，避免开局单击时触发双击行为
		record['lastMouse']=data
		record['currMouse']=data
		record['lastPress']=data
		self.__record=record
	def timerEvent(self,event):
		record=self.__record
		tId=event.timerId()
		cId=self.__timerID
		self.killTimer(event.timerId())
		if(cId==tId):#当前定时器
			if(not self.__move and record['currMouse'].pressStatus!=self.__pressStatus['Release']):#未发生移动，未抬起鼠标，触发长按信号
				self.longClick.emit()

	def Get_Position(self):
		'''
			返回鼠标坐标。是屏幕坐标(global)，需要使用QWidget.mapFromGlobal(QPoint)自行转换为控件相对坐标
		'''
		return self.__record['currMouse'].pos
	def Get_PressButtonStatus(self):
		'''
			返回两份数据：
				- 当前鼠标的键(左中右)：形如Qt.MouseButton.XXXButton的枚举值；
				- 按下状态(单击/双击/抬起)：形如QMouseEvent.Type.MouseButtonXXX的枚举值；
		'''
		return self.__record['currMouse'].btn,self.__record['currMouse'].pressStatus
	def Get_MoveDelta(self,total:bool=True,strict:bool=True):
		'''
			返回鼠标移动量(仅鼠标按下时有效)，为QPoint对象。
			total为真时计算自按下鼠标起的鼠标移动量，否则计算与上一次鼠标事件间的鼠标移动量；
			strict为真时仅在触发“移动”时计算移动量，即微小的偏移会被视为“抖动”而将偏移量视为0；
		'''
		record=self.__record
		data_curr=record['currMouse']
		if(data_curr.pressStatus!=self.__pressStatus['Release']):#说明鼠标按下
			if(not strict or self.__move):#严格模式下，仅判定发生移动时计算移动量
				p1=record['currMouse'].pos
				if(total):
					p2=record['lastPress'].pos
				else:
					p2=record['lastMouse'].pos
				return QPoint(p1.x()-p2.x(),p1.y()-p2.y())
		return QPoint(0,0)
	def Get_HasMoved(self,trigger:bool=False):
		'''
			判断是否发生移动(毕竟用Get_MoveDelta来判断移动的发生是有点麻烦，还不如多一个函数)。
			如果trigger为真，则移动后初次调用时会返回真，但后续的调用均返回假，使用该参数可有效避免重复返回True。
		'''
		if(not trigger):
			return self.__move
		if(not self.__triggerMove and self.__move):
			self.__triggerMove=True
			return True
		return False
	def Set_DoubleClickInterval(self,interval:int):
		'''
			设置双击时间间隔(ms)
		'''
		self.__doubleClickInterval=interval
	def Set_LongPressInterval(self,interval:int):
		'''
			设置长按时间间隔(ms)
		'''
		self.__longPressInterval=interval
	def Set_AntiJitter(self,val:int):
		'''
			设置防抖值
		'''
		self.__antiJitter=val if val>0 else 0
	def Opt_Update(self,event:QMouseEvent):
		'''
			更新状态，传入鼠标事件
		'''
		record=self.__record
		data_curr=self.__Data(event)
		if(event.type()==self.__pressStatus['SPress'] or event.type()==self.__pressStatus['DPress']):#单/双击
			self.__move=False
			self.__triggerMove=False
			data_old=record['lastPress']
			data_curr.pressStatus=self.__pressStatus['SPress']
			if(data_old.btn==data_curr.btn):#同键位按下
				if(data_curr.timeStamp-data_old.timeStamp<self.__doubleClickInterval):#在时间间隔内
					if(data_old.pressStatus!=self.__pressStatus['DPress']):#没有双击过
						data_curr.pressStatus=self.__pressStatus['DPress']#双击
			record['lastPress']=data_curr
			record['lastMouse']=data_curr
			record['currMouse']=data_curr
			self.__timerID=self.startTimer(self.__longPressInterval)
		else:#移动/抬起
			data_curr.btn=event.buttons()
			data_curr.pressStatus=record['lastMouse'].pressStatus
			if(event.type()==self.__pressStatus['Release']):#抬起
				if(data_curr.btn==Qt.NoButton):#确保无按键按下时设置为Release
					data_curr.pressStatus=self.__pressStatus['Release']
					data_curr.btn=event.button()
			if(data_curr.pressStatus!=self.__pressStatus['Release'] and not self.__move):#判断有无发生拖拽
				delta=self.Get_MoveDelta(strict=False)
				if(abs(delta.x())+abs(delta.y())>self.__antiJitter):
					self.__move=True
					record['currMouse'].pos=record['lastPress'].pos
			record['lastMouse']=record['currMouse']
			record['currMouse']=data_curr
	def Opt_Release(self):
		'''
			特殊行为(纯纯打补丁)，选择性地将鼠标释放。
			因为一些特殊场合(例如内部拖拽)会导致控件无法进入到mouseReleaseEvent中，导致无法顺利调用Opt_Update更新鼠标状态
		'''
		self.__record['currMouse'].pressStatus=self.__pressStatus['Release']
		self.__record['lastMouse']=self.__record['currMouse']

