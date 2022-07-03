"""
Read EXIF information using exiftool
"""

import subprocess
import json


class ExifReadError(Exception):
    def __init__(self, message: str, reason: str = "None") -> None:
        super().__init__([message, reason])


def read_exif_data(filepath: str) -> dict:
    """
    Read EXIF information as dict
    """

    result = subprocess.run(
        ['exiftool', '-j',
         filepath],
        capture_output=True,
        text=True,
        check=False)
    if result.returncode != 0:
        raise ExifReadError(
            "Error reading EXIF information "+filepath, result.stderr)
    exif_json = json.loads(result.stdout)
    return exif_json[0]
