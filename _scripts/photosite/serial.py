import photosite.gallery_helper as helper
import photosite.photodb
from photosite.photodb import ImageDatabase


def find_serial(db_filename: str = photosite.photodb.image_database) -> tuple:
    with ImageDatabase(db_filename) as db:
        photos_with_body_serial = db.photos_with_body_serial()
        photos_with_lens_serial = db.photos_with_lens_serial()

    return (photos_with_body_serial, photos_with_lens_serial)
