
@echo off

pushd Repository
git log --oneline --all --graph
@REM git show-branch 
@REM git stash list
echo.

@REM git log HEAD --oneline -n 1
@REM git rev-parse --short HEAD
@REM git stash clear

@REM git checkout -f master
@REM DEL B
@REM DEL C
@REM git add .
@REM git stash
@REM git checkout -f C
@REM git restore --source master .
@REM git add .
@REM git stash pop
@REM git reset .

@REM git diff --stat


git checkout -f master
type nul>D
git add .
@REM git checkout -f C
git restore --source C .


@REM git clean -xdf
@REM git checkout -f master
@REM git checkout -f A
@REM git add .

@REM git reset .
@REM git reset --hard B
@REM git reset --hard 99132bc

@REM git status --short





@REM git checkout -f 11760fe
@REM git checkout -f master 
@REM git restore --source A .

@REM git stash 
@REM git stash pop
@REM git restore --source 11760fe .
@REM git stash clear

exit

git checkout B

exit

git restore --source master .

exit

@REM git switch A

exit

git stash pop

exit



@REM git show-branch 
@REM git show-branch master
@REM git show-branch --sparse
@REM git show-branch --independent
@REM git log --oneline --all
@REM git switch ddd
@REM git switch HEAD~3

@REM d8364e6
@REM git show-branch HEAD
@REM git show-branch d8364e6

@REM git checkout master
@REM git merge --no-ff A

@REM git checkout master
@REM git branch a
@REM git branch master

@REM git merge master

@REM git log --all -n -1 --date-order 
@REM git log --oneline --all -n -1 --date-order 
@REM git log master  --oneline --all
@REM git log master --cumulative --oneline --all
@REM git log master --shortstat --oneline --all
@REM git log master --numstat --oneline --all
@REM git log master --raw --oneline --all
@REM git log --simplify-merges --oneline --all
@REM git log master --full-history --ancestry-path --simplify-merges --oneline --all

@REM git log master --simplify-by-decoration --oneline --all
@REM git log --oneline --all --graph
@REM git log --oneline -n 1

@REM git log a --oneline --
@REM git checkout master
@REM git show 99e1843
@REM git show 99e1843
@REM git checkout HEAD~5
@REM git log --merges --oneline --all
@REM git show-branch
@REM git merge-base a master
@REM git merge-base a b
@REM git rev-parse --contains 9f1686c --
@REM git branch --contains 9f1686c --all
@REM git branch --contains 9f1686c --all
@REM git branch --contains 7ad986a --all
@REM git log a --oneline --
@REM git log b --oneline --
@REM git log c --oneline --
@REM git log master --oneline --
@REM git log 99e1843 --oneline --source --
@REM git log master --oneline --source --
@REM git rev-parse --short 9f1686c~
@REM git rev-parse --short dc3bbda~
@REM git rev-parse --short HEAD^^2
@REM git log master --oneline --
@REM git log master --oneline --merges --
@REM git log master --oneline --no-merges --
@REM git log --oneline --graph --all
@REM git reflog
@REM git log --oneline --all

@REM git log -h
@REM git log --oneline --decorate
@REM git log a --oneline --
@REM git log --oneline --all 
@REM git log --oneline --decorate --all 
@REM git log --oneline --decorate --graph --all 
@REM git checkout HEAD~3
@REM git log master
@REM git diff HEAD~4
@REM git rev-parse c
@REM git rev-parse c
@REM git branch -d
@REM git branch -v --no-abbrev

@REM git branch --contains 2bfc99bd780e7561872d440277456fd6cc37f7e3
@REM git branch --contains cb0b68755d8353f2357ebb4961413e32ac7dfbbb
@REM git branch --contains c~7
@REM git branch --contains 469c860f3ebbafea6d1af0b8073abfdde28a07b0
@REM git branch -a
@REM git reset b
@REM git checkout master
@REM git reset HEAD
@REM git checkout .
@REM git reset HEAD~2


