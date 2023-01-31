from __future__ import annotations

import concurrent.futures
import glob
import logging
import os
from datetime import datetime

import apsw
import apsw.ext
import photosite.schema as schema
from photosite.photo import ExifPhotoInformation

if os.getenv("IMAGE_DATABASE") is None:
    image_database = "/var/tmp/imagedatabase.sqlite"
else:
    image_database = os.getenv("IMAGE_DATABASE")


class ImageDatabase:
    def __init__(self, db_filename: str = image_database) -> None:
        logging.info("Using image database %s", db_filename)
        self._db_filename = db_filename

    def __enter__(self) -> ImageDatabase:
        self._db_connection = apsw.Connection(self._db_filename)

        schema._ensure_schema(self._db_connection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._db_connection.close()
        return False

    def exists(self, filename: str, mtime: float = None) -> bool:
        with self._db_connection:
            rows = self._db_connection.execute(
                "select image_modified from photo where image_path = ?1", (filename,)
            ).fetchall()
            if len(rows) == 0:
                return False
            if mtime is not None and rows[0][0] != mtime:
                return False
            return True

    def add_or_update(self, photo: photosite.ExifPhotoInformation, mtime: int):
        if not self.exists(photo.path):
            with self._db_connection:
                self._db_connection.execute(
                    """insert into photo 
                (image_path, image_modified, created, aperture, exposure, iso, lens, focal_length, tags) VALUES
                (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)""",
                    (
                        photo.path,
                        mtime,
                        photo.date_time.timestamp(),
                        photo.aperture,
                        photo.exposure,
                        photo.iso,
                        photo.lens,
                        photo.focal_length,
                        "\n".join(photo.tags) if len(photo.tags) > 0 else "",
                    ),
                )
        else:
            with self._db_connection:
                self._db_connection.execute(
                    """update photo
                set image_modified = ?2, created = ?3, aperture = ?4, exposure = ?5, iso = ?6, lens = ?7, focal_length = ?8, tags = ?9
                where image_path = ?1""",
                    (
                        photo.path,
                        mtime,
                        photo.date_time.timestamp(),
                        photo.aperture,
                        photo.exposure,
                        photo.iso,
                        photo.lens,
                        photo.focal_length,
                        "\n".join(photo.tags) if len(photo.tags) > 0 else "",
                    ),
                )

    def remove(self, filename: str):
        with self._db_connection:
            self._db_connection.execute(
                "delete from photo where image_path = ?1", (filename,)
            )

    def all_photo_paths(self) -> list:
        with self._db_connection:
            all_photos = self._db_connection.execute(
                "select image_path from photo order by image_path"
            ).fetchall()
            return [row[0] for row in all_photos]

    def get_all_photos(self) -> list:
        self._db_connection.rowtrace = apsw.ext.DataClassRowFactory(
            dataclass_kwargs={"frozen": True}
        )

        with self._db_connection:
            all_photos = [
                ImageDatabase._row_to_dict(row)
                for row in self._db_connection.execute(
                    "select * from photo order by created desc"
                )
            ]

        self._db_connection.rowtrace = None
        return all_photos

    def get_photos_by_image_paths(self, image_paths: list) -> list:
        self._db_connection.rowtrace = apsw.ext.DataClassRowFactory(
            dataclass_kwargs={"frozen": True}
        )

        in_clause_binders = ",".join("?" * len(image_paths))
        query = f"select * from photo where image_path in ({in_clause_binders}) order by created desc"

        with self._db_connection:
            photos = [
                ImageDatabase._row_to_dict(row)
                for row in self._db_connection.execute(query, image_paths)
            ]

        self._db_connection.rowtrace = None
        return photos

    def find_photos_by_tags_containing(self, needle: str) -> list:
        self._db_connection.rowtrace = apsw.ext.DataClassRowFactory(
            dataclass_kwargs={"frozen": True}
        )

        query = (
            "select * from photo where tags like '%' || ?1 ||'%' order by created desc"
        )
        with self._db_connection:
            photos = [
                ImageDatabase._row_to_dict(row)
                for row in self._db_connection.execute(query, (needle,))
            ]

        self._db_connection.rowtrace = None
        return photos

    def _row_to_dict(row):
        return {
            "id": row.id,
            "image_path": row.image_path,
            "created": datetime.fromtimestamp(row.created),
            "aperture": row.aperture,
            "exposure": row.exposure,
            "iso": row.iso,
            "lens": row.lens,
            "focal_length": row.focal_length,
            "tags": row.tags.split("\n") if row.tags != "" else [],
        }


def update_database(file_name: str = image_database):
    jobs = []
    with ImageDatabase(file_name) as img_db, concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        logging.info("Start updating database")
        image_paths = glob.glob("assets/images/*/*.jpg", root_dir=".")
        for image_path in image_paths:
            mtime = os.path.getmtime(image_path)
            if not img_db.exists(image_path, mtime):
                jobs.append(executor.submit(_read_photo, image_path, mtime))

        logging.info("Jobs: %d", len(jobs))
        for job in jobs:
            photo, mtime = job.result()
            logging.info("Add or update %s", photo.path)
            img_db.add_or_update(photo, mtime)

        logging.info("Remove deleted images from databasae")
        photo_paths_in_db = img_db.all_photo_paths()
        non_existing_paths = [
            path for path in photo_paths_in_db if not os.path.exists(path)
        ]
        for non_existing_path in non_existing_paths:
            logging(f"Remove %s from database", non_existing_path)
            img_db.remove(non_existing_path)
        logging.info("Done updating database")


def _read_photo(image_path: str, mtime: float):
    photo = ExifPhotoInformation(image_path)
    return (photo, mtime)
