import photosite.gallery_helper as helper
import photosite.photodb
from photosite.photodb import ImageDatabase


def build_data(db_filename: str = photosite.photodb.image_database) -> tuple:
    with ImageDatabase(db_filename) as db:
        photo_list = db.get_all_photos()
    index_map = {}
    latest_date_key = _date_key_from_photo(photo_list[0])
    for photo in photo_list:
        date_key = _date_key_from_photo(photo)

        index_for_date = index_map.get(
            date_key,
            {
                "display-date": photo["created"].strftime(r"%B %Y"),
                "index_filename": _index_filename(date_key, latest_date_key),
                "photos": [],
            },
        )
        index_for_date["photos"].append(
            {
                "thumb": helper._photo_name_to_thumbnail(photo, "thumbnails"),
                "image": photo["image_path"],
                "image-info": helper._create_page_data_from_photo(photo),
            }
        )
        index_map[date_key] = index_for_date

    indices = []
    for key in sorted(index_map.keys(), reverse=True):
        indices.append(
            {
                "display-date": index_map[key]["display-date"],
                "index_filename": index_map[key]["index_filename"],
            }
        )

    return (index_map, indices)


def _date_key_from_photo(photo: dict) -> str:
    return photo["created"].strftime(r"%Y%m")


def _index_filename(current_date_key: str, latest_date_key) -> str:
    return (
        f"index.md"
        if current_date_key == latest_date_key
        else f"index-{current_date_key}.md"
    )
