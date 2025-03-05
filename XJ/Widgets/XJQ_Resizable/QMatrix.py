
from .Matrix import Matrix
from PyQt5.QtCore import QPoint,QRect

class QMatrix(Matrix):
	'''
		仅仅是在Matrix的基础上加了个方便使用的转换函数罢了
	'''
	def Get_TransQPoint(self,*points:QPoint,invert:bool=False):
		'''
			将逻辑坐标转化为实际坐标。
			invert为真则反着来，将实际坐标转回逻辑坐标。
		'''
		points=self.Get_TransPoint(*((p.x(),p.y()) for p in points),invert=invert)
		return [QPoint(*p) for p in points]
	def Get_TransQRect(self,*rect:QRect,invert:bool=False):
		'''
			将逻辑矩形转化为实际坐标。
			invert为真则反着来，将实际坐标转回逻辑坐标。
		'''
		return [QRect(*self.Get_TransQPoint(r.topLeft(),r.bottomRight(),invert=invert)) for r in rect]
