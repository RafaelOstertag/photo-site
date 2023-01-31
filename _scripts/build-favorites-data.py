#!/usr/bin/env python3

import logging

import photosite.favorite_gallery
import yaml

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


if __name__ == "__main__":
    logging.info("Building favorites gallery data")
    with open("_data/favorites.yml", "r", encoding="utf-8") as f:
        photos_list = photosite.favorite_gallery.build_data(yaml.full_load(f))

    with open("_data/gallery_favorites.yml", "w", encoding="utf-8") as f:
        yaml.dump(photos_list, stream=f)

    logging.info("Done building favorites gallery data")
