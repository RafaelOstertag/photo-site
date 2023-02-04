#!/usr/bin/env python3
#
# Verifies that no photos contain serial numbers of the camera body or lens.
#
# It will exit with a return code of 1, if it finds serial numbers.


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

    if fail:
        print("""
        ##
        ## Photos found with embedded serial numbers
        ##
        """)
        sys.exit(1)
    else:
        print("No photos with serial numbers found. Good.")
