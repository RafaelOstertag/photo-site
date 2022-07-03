#!/bin/sh

set -euo pipefail

path=$(dirname $0)

"${path}"/build-thumbs.sh
"${path}"/build-data.py
"${path}"/build-index-files.py
"${path}"/build-photo-pages.sh

jekyll clean
jekyll build
