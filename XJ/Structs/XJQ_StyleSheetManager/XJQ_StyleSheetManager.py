
__version__='1.0.0'
__author__='Ls_Jan'

import os
import re

__all__=['XJQ_StyleSheetManager']
class XJQ_StyleSheetManager:
	'''
		专门用于管理样式表的类，
		本类没有多大的继承必要。
	'''
	def __init__(self,**args):
		'''
			args中的参数将直接传给setStyleSheet，可传可不传，看需要。
			只不过不建议传参数，因为指不定哪天会让这个构造函数无参
		'''
		self.__qss={}
		#py的多继承，有点屎说实话，成员函数重名的情况下要通过这个方式确保调用的是本类中的函数
		#于是我也理解了，为什么有的类，一旦多继承就会爆胎，我这就是通过self调用结果立马翻车，然后改用类名的方式调用才正常运行
		args.setdefault('qss','')
		XJQ_StyleSheetManager.setStyleSheet(self,**args)
	def setStyleSheet(self,qss:str,name:str='',multi:bool=False,clear:bool=False):
		'''
			设置样式表，qss可为文件路径。

			multi参数用于处理qss中夹杂多张子表的情况，例如传入qss样式为'A{bg:red};B{fg:yellow}'，会分析为两份名称分别为A和B的样式表并分别记录下来

			clear参数是为了减少不必要的内存占用，在样式表读取后如果不再需要读取其中的数据时可指定clear为真，以清除内部记录
		'''
		if(clear):
			self.__qss.clear()
		else:
			try:
				if(os.path.isfile(qss)):
					with open(qss,'r',encoding='utf-8') as f:
						qss=f.read()
					qss=re.sub('/\*.*?\*/','',qss)#替换掉注释
				if(multi):
					count=0
					record=[]
					content=''
					for ch in qss:
						content+=ch
						if(ch=='{'):
							if(count==0):
								record.append([content[:-1].strip()])
								content=content[-1:]
							count+=1
						elif(ch=='}'):
							count-=1
							if(count==0):
								record[-1].append(content)
								content=''
					for item in record:
						XJQ_StyleSheetManager.setStyleSheet(self,item[1][1:-1],item[0])
				else:
					if(qss.strip()):
						self.__qss[name]=qss
			except Exception as e:
				print(f'【样式读取出现错误】\n{e}\n')
				return False
		return True
	def styleSheet(self,name:str='',returnNames:bool=False,returnDict:bool=False):
		'''
			获取样式表。
			如果指定returnNames则返回样式表名称(列表)，
			如果指定returnDict则返回记录的字典数据
		'''
		return self.__qss if returnDict else list(self.__qss.keys()) if returnNames else self.__qss.get(name,'')


