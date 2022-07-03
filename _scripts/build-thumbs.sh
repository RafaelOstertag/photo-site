#!/usr/bin/env bash

set -euo pipefail

. "$(dirname $0)/common.sh"

# Thumbnail creation

for image_dir in ${IMAGE_DIRS}
do
    thumbnail_dir="${image_dir}/thumbnails"
    medium_dir="${image_dir}/mediums"
    mkdir -p "${thumbnail_dir}"
    mkdir -p "${medium_dir}"
    for image in "${image_dir}"/*.jpg
    do
        filename=$(basename "${image}")
        thumbnail_filepath="${thumbnail_dir}/${filename}"
        medium_filepath="${medium_dir}/${filename}"
        if [ "${image}" -nt "${thumbnail_filepath}" ]
        then
            echo "Generate thumbnail for ${image} -> ${thumbnail_filepath}"
            convert -strip -resize '15%' "${image}" "${thumbnail_filepath}"
        else
            echo "Skipping thumbnail generation for ${image}"
        fi
        if [ "${image}" -nt "${medium_filepath}" ]
        then
            echo "Generate medium image for ${image} -> ${medium_filepath}"
            convert -strip -resize '50%' "${image}" "${medium_filepath}"
        else
            echo "Skipping medium image generation for ${image}"
        fi
    done
done
