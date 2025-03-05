
__version__='1.1.0'
__author__='Ls_Jan'
__all__=['TreeNode']

class TreeNode(list):
	'''
		继承于List[int]，列表内容记录父索引和子节点索引。
		该类不单独使用，与XJ_ArrayTree组合成数组树。
		将该类暴露出去是为了方便外部使用。
		
		外部只需(也只应该)关心列表内容(子节点索引)即可。
		如有需要，可以对其进行派生以记录其他数据。
	'''
	_x:int=0#左
	_y:int=0#上
	_w:int=0#宽
	_h:int=0#高
	_cw:int=0#列最大宽(根据当前对齐情况而变化)
	_node_isVisible:int=1#可见等级。完全可见(1)、仅隐去子节点(0)、本节点及子节点不可见(-1)


