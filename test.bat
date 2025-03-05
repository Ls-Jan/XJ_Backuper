
@echo off

pushd Repository
@REM git show-branch 
@REM git stash list

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
@REM git switch HEAD~3

@REM git checkout -f master
@REM type nul>D
@REM git add .
@REM git checkout -f C
@REM git restore --source C .
@REM git clean -xdf
@REM git checkout -f master
@REM git checkout -f A
@REM git add .
@REM git restore --source A .
@REM git stash 
@REM git stash pop
@REM git restore --source 11760fe .
@REM git stash clear

echo.
git log --oneline --all --graph

