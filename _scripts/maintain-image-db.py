#!/usr/bin/env python3

import logging

import photosite.photodb as photodb

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


if __name__ == "__main__":
    photodb.update_database()
