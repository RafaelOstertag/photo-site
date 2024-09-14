#!/usr/bin/env bash

set -euo pipefail

. "$(dirname $0)/common.sh"

echo "Start generating thumbnails"

for image_dir in ${IMAGE_DIRS}
do
    thumbnail_dir="${image_dir}/thumbnails"
    mkdir -p "${thumbnail_dir}"
    for image in "${image_dir}"/*.jpg
    do
        filename=$(basename "${image}")
        thumbnail_filepath="${thumbnail_dir}/${filename%%.jpg}.webp"
        if [ "${image}" -nt "${thumbnail_filepath}" ]
        then
            echo "Generate thumbnail for ${image} -> ${thumbnail_filepath}"
            convert -define webp:method=3 -define webp:image-hint=photo -strip -resize x350 "${image}" "${thumbnail_filepath}" &
        fi

        if [ $(jobs -r | wc -l | tr -d " ") -ge 4 ]
        then
            wait
        fi
    done
done

echo "Done generating thumbnails"