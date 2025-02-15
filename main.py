

from XJ_Saver.XJ_Git import XJ_Git
from XJ_Saver.XJ_GitRecord import XJ_GitRecord
from XJ.Widgets.XJQ_VisibleTree import XJQ_VisibleTree

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

path='./Repository'
# path='./x'

if True:
	# gm=XJ_GitManager([])
	# gm.Opt_LoadFromLocal(path)
	# print(gm.tree)
	# exit()

	app=QApplication([])
	vt=XJQ_VisibleTree()
	gr=XJ_GitRecord(vt.Get_Tree())
	gr.Opt_LoadFromLocal(path)
	vt.Opt_Update()

	app.exec()
exit()







