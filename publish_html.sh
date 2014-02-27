#!/bin/sh
# This is probably very prone to fail.
git checkout $1
make clean html singlehtml && cp _build/*html /tmp -r;
git checkout gh-pages
rm bachelor -rf  
mkdir -p bachelor
cp /tmp/*html bachelor -r
git add bachelor
git commit -am 'Automated update.'
git checkout master
