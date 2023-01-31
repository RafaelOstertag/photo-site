#!/usr/bin/env python3

import argparse
import logging

import photosite.tag_gallery
import yaml

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="build-tag-data",
        description="Build photo list of photos having matching tags",
    )
    parser.add_argument("tag")
    args = parser.parse_args()

    logging.info("Building tag gallery data for %s", args.tag)
    photos_list = photosite.tag_gallery.build_data(args.tag)
    with open(f"_data/gallery_{args.tag}.yml", "w", encoding="utf-8") as f:
        yaml.dump(photos_list, stream=f)
    logging.info("Done building tag gallery data for %s", args.tag)
