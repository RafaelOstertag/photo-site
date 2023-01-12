#!/bin/sh

set -eu

path=$(dirname $0)

"${path}"/build-thumbs.sh
"${path}"/build-data.py
"${path}"/build-favorites-data.py
"${path}"/build-index-files.py
"${path}"/build-photo-pages.sh
"${path}"/build-favorites-photo-pages.py

jekyll clean
jekyll build
