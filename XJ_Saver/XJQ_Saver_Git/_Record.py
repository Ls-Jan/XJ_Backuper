
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['_Record']

from ..XJQ_Saver_Base import XJQ_Saver_Base
from .XJQ_GitOperator import XJQ_GitOperator

class _Record:
	'''
		简化XJQ_Saver_Git的部分代码。
		需要使用with语句。
		例如：
			rec=_Record(...)
			with rec:
				rec.op.Git_AddCommit("Msg")
	'''
	op:XJQ_GitOperator
	__saver:XJQ_Saver_Base
	__mskSwitch:bool
	def __init__(self,saver:XJQ_Saver_Base,op:XJQ_GitOperator):
		self.op=op
		self.__saver=saver
		self.__mskSwitch=False
	def __enter__(self):
		self.__mskSwitch=self.__saver.Set_Busy(True)
	def __exit__(self,exc_type,exc_val,exc_tb):
		if(self.op.success):
			self.__saver.Opt_Update()
		self.__saver.Set_Busy(not self.__mskSwitch)


