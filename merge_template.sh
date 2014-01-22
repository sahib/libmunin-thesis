#!/bin/sh
git commit -am "Template change: $1"

git checkout projekt
git merge master

git checkout bachelor
git merge master

git checkout master
