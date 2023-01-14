import os
import glob
import concurrent.futures

from photosite.photo import Photo


def read_photo_data() -> tuple:
    """Read photos and data.

    Returns a tuple containing the index list (list of images) and 
    photo page map, keyed by image name containing additional information
    """
    return _photo_list_to_data(_find_images())


def create_page_data_from_photo(photo: Photo) -> map:
    photo_page_data = {}
    photo_page_data['focal_length'] = photo.focal_length
    photo_page_data['exposure'] = photo.exposure
    photo_page_data['aperture'] = photo.aperture
    photo_page_data['iso'] = photo.iso
    photo_page_data['lens'] = photo.lens
    photo_page_data['tags'] = photo.tags
    photo_page_data['medium'] = photo_name_to_thumbnail(photo, 'mediums')
    return photo_page_data


def _date_key_from_photo(photo: Photo) -> str:
    return photo.date_time.strftime(r'%Y%m')


def _index_filename(current_date_key: str, latest_date_key) -> str:
    return f'index.md' if current_date_key == latest_date_key else f"index-{current_date_key}.md"


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
        photo_page_data = create_page_data_from_photo(photo)

        if idx > 0:
            photo_page_data['prev'] = photo_name_to_html_page(
                photo_list[idx-1], 'photos')
        if idx < (len(photo_list)-1):
            photo_page_data['next'] = photo_name_to_html_page(
                photo_list[idx+1], 'photos')

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
            'page': photo_name_to_html_page(photo, 'photos'),
            'thumb': photo_name_to_thumbnail(photo, 'thumbnails'),
            'latest': photo.date_time.date() == latest_date
        })
        index_map[date_key] = index_for_date

        index_data['page'] = photo_name_to_html_page(photo, 'photos')
        index_data['thumb'] = photo_name_to_thumbnail(photo, 'thumbnails')
        index_data['display-date'] = photo.date_time.strftime(r'%B %Y')

    return (index_map, photo_page_map)


def _find_images() -> list:
    image_files = glob.glob('assets/images/*/*.jpg', root_dir='.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        image_list = [x for x in executor.map(lambda x: Photo(x), image_files)]
    image_list.sort(key=lambda x: x.date_time, reverse=True)
    return image_list


def photo_name_to_html_page(photo: Photo, path: str) -> str:
    return os.path.join(path, photo.path.removeprefix('assets/images/').removesuffix('.jpg') + '.md')


def photo_name_to_thumbnail(photo: Photo, path: str) -> str:
    return os.path.join(photo.dirname, path, photo.filename)
