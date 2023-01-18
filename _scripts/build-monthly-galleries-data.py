#!/usr/bin/env python3

import yaml
import photosite

if __name__ == "__main__":
    index_map, indices = photosite.gallery_data_all_photos()

    with open('_data/monthly_gallery_map.yml', 'w', encoding='utf-8') as f:
        yaml.dump(index_map, stream=f)

    with open('_data/monthly_galleries_list.yml', 'w', encoding='utf-8') as f:
        yaml.dump(indices, stream=f)
