import photosite.gallery_helper as helper
import photosite.photodb
from photosite.photodb import ImageDatabase


def build_data(db_filename: str = photosite.photodb.image_database) -> tuple:
    with ImageDatabase(db_filename) as db:
        photo_list = db.get_all_photos()
    return [
        {
            "thumb": helper._photo_name_to_thumbnail(photo, "thumbnails"),
            "image": photo["image_path"],
            "image-info": helper._create_page_data_from_photo(photo),
        }
        for photo in photo_list
    ]
