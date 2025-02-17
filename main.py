

from XJ_Saver.XJ_Saver_Git import XJ_Saver_Git
from XJ_Saver.XJ_Git import XJ_Git
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


if True:
	path='./Repository'

	# rst=XJ_Git.Get_Merges(path)
	# rst=XJ_Git.Get_RecentCommits(-1,path)
	# print(rst.nameLst)
	# exit()



	app=QApplication([])

	sv=XJ_Saver_Git()
	# sv.Set_Path(path)

	app.exec()






