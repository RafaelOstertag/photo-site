import photosite.gallery_helper as helper
import photosite.photodb
from photosite.photodb import ImageDatabase


def build_data(
    needle: str, db_filename: str = photosite.photodb.image_database
) -> list:
    with ImageDatabase(db_filename) as db:
        photo_list = db.find_photos_by_tags_containing(needle)

    return [
        {
            "thumb": helper._photo_name_to_thumbnail(photo, "thumbnails"),
            "image": photo["image_path"],
            "image-info": helper._create_page_data_from_photo(photo),
        }
        for photo in photo_list
    ]
