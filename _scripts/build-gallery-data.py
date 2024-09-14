#!/usr/bin/env python3

import logging

import photosite.gallery
import yaml

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


if __name__ == "__main__":
    logging.info("Building gallery data")
    photos_list = photosite.gallery.build_data()

    with open("_data/gallery.yml", "w", encoding="utf-8") as f:
        yaml.dump(photos_list, stream=f)

    logging.info("Done building gallery data")
