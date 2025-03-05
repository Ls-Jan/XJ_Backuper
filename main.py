
'''
	建议运行CreateGitExample.py快速建立仓库以便查看效果
'''

from XJ_Saver.XJQ_Saver_Git import XJQ_Saver_Git
from PyQt5.QtWidgets import QApplication

if True:
	path='.'
	path='./Repository'
	app=QApplication([])

	sv=XJQ_Saver_Git()
	if path:
		sv.Set_Path(path)
	sv.show()

	app.exec()






