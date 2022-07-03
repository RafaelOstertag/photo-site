#!/usr/bin/env bash

set -euo pipefail

. "$(dirname $0)/common.sh"

thumbnails=$(find ${IMAGE_BASE} -name thumbnails -type d | sed -e 's/^/Disallow: \//')

cat >robots.txt <<EOF
Sitemap: https://www.rafaelostertag.photo/sitemap.xml

User-agent: *
${thumbnails}
EOF
