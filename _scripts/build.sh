#!/bin/sh

set -eu

path=$(dirname $0)

"${path}"/build-thumbs.sh
"${path}"/build-monthly-galleries-data.py
"${path}"/build-favorites-data.py
"${path}"/build-monthly-galleries.py

jekyll clean
jekyll build
