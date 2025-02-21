

from XJ_Saver.XJQ_Saver_Git import XJQ_Saver_Git
from XJ_Saver.XJ_Git import XJ_Git
from XJ_Saver.XJ_GitRecord import XJ_GitRecord
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


import subprocess


# if True:
# 	app=QApplication([])

# 	wid=QWidget()
# 	box=QHBoxLayout(wid)
# 	smp=QSignalMapper()
# 	for i in range(3):
# 		btn=QPushButton(str(i))
# 		btn.resize(100,100)
# 		btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding))
# 		box.addWidget(btn)
# 		btn.clicked.connect(smp.map)
# 		smp.setMapping(btn,btn)
# 	btn.clicked.disconnect(smp.map)
# 	smp.mappedWidget.connect(lambda btn:print("4>",btn.text()))

# 	wid.show()
# 	wid.resize(600,200)
# 	app.exec()
# 	exit()





if True:
	path=''
	path='.'
	# path='./Repository'

	# rst=XJ_Git.Get_RecentCommits(-1,path).commits
	# for i in range(len(rst)):
	# 	print(i,rst[i])
	# exit()

	# tree=[[-1]]
	# gr=XJ_GitRecord(tree)
	# gr.Opt_LoadFromLocal(path)
	# for i in range(len(tree)):
	# 	print(i,tree[i])
	# print(gr.commitIndex)
	# exit()

	# print(gr.commits)
	# exit()
	# rst=XJ_Git.Get_Merges(path)
	# rst=XJ_Git.Get_RecentCommits(-1,path)
	# print(rst.nameLst)
	# exit()



	app=QApplication([])

	sv=XJQ_Saver_Git()
	if path:
		sv.Set_Path(path)
	sv.show()

	app.exec()






