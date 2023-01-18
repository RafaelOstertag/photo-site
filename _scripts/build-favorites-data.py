#!/usr/bin/env python3

import yaml
import photosite

if __name__ == "__main__":
    with open('_data/favorites.yml', 'r', encoding='utf-8') as f:
        photos_list = photosite.gallery_data(yaml.full_load(f))
    with open('_data/gallery_favorites.yml', 'w', encoding='utf-8') as f:
        yaml.dump(photos_list, stream=f)
