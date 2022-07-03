#!/usr/bin/env python3

import yaml

import photosite

if __name__ == "__main__":
    index_map, photo_page_map = photosite.read_photo_data()

    with open('_data/index_map.yml', 'w', encoding='utf-8') as f:
        yaml.dump(index_map, stream=f)

    with open('_data/photo_page.yml', 'w', encoding='utf-8') as f:
        yaml.dump(photo_page_map, stream=f)
