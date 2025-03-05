
import numpy as np
from typing import Tuple

class Matrix:
	'''
		转换矩阵，底层使用np.ndarray。
		QTransform也能达到同样的效果，但觉得没这个必要
	'''
	__matrix:np.ndarray#3*3转换矩阵(np.array)，逻辑坐标→显示坐标
	__iMatrix:np.ndarray#__matrix的逆矩阵
	__changed:bool#为了一碟醋包的饺子。判断逆矩阵是否需要更新
	__scaleMin:float=0.5#缩放最小值
	__scaleMax:float=10#缩放最大值
	def __init__(self):
		self.__matrix=np.array([[1,0,0],[0,1,0],[0,0,1]])
	def Get_TransPoint(self,*point:Tuple[float,float],invert:bool=False):
		'''
			将逻辑坐标转化为实际坐标。
			如果invert为真则将实际坐标转回逻辑坐标。
		'''
		matrix=self.__matrix 
		if(invert):
			if(self.__changed):
				self.__iMatrix=np.linalg.inv(matrix)
				self.__changed=False
			matrix=self.__iMatrix
		mat=np.array([[p[0],p[1],1] for p in point])
		mat=mat.dot(matrix)
		return [tuple(row[:2]) for row in mat]
	def Get_ScaleRate(self):
		return self.__matrix[0][0]
	def Set_ScaleLimit(self,scaleMin:float=None,scaleMax:float=None):
		'''
			设置缩放极限
		'''
		if(scaleMin!=None):
			self.__scaleMax=scaleMin
		if(scaleMax!=None):
			self.__scaleMax=scaleMax
	def Opt_Move(self,dx:float,dy:float):
		'''
			单纯的画布移动
		'''
		self.__matrix[2]+=[dx,dy,0]
		self.__changed=True
	def Opt_Scale(self,cx:float,cy:float,rate:float,setScale:bool=False):
		'''
			在指定中心进行增量缩放。
			如果setScale为真则为设置缩放。
		'''
		currRate=self.__matrix[0][0]
		if(not setScale):
			rate=rate*currRate
		rate=max(self.__scaleMin,rate)
		rate=min(self.__scaleMax,rate)
		rate/=currRate
		self.__matrix=self.__matrix.dot(np.array([
				[rate,0,0],
				[0,rate,0],
				[cx*(1-rate),cy*(1-rate),1]
			]))
		self.__changed=True
		
