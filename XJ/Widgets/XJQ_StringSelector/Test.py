
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_StringSelector import XJQ_StringSelector

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		ss=XJQ_StringSelector()
		self.__ss=ss
		lst=['1','2','3']
		ss.Set_DisableList([str(i) for i in range(10)])
		ss.Set_SelectableList(lst)
		ss.createNewString.connect(lambda key:None if key.isdigit() else ss.Opt_CancelLastString())
	def Opt_Run(self):
		ss=self.__ss
		lv=ss.Get_ListView()
		# lv.edit(lv.model().index(lv.model().rowCount()-1,0))
		ss.show()
		ss.Set_AdditionHint("<新增字串(只允许纯数字两位以上)>")
		data=ss.exec()
		print(data)
		# super().Opt_Run()
		return ss











