import os
import glob
import concurrent.futures

from photosite.photo import Photo


def gallery_data_all_photos() -> tuple:
    photo_list = _find_all_photos()
    index_map = {}
    latest_date_key = _date_key_from_photo(photo_list[0])
    for photo in photo_list:
        date_key = _date_key_from_photo(photo)

        index_for_date = index_map.get(date_key, {
            'display-date': photo.date_time.strftime(r'%B %Y'),
            'index_filename': _index_filename(date_key, latest_date_key),
            'photos': []
        })
        index_for_date['photos'].append({
            'thumb': _photo_name_to_thumbnail(photo, 'thumbnails'),
            'image': photo.path,
            'image-info': _create_page_data_from_photo(photo)
        })
        index_map[date_key] = index_for_date

    indices = []
    for key in sorted(index_map.keys(), reverse=True):
        indices.append({
            'display-date': index_map[key]['display-date'],
            'index_filename': index_map[key]['index_filename']
        })

    return (index_map, indices)


def gallery_data(file_list: list) -> list:
    photo_list = _read_photos(file_list)
    return [{
            'thumb': _photo_name_to_thumbnail(photo, 'thumbnails'),
            'image': photo.path,
            'image-info': _create_page_data_from_photo(photo)
            } for photo in photo_list]


def gallery_data_with_tags(s: str) -> list:
    all_photos = _find_all_photos()
    return [
        {
            'thumb': _photo_name_to_thumbnail(photo, 'thumbnails'),
            'image': photo.path,
            'image-info': _create_page_data_from_photo(photo)
        }
        for photo in all_photos
        if _contains(photo.tags, s)
    ]


def _contains(lst: list, s: str) -> bool:
    for i in lst:
        if s.casefold() in i.casefold():
            return True
    return False


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
    return f'index.md' if current_date_key == latest_date_key else f"index-{current_date_key}.md"


def _find_all_photos() -> list:
    image_files = glob.glob('assets/images/*/*.jpg', root_dir='.')
    return _read_photos(image_files)


def _read_photos(image_files):
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        image_list = [x for x in executor.map(lambda x: Photo(x), image_files)]
    image_list.sort(key=lambda x: x.date_time, reverse=True)
    return image_list


def _photo_name_to_thumbnail(photo: Photo, path: str) -> str:
    return os.path.join(photo.dirname, path, photo.filename)
