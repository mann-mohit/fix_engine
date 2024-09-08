#!/bin/bash

FIX_HOME="/home/repos/fix_engine"
cd ${FIX_HOME}

scriptName=${0}
packageName=${1}

if [ ${#} -ne 1 ]
then
	echo "Usage error"
	exit 1
fi

SCR="${FIX_HOME}/src/scripts"

makefileCreator="${SCR}/MakefileCreator.py"

/usr/bin/python3 ${makefileCreator} ${packageName}
if [ ${?} -ne 0 ]
then
	echo "Error in creating makefile"
	exit(1)
fi

targetDir="${FIX_HOME}/target/
