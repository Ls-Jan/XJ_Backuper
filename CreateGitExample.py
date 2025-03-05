
'''
	用于快速生成Git样例
'''


import subprocess
import pathlib
import os

def RunCMD(cmd:str,path:str)->bytes:
	'''
		运行命令并将结果返回。
		接受一个func函数用于处理每行的内容
	'''
	path=pathlib.Path(path)#将路径分隔符自动转换成系统对应符号，傻逼windows喜欢反斜杠
	cmd=f'pushd {path} && {cmd}'
	proc=subprocess.run(cmd,capture_output=True,shell=True)#pushd可以不用切盘符即可切换路径。(text=True是个垃圾参数，用了大概率暴毙，猜测是字符编码问题
	return proc.stdout if proc.stdout else proc.stderr

def WriteFile(name:str,context:str=None,path:str='.',append:bool=True):
	'''
		创建一个文件并向其中追加(或清除重写)指定内容
	'''
	file=pathlib.Path(path).joinpath(name)
	with open(str(file),'a' if append else 'w') as f:
		f.write(context)


if True:
	repo='Repository'

	rst=RunCMD(f'rmdir /Q /S {repo}','.')#移除目录
	rst=RunCMD(f'mkdir {repo}','.')#创建目录
	rst=RunCMD(f'git init',repo)#创建git仓库
	WriteFile('init','init',repo)#生成一个文件，否则无法提交
	rst=RunCMD(f'git add . && git commit -m init',repo)

	# lst=['master','A']
	lst=['master','A','B','C']
	for n in lst:
		rst=RunCMD('git checkout HEAD~3',repo)
		rst=RunCMD(f'git switch -c {n}',repo)
		for i in range(len(lst)-1):
			c=f'{n.lower()}{i}'
			WriteFile(n,f'{c}\n',repo)
			rst=RunCMD(f'git add . && git commit -m {c}',repo)
		rst=RunCMD(f'git checkout master',repo)
		rst=RunCMD(f'git merge --no-ff {n}',repo)

	os.system(f'pushd {repo} && git log --oneline --all --graph')


