#!/usr/bin/env python3

import logging

import photosite.monthly_gallery
import yaml

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

if __name__ == "__main__":
    logging.info("Building monthly gallery data")
    index_map, indices = photosite.monthly_gallery.build_data()

    with open("_data/monthly_gallery_map.yml", "w", encoding="utf-8") as f:
        yaml.dump(index_map, stream=f)

    with open("_data/monthly_galleries_list.yml", "w", encoding="utf-8") as f:
        yaml.dump(indices, stream=f)

    logging.info("Done building monthly gallery data")
