#!/bin/sh

set -eu
RD_OPTION_REBUILD=${RD_OPTION_REBUILD:-NO}

path=$(dirname $0)

"${path}"/build-thumbs.sh
"${path}"/maintain-image-db.py

"${path}"/verify-no-serial.py

"${path}"/build-monthly-galleries-data.py
# "${path}"/build-tag-data.py "Black & White" --suffix=bw
"${path}"/build-monthly-galleries.py

if [ "${RD_OPTION_REBUILD}" = "YES" ]; then
    jekyll clean
    jekyll build
else
    jekyll build --incremental
fi
