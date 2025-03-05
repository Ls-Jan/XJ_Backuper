



from PyQt5.QtWidgets import QStyledItemDelegate,QLineEdit,QWidget,QStyleOptionViewItem
from PyQt5.QtCore import pyqtSignal,QModelIndex,Qt

class TextEditDelegate(QStyledItemDelegate):
	'''
		只有一个目的：打开编辑器时发送信号(newEditor)。
		过程中发现居中效果不佳，附上alignCenter选择性的调整位置
	'''
	newEditor=pyqtSignal(QLineEdit,QModelIndex)
	alignCenter=False
	def createEditor(self,parent:QWidget,option:QStyleOptionViewItem,index:QModelIndex):
		editor=super().createEditor(parent,option,index)
		if(isinstance(editor,QLineEdit)):
			self.newEditor.emit(editor,index)
		return editor
	def updateEditorGeometry(self, editor, option, index):
		'''
			莫名其妙，这个函数会被调用两次，
			并且第二次QLineEdit的宽发生了变化，并且内容进行了两次同样的设置，
			导致createEditor后首次设置的位置被更改，莫名其妙。
		'''
		super().updateEditorGeometry(editor, option, index)
		if(self.alignCenter):
			editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
			W=option.rect.width()
			w=editor.width()
			editor.move((W-w)>>1,editor.y())


