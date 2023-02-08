import os


def _photo_name_to_thumbnail(photo: dict, path: str) -> str:
    photo_dirname = os.path.dirname(photo["image_path"])
    photo_filename = os.path.basename(photo["image_path"])
    return os.path.join(photo_dirname, path, photo_filename)


def _create_page_data_from_photo(photo: dict) -> dict:
    photo_page_data = {}
    photo_page_data["focal_length"] = photo["focal_length"]
    photo_page_data["exposure"] = photo["exposure"]
    photo_page_data["aperture"] = photo["aperture"]
    photo_page_data["iso"] = photo["iso"]
    photo_page_data["lens"] = photo["lens"]
    photo_page_data["tags"] = photo["tags"]
    return photo_page_data
