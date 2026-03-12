import copy
from datetime import date, datetime
from pathlib import Path
from typing import Any

import exifread


def extract_exif_data(path: Path) -> dict[str, Any]:
    """
    Extracts EXIF data from the given image file and returns it as a dictionary.
    The keys are human-readable tag names where possible,
    and the values are converted if possible.
    """

    # https://exiftool.org/TagNames/EXIF.html

    tags: dict[str, Any] = {}
    with open(path, "rb") as file_handle:

        # Return Exif tags
        tags = exifread.process_file(file_handle, builtin_types = True)

    result: dict[str, Any] = copy.deepcopy(tags)

    # Date
    datetime_tag: str | None = tags.get("EXIF DateTimeOriginal") or tags.get("EXIF DateTimeDigitized") or tags.get("Image DateTime")
    offset_tag: str | None = tags.get("EXIF OffsetTimeOriginal") or tags.get("EXIF OffsetTimeDigitized") or tags.get("EXIF OffsetTime")
    subsec_tag: str | None = tags.get("EXIF SubSecTimeOriginal") or tags.get("EXIF SubSecTimeDigitized") or tags.get("EXIF SubSecTime")
    if datetime_tag:
        result["DateTime"] = _parse_datetime(
            datetime_tag,
            offset_tag if offset_tag else None,
            subsec_tag if subsec_tag else None,
        )

    # Photographer
    photographer: str | None = tags.get("Image Artist") or tags.get("Image Copyright")
    if photographer:
        result["Photographer"] = photographer

    # Camera
    model: str | None = tags.get("Image Model")
    make: str | None = tags.get("Image Make")
    camera = None
    if make and model:
        camera = f"{make} {model}"
    elif model:
        camera = model
    elif make:
        camera = make
    if camera:
        result["Camera"] = camera

    # Comments
    comments: Any = tags.get("Image ImageDescription") or tags.get("EXIF UserComment")
    if comments:
        result["Comments"] = comments

    # GPS
    # https://exiftool.org/TagNames/GPS.html
    # In degrees, minutes, seconds format, as a list of three floats
    latitude_nums: list[float] | None = tags.get("GPS GPSLatitude")
    longitude_nums: list[float] | None = tags.get("GPS GPSLongitude")
    latitude_sign: float = 1.0 if tags.get("GPS GPSLatitudeRef") in ['N', None] else -1.0
    longitude_sign: float = 1.0 if tags.get("GPS GPSLongitudeRef") in ['E', None] else -1.0
    # As a single number
    latitude = tags.get("GPS GPSLatitudeRef") and latitude_nums and _dms_to_decimal(latitude_nums, latitude_sign)
    longitude = tags.get("GPS GPSLongitudeRef") and longitude_nums and _dms_to_decimal(longitude_nums, longitude_sign)
    if latitude:
        result["Latitude"] = latitude
    if longitude:
        result["Longitude"] = longitude

    return result


def _dms_to_decimal(dms: list[float], sign: float) -> float:
    """Convert degrees, minutes, seconds to decimal degrees, accounting for N/S/E/W."""
    degrees, minutes, seconds = dms
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    return decimal * sign

#
# def _exif_to_map(exif: Exif) -> dict[str | int, Any]:
#     """
#     Reads the EXIF data from a PIL Image
#     and returns a dictionary mapping human-readable tag names to their values.
#     """
#
#     IFD_CODE_LOOKUP = {i.value: i.name for i in ExifTags.IFD}
#     tags: dict[str | int, Any] = {}
#     for tag_id, tag_raw_value in exif.items():
#         # if the tag is an IFD block, nest into it
#         if tag_id in IFD_CODE_LOOKUP:
#             ifd_tag_name = IFD_CODE_LOOKUP[tag_id]
#             ifd_data = exif.get_ifd(tag_id).items()
#             print(f"IFD '{ifd_tag_name}' (id {tag_id}):")
#             for nested_id, nested_raw_value in ifd_data:
#                 nested_tag_name = ExifTags.GPSTAGS.get(nested_id, None) or ExifTags.TAGS.get(nested_id,
#                                                                                              None) or nested_id
#                 nested_value = _normalize_exif_value(nested_raw_value)
#                 tags[nested_tag_name] = nested_value
#                 print(f"  {nested_tag_name}: {nested_value}")
#         else:
#             tag_name = ExifTags.TAGS.get(tag_id, tag_id)
#             tag_value = _normalize_exif_value(tag_raw_value)
#             tags[tag_name] = tag_value
#             print(f"{tag_name}: {tag_value}")
#
#     return tags
#
# def _normalize_exif_value(value: Any) -> Any:
#     """Normalize EXIF values by stripping null bytes from strings."""
#     if value is None:
#         return None
#     elif isinstance(value, str):
#         return value.rstrip('\x00')
#     elif isinstance(value, bytes):
#         return value.rstrip(b'\x00')
#     return value

def _parse_datetime(datetime_str: str | None, offset_str: str | None, subsec_str: str | None) -> datetime | None:
    """Parse EXIF date strings and return a cleaned date string."""
    if datetime_str is None:
        return None
    # Format is typically 'YYYY:MM:DD HH:MM:SS'
    parts = datetime_str.split(' ')
    date_str = parts[0].replace(':', '-')
    time_str = parts[1] if len(parts) > 1 else "00:00:00"
    full_str = f"{date_str}T{time_str}.{subsec_str or '0'}{offset_str or ''}"
    return datetime.fromisoformat(full_str)