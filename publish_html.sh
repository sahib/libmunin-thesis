#!/bin/sh
# This is probably very prone to fail.

function build {
    git checkout $1
    make clean html && cp _build/*html /tmp -r;
    git checkout gh-pages
    mkdir -p $1 
    rm *html -rf && cp /tmp/*html $1 -r
    git add $1
    git commit -am 'Automated update.'
    git checkout master
}

build project
build bachelor
