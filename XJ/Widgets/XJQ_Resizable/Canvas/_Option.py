

from typing import Union
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint


class _Option:#功能
	scalable:bool=True#可缩放
	draggable:bool=True#可拖拽/移动
	scaleCenter:Union[QPoint,QWidget]=None#缩放中心，不存在则以指定位置(默认鼠标)为中心进行缩放


