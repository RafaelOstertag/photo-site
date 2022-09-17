#!/usr/bin/env python3

import yaml

import photosite

def make_favorite_photo_pages(photo_list : list) -> map:
    favorites_page_map = {}
    for idx, photo in enumerate(photo_list):
        favorite_page_data = photosite.create_page_data_from_photo(photo)

        if idx > 0:
            favorite_page_data['prev'] = photosite.photo_name_to_html_page(
                photo_list[idx-1], 'favorites/photos')
        if idx < (len(photo_list)-1):
            favorite_page_data['next'] = photosite.photo_name_to_html_page(
                photo_list[idx+1], 'favorites/photos')

        favorites_page_map[photo.path] = favorite_page_data

    return favorites_page_map

if __name__ == "__main__":

    with open('_data/favorites.yml', 'r', encoding='utf-8') as f:
        photo_path_list = yaml.load(f, yaml.Loader)
    
    photo_list = [photosite.Photo(x) for x in photo_path_list]
    favorites_index_data = [{'thumb': photosite.photo_name_to_thumbnail(x, 'thumbnails'), 'page': photosite.photo_name_to_html_page(x, 'favorites/photos')} for x in photo_list]

    with open('_data/favorites_index.yml', 'w', encoding='utf-8') as f:
        yaml.dump(favorites_index_data, stream=f)

    with open('_data/favorites_photo_page.yml', 'w', encoding='utf-8') as f:
        yaml.dump(make_favorite_photo_pages(photo_list), stream=f)
