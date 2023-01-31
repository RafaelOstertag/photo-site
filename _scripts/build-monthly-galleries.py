#!/usr/bin/env python3

import yaml


def _write_indices(monthly_gallery_map: dict):
    sorted_key_list = sorted(monthly_gallery_map, reverse=True)
    for key in sorted_key_list:
        filename = monthly_gallery_map[key]["index_filename"]
        with open(filename, "w", encoding="utf-8") as indexfile:
            indexfile.write(
                f"""---
layout: monthly_gallery
title: {monthly_gallery_map[key]['display-date']}
month_key: '{key}'
---
"""
            )


if __name__ == "__main__":
    with open("_data/monthly_gallery_map.yml", "r", encoding="utf-8") as f:
        _write_indices(yaml.full_load(f))
