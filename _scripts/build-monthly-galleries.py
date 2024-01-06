#!/usr/bin/env python3

import os.path

import yaml


def _write_indices(monthly_gallery_map: dict):
    sorted_key_list = sorted(monthly_gallery_map, reverse=True)
    for key in sorted_key_list:
        filename = monthly_gallery_map[key]["index_filename"]
        with open(os.path.join("monthly",filename), "w", encoding="utf-8") as indexfile:
            indexfile.write(
                f"""---
layout: monthly_gallery
title: {monthly_gallery_map[key]['display-date']}
month_key: '{key}'
description: |
  Step into the ever-changing tapestry of moments at my Monthly Photo Gallery, where every 
  month unfolds as a unique chapter in visual storytelling. As an amateur photographer, I invite you
  to explore the distinct charm of each month captured through my lens. As you navigate through 
  the gallery, you'll experience a diverse range of 
  emotions and perspectives, showcasing the evolving beauty of life. Join me on this monthly photographic
  journey, where amateur enthusiasm meets the rich tapestry of changing seasons.

  This gallery is for the month of {monthly_gallery_map[key]['display-date']}.
---
"""
            )


if __name__ == "__main__":
    with open("_data/monthly_gallery_map.yml", "r", encoding="utf-8") as f:
        _write_indices(yaml.full_load(f))
