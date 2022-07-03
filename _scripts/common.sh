IMAGE_BASE=assets/images
IMAGE_DIRS=$(find "${IMAGE_BASE}" -type d -not \( -path '*/thumbnails' -or -path '*/mediums' -or -path "${IMAGE_BASE}" \))

echo "Identified image directories"
echo "${IMAGE_DIRS}"
echo ""

