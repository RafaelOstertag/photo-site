#!/usr/bin/env python3

import yaml
import os
import os.path

favorite_photo_md_content="""---
layout: favoritesphoto
title: "Photo"
image: {}
---
"""


if __name__ == "__main__":
    with open('_data/favorites.yml', 'r', encoding='utf-8') as f:
        photo_path_list = yaml.load(f, yaml.Loader)

    for photo_path in photo_path_list:
        photo_path_without_prefix = photo_path.removeprefix('assets/images/')
        photo_basename = os.path.basename(photo_path_without_prefix)

        photo_page_name = photo_basename.removesuffix('.jpg') + ".md"
        photo_md_path = 'favorites/photos/' + os.path.dirname(photo_path_without_prefix)
        os.makedirs(photo_md_path, exist_ok=True)
        photo_md_filepath = photo_md_path +'/' + photo_page_name

        with open(photo_md_filepath, 'w', encoding='utf-8') as f:
            f.write(favorite_photo_md_content.format(photo_path))
