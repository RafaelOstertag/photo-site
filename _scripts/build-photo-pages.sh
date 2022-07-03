#!/usr/bin/env bash

set -euo pipefail

BASE_DIR=photos

. "$(dirname $0)/common.sh"

for image_dir in ${IMAGE_DIRS}
do
    html_dir="${BASE_DIR}/$(basename "${image_dir}")"
    mkdir -p "${html_dir}"
    
    for image in "${image_dir}"/*.jpg
    do
        page_name=$(basename "${image}" .jpg)
        cat > "${html_dir}"/${page_name}.md <<EOF
---
layout: photo
title: "Photo"
image: ${image}
---
EOF
    done
done
