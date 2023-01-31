import json
import os
import subprocess
from datetime import datetime


class ExifPhotoInformation:
    """Photo with exif information"""

    def __init__(self, image_path: str) -> None:
        self._photo_path = image_path

        self._exif_data = read_exif_data(image_path)

    @property
    def path(self) -> str:
        """Get the path to the photo"""
        return self._photo_path

    @property
    def filename(self) -> str:
        """Get filename of photo"""
        return os.path.basename(self._photo_path)

    @property
    def dirname(self) -> str:
        """Get directory name where photo is stored"""
        return os.path.dirname(self._photo_path)

    @property
    def date_time(self) -> datetime:
        """Get the date and time of the photo"""
        exif_datetime = self._exif_data["DateTimeOriginal"].split(" ")
        datetime_object = datetime.fromisoformat(
            exif_datetime[0].replace(":", "-") + " " + exif_datetime[1]
        )
        if datetime_object.year == 2021 and datetime_object.month == 5:
            # compensate for invalid camera date
            datetime_object = datetime_object.replace(year=2022)

        return datetime_object

    @property
    def focal_length(self) -> str:
        """Return focal length rounded to the nearest integer in mm"""
        return self._exif_data["FocalLength"]

    @property
    def exposure(self) -> str:
        """exposure of photo"""
        return self._exif_data["ExposureTime"]

    @property
    def aperture(self) -> str:
        """aperture used"""
        return "f/" + str(self._exif_data["Aperture"])

    @property
    def iso(self) -> str:
        """iso"""
        return "ISO " + str(self._exif_data["ISO"])

    @property
    def lens(self) -> str:
        """Return the lens information"""
        return self._exif_data["Lens"]

    @property
    def tags(self) -> list:
        """Return hierarchical tags. If no tags exists, an
        empty list is returned.
        """
        if not "HierarchicalSubject" in self._exif_data:
            return []

        tag_list = self._exif_data["HierarchicalSubject"]
        # exiftool returns a string instead of a list
        # if we have only one tag assigned
        if isinstance(tag_list, str):
            tag_list = [tag_list]

        return [
            tag.replace("|", " :: ") for tag in tag_list if not tag.startswith("export")
        ]

    @property
    def abs_image_path(self) -> str:
        """Return the absolute path of the image"""
        return os.path.abspath(self._photo_path)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ExifPhotoInformation):
            return False

        return self.abs_image_path == __o.abs_image_path


class ExifReadError(Exception):
    def __init__(self, message: str, reason: str = "None") -> None:
        super().__init__([message, reason])


def read_exif_data(filepath: str) -> dict:
    """
    Read EXIF information as dict
    """

    result = subprocess.run(
        ["exiftool", "-j", filepath], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise ExifReadError("Error reading EXIF information " + filepath, result.stderr)
    exif_json = json.loads(result.stdout)
    return exif_json[0]
