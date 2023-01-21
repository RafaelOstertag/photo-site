#!/usr/bin/env python3

import yaml
import photosite
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
                    prog = 'build-tag-data',
                    description = 'Build photo list of photos having matching tags')
    parser.add_argument('tag')
    args = parser.parse_args()

    photos_list = photosite.gallery_data_with_tags(args.tag)
    with open(f"_data/gallery_{args.tag}.yml", 'w', encoding='utf-8') as f:
        yaml.dump(photos_list, stream=f)
