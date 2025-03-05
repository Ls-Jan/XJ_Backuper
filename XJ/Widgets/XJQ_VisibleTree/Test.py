
__version__='1.0.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_VisibleTree import XJQ_VisibleTree

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		vt=XJQ_VisibleTree()
		# vt.Set_NodeSize(-1,50,50,True)
		# vt.Set_Interval(25,50)
		self.__vt=vt
	def Opt_Run(self):
		vt=self.__vt
		cv=vt.Get_Canvas()
		tr=vt.Get_Tree()
		for id in [0,1,2,3,3,5,2,5,8,7]:#指定节点下插入节点
			tr.Opt_NodeNewChild(id)
		vt.Get_Canvas().setGeometry(600,100,1000,800)
		tr.Set_NodeSize(1,100,50)
		tr.Set_NodeSize(3,200,50)
		tr.Set_NodeSize(6,150,50)
		tr.Set_NodeSize(10,200,50)
		vt.Set_LineColor((255,128,128),(0,1),(1,2),(2,3),(3,5))
		vt.Set_LineColor((128,128,255),(2,7))
		# tr.Set_Alignment(0)
		# tr.Set_Alignment(1)
		vt.Opt_Update()
		cv.Set_ViewArea()
		for id in range(tr.Get_NodeCount()):
			# print(">>>",id,tr[id])
			node=vt.Get_Node(id)
			node.setText(str(id))
			node.clicked.connect((lambda id:lambda:print("CLICK>",id))(id))

		super().Opt_Run()
		return self.__vt




