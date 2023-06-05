#!/bin/sh

set -eu

path=$(dirname $0)

"${path}"/build-thumbs.sh
"${path}"/maintain-image-db.py

"${path}"/verify-no-serial.py

"${path}"/build-monthly-galleries-data.py
"${path}"/build-favorites-data.py
"${path}"/build-tag-data.py "Black & White" --suffix=bw
"${path}"/build-tag-data.py "Creux du Van" --suffix=cdv
"${path}"/build-monthly-galleries.py

jekyll clean
jekyll build
