__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .GetRealPath import GetRealPath

__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		p2=GetRealPath('.')
		print('本模块所在路径(该值通过GetRealPath(".")获取): ',p2)
		print()
		return super().Opt_Run()



