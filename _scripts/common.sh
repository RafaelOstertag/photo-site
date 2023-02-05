IMAGE_BASE=assets/images
IMAGE_DIRS=$(find "${IMAGE_BASE}" -type d -not \( -path '*/thumbnails' -or -path '*/mediums' -or -path "${IMAGE_BASE}" \))
STAGING_DIR=~/Pictures/photo-site-stage

echo "Identified image directories"
echo "${IMAGE_DIRS}"
echo ""

