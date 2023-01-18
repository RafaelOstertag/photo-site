#!/usr/bin/env bash

set -euo pipefail

. "$(dirname $0)/common.sh"


for image_dir in ${IMAGE_DIRS}
do
    thumbnail_dir="${image_dir}/thumbnails"
    mkdir -p "${thumbnail_dir}"
    for image in "${image_dir}"/*.jpg
    do
        filename=$(basename "${image}")
        thumbnail_filepath="${thumbnail_dir}/${filename}"
        if [ "${image}" -nt "${thumbnail_filepath}" ]
        then
            echo "Generate thumbnail for ${image} -> ${thumbnail_filepath}"
            convert -strip -resize x300 "${image}" "${thumbnail_filepath}" &
        else
            echo "Skipping thumbnail generation for ${image}"
        fi

        if [ $(jobs -r | wc -l | tr -d " ") -ge 4 ]
        then
            wait
        fi
    done
done
