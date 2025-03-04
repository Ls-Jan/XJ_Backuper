

from XJ_Saver.XJQ_Saver_Git.XJQ_Saver_Git import XJQ_Saver_Git
from XJ_Saver.XJ_Git import XJ_Git,RunCMD
from XJ_Saver.XJ_GitRecord import XJ_GitRecord
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


path=''
path='.'
path='./Repository'


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


# if True:
if False:
	rst=XJ_Git.Get_ChangedFiles(path=path)
	print(rst.changed)
	record={
		'A':rst.add,
		'M':rst.modify,
		'R':rst.rename,
		'D':rst.delete
	}
	for n in record:
		print(n)
		for j in record[n]:
			print(j)
		print()
	print(rst.unknown)
	exit()

# if True:
if False:
	rst=XJ_Git.Get_CommitChildren(path)
	for node,children in rst.children.items():
		print(node,children)
	print(rst.rootCommit)
	exit()

# if True:
if False:
	tree=[[-1]]
	gr=XJ_GitRecord(tree)
	gr.Opt_LoadFromLocal(path)
	for i in range(len(tree)):
		print(i,tree[i])
	print(gr.commitIndex)
	print(tree)
	exit()


from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree
# if True:
if False:
	app=QApplication([])
	vtree=XJQ_VisibleTree()
	tree=vtree.Get_Tree()
	tree.clear()
	tree.extend([[-1, 1], [-1, 2], [-1, 4, 3], [-1, 5], [-1], [-1]])
	vtree.Opt_Update()
	vtree.Get_Canvas().show()
	for i in range(len(tree)):
		vtree.Get_Node(i).setText(str(i))
	tree.Set_NodeSize(3,200)
	vtree.Opt_Update()

	exit(app.exec())


if True:
	# rst=XJ_Git.Get_BranchNames(path=path)
	# print(rst.headBranch)
	# print(rst.headCommit)
	# print(rst.nameLst)
	# exit()

	# rst=XJ_Git.Get_RecentCommits(-1,path).commits
	# for i in range(len(rst)):
	# 	print(i,rst[i])
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






