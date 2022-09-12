#!/usr/bin/env python3

import yaml



def _write_indices(index_map: dict):
    sorted_key_list = sorted(index_map, reverse=True)
    for idx, key in enumerate(sorted_key_list):
        filename = index_map[key]['index_filename']
        with open(filename, 'w', encoding='utf-8') as indexfile:
            indexfile.write(f"""---
layout: photoindex
index_key: '{key}'
{f"next: {index_map[sorted_key_list[idx-1]]['index_filename']}" if idx > 0 else "" }
{f"prev: {index_map[sorted_key_list[idx+1]]['index_filename']}" if idx < (len(sorted_key_list)-1) else ""}
---
""")


if __name__ == "__main__":
    with open('_data/index_map.yml', 'r', encoding='utf-8') as f:
        _write_indices(yaml.full_load(f))
