import os
import glob

from photosite.photo import Photo


def read_photo_data() -> tuple:
    """Read photos and data.

    Returns a tuple containing the index list (list of images) and 
    photo page map, keyed by image name containing additional information
    """
    return _photo_list_to_data(_find_images())


def _create_page_data_from_photo(photo: Photo) -> map:
    photo_page_data = {}
    photo_page_data['focal_length'] = photo.focal_length
    photo_page_data['exposure'] = photo.exposure
    photo_page_data['aperture'] = photo.aperture
    photo_page_data['iso'] = photo.iso
    photo_page_data['lens'] = photo.lens
    photo_page_data['tags'] = photo.tags
    photo_page_data['medium'] = _photo_name_to_thumbnail(photo, 'mediums')
    return photo_page_data


def _date_key_from_photo(photo: Photo) -> str:
    return photo.date_time.strftime(r'%Y%m')


def _index_filename(current_date_key: str, latest_date_key) -> str:
    return f'index.html' if current_date_key == latest_date_key else f"index-{current_date_key}.html"


def _photo_list_to_data(photo_list: list) -> tuple:
    """
    photo_list is supposed to be sorted by date descending
    """
    index_map = {}
    photo_page_map = {}
    latest_date_key = _date_key_from_photo(photo_list[0])
    latest_date = photo_list[0].date_time.date()
    for idx, photo in enumerate(photo_list):
        index_data = {}
        photo_page_data = _create_page_data_from_photo(photo)

        if idx > 0:
            photo_page_data['prev'] = _photo_name_to_html_page(
                photo_list[idx-1])
        if idx < (len(photo_list)-1):
            photo_page_data['next'] = _photo_name_to_html_page(
                photo_list[idx+1])

        photo_page_map[photo.path] = photo_page_data

        date_key = _date_key_from_photo(photo)
        photo_page_data['index_filename'] = _index_filename(
            date_key, latest_date_key)

        index_for_date = index_map.get(date_key, {
            'display-date': photo.date_time.strftime(r'%B %Y'),
            'index_filename': _index_filename(date_key, latest_date_key),
            'photos': []
        })
        index_for_date['photos'].append({
            'page': _photo_name_to_html_page(photo),
            'thumb': _photo_name_to_thumbnail(photo, 'thumbnails'),
            'latest': photo.date_time.date() == latest_date
        })
        index_map[date_key] = index_for_date

        index_data['page'] = _photo_name_to_html_page(photo)
        index_data['thumb'] = _photo_name_to_thumbnail(photo, 'thumbnails')
        index_data['display-date'] = photo.date_time.strftime(r'%B %Y')

    return (index_map, photo_page_map)


def _find_images() -> list:
    image_list = [Photo(x) for x in glob.glob(
        'assets/images/*/*.jpg', root_dir='.')]
    image_list.sort(key=lambda x: x.date_time, reverse=True)
    return image_list


def _photo_name_to_html_page(photo: Photo) -> str:
    return os.path.join('photos', photo.path.removeprefix('assets/images/').removesuffix('.jpg') + '.html')


def _photo_name_to_thumbnail(photo: Photo, path: str) -> str:
    return os.path.join(photo.dirname, path, photo.filename)
