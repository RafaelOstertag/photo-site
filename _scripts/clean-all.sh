#!/usr/bin/env bash

set -eu

path=$(dirname $0)

jekyll clean

thumbnail_dirs=$(find assets/images -name thumbnails)
if [ -n "${thumbnail_dirs}" ]
then
    rm -rfv ${thumbnail_dirs}
fi

rm -fv _data/gallery*.yml _data/monthly*.yml