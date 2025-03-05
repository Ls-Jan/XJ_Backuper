
__version__='0.0.0'
__author__='Ls_Jan'
__all__=['RunCMD']

import subprocess
from typing import List
import pathlib

def RunCMD(cmd:str,path:str='.',func=lambda row:row,ignoreEmpty:bool=True)->List[str]:
	'''
		运行命令并将结果返回。
		接受一个func函数用于处理每行的内容
	'''
	path=pathlib.Path(path)#将路径分隔符自动转换成系统对应符号，傻逼windows喜欢反斜杠
	cmd=f'pushd {path} && {cmd}'
	print(">>>",cmd)
	proc=subprocess.run(cmd,capture_output=True,shell=True)#pushd可以不用切盘符即可切换路径。(text=True是个垃圾参数，用了大概率暴毙，猜测是字符编码问题
	if(proc.stdout):
		lst=[row.strip() for row in proc.stdout.decode().split('\n')]
		if(ignoreEmpty):
			lst=filter(lambda row:row,lst)
		lst=[func(row) for row in lst] if func else lst
		if(ignoreEmpty):
			lst=list(filter(lambda row:row,lst))
	else:
		lst=[proc.stderr.decode()]
	return lst
