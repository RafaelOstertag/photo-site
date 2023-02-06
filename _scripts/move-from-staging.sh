#!/usr/bin/env bash

set -euo pipefail

. "$(dirname $0)/common.sh"

get_create_date() {
    local photo=$1

    exiftool -t "${photo}" | awk 'BEGIN { FS="\t" } $1 == "Create Date" { print $2 }' | head -1
}

concat_year_and_month() {
    local date=$1

    year=$(echo "${date}" | cut -f 1 -d ':')
    month=$(echo "${date}" | cut -f 2 -d ':')
  
    echo "${year}${month}"
}

for photo in "${STAGING_DIR}"/*.jpg
do
    create_date=$(get_create_date "${photo}")
    year_month=$(concat_year_and_month "${create_date}")
    target_dir="${IMAGE_BASE}/${year_month}"

    if [ ! -d "${target_dir}" ]
    then
        mkdir -p "${target_dir}"
    fi

    mv -iv "${photo}" "${target_dir}/"
done

