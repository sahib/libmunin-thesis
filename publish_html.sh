#!/bin/sh
# This is probably very prone to fail.
git checkout $1
make clean html singlehtml && cp _build/*html /tmp -r;
git checkout gh-pages
rm projekt -rf  
mkdir -p projekt 
cp /tmp/*html projekt -r
git add projekt
git commit -am 'Automated update.'
git checkout master
