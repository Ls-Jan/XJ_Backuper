

from XJ_Saver.XJQ_Saver_Git.XJQ_Saver_Git import XJQ_Saver_Git
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *




if False:
	app=QApplication([])

	dlg=QDialog()
	dlg.setWindowTitle('选择分支')
	view=QListWidget()
	btnNew=QPushButton("创建新分支")
	btnApply=QPushButton("确认")
	vbox=QVBoxLayout(dlg)
	hbox=QHBoxLayout()
	vbox.addWidget(view)
	vbox.addStretch(1)
	vbox.addLayout(hbox)
	hbox.addWidget(btnNew)
	hbox.addWidget(btnApply)

	for i in ['<游离>',(str(i) for i in range(5))]:
		view.insertItem(len(view),str(i))
	view.setCurrentIndex(view.model().index(0,0))
	view.pressed.connect(lambda:print([i.row() for i in view.selectedIndexes()]))
	view.show()

	dlg.resize(300,200)
	# group.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
	dlg.exec()
	# app.exec()
	exit()




if True:
	path=''
	path='.'
	path='./Repository'

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






