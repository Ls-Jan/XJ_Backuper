
__version__='1.0.0'
__author__='Ls_Jan'


import os
import inspect

__all__=['GetRealPath']
def GetRealPath(relativePath:str):
	'''
		用于获取对应的绝对路径，
		调用者(脚本/模块)所在目录为根路径，
		人话就是，调用该函数的语句在哪个脚本/模块的，根路径就以那个脚本/模块为准
	'''
	info=inspect.stack()[1]#调用者的上下文信息
	path=info.filename#本文件路径
	path=os.path.split(path)[0]#当前所在目录
	path=os.path.join(path,relativePath)#路径拼接
	path=os.path.realpath(path)#改成绝对路径
	return path

