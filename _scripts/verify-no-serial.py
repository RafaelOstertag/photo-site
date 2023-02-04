#!/usr/bin/env python3

import logging
import sys

import photosite.serial
import yaml

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


if __name__ == "__main__":
    body_serials, lens_serials = photosite.serial.find_serial()

    fail = False

    if len(body_serials) > 0:
        fail = True
        print("Photos with body serial")
        [print(i) for i in body_serials]

    if len(lens_serials) > 0:
        fail = True
        print("Photos with lens serial")
        [print(i) for i in lens_serials]

    sys.exit(1) if fail else sys.exit(0)
