
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtGui import QColor

__all__=['QColorToRGBA']
def QColorToRGBA(col:QColor,returnCSS:bool=False):
	'''
		蟹蟹，有被烦到，好几次被这个鸡肋给整蛊，实在受不了了，哪怕这函数再弱智也单独写出来。

		将QColor转化为RGBA元组，如果returnCSS为真那么会顺手处理为'rgba(r,g,b,a)'这种样式
	'''
	rgba=[col.red(),col.green(),col.blue(),col.alpha()]
	if(returnCSS):
		rgba[-1]=round(rgba[-1]/255,3)
	rgba=tuple(rgba)
	return f'rgba{rgba}' if returnCSS else rgba

