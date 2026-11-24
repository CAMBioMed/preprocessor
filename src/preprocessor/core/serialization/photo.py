"""Photo metadata models for project files."""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, Field, JsonValue, PositiveInt, field_validator

from preprocessor.core.serialization.crop_params import CropParams
from preprocessor.core.serialization.lens_correction_params import LensCorrectionParams
from preprocessor.core.serialization.metadata import parse_date, parse_str
from preprocessor.core.serialization.point2d import Point2D
from preprocessor.core.serialization.project_path import ProjectPath
from preprocessor.core.serialization.ruler_params import RulerParams

type PhotoParam = CropParams | LensCorrectionParams | RulerParams
"""A processing parameter stored with a photo."""


class Photo(BaseModel, validate_assignment=True):
    """A source photo, its metadata, and its annotations."""

    model_config = ConfigDict(
        extra="forbid",
    )

    id: str = Field(
        description="The unique identifier of the photo.",
    )
    image_path: ProjectPath = Field(
        description="The path to the image file.",
    )
    width: PositiveInt = Field(
        description="The width of the photo, in pixels.",
    )
    height: PositiveInt = Field(
        description="The height of the photo, in pixels.",
    )
    metadata: dict[str, JsonValue] = Field(
        description="The associated metadata.",
    )
    quadrat: tuple[Point2D, Point2D, Point2D, Point2D] | None = Field(
        description=(
            "Optional quadrat corners ordered top-left, top-right, bottom-right, bottom-left "
            "as image-pixel (x, y) coordinates measured from the top-left origin, with x "
            "increasing rightward and y increasing downward."
        ),
        default=None,
    )

    params: list[PhotoParam] = Field(
        description="The processing parameters associated with the photo.",
        default_factory=list,
    )

    @field_validator("id")
    @classmethod
    def validate_photo_id(cls, value: str) -> str:
        """Normalize a photo identifier to lowercase."""

        # Validate that the value is non-blank
        if not value.strip():
            msg = "Photo ID must be non-blank."
            raise ValueError(msg)
        return value.lower()

    def determine_filename(self, group_idx: int) -> str:
        """
        Determines the export filename of the photo with this metadata.

        :param group_idx: The index of the photo in its group (e.g. in its site, area, year, season, transect).
        :return: The export filename of the photo.
        """

        filename: str | None = parse_str(self.metadata.get("filename"))

        if filename is not None:
            return filename

        partner: str | None = parse_str(self.metadata.get("partner"))
        area: str | None = parse_str(self.metadata.get("area"))
        site: str | None = parse_str(self.metadata.get("site"))
        date = parse_date(self.metadata.get("date"))
        date_str: str | None = date.isoformat() if date is not None else None
        year: str | None = str(date.year) if date is not None else None
        season: str | None = parse_str(self.metadata.get("season"))
        transect: str | None = parse_str(self.metadata.get("transect"))
        idx: str | None = f"{group_idx:03d}"
        ext: str = self.image_path.suffix.lower() if self.image_path.suffix else ".jpg"

        # Generate _ separated string of all the parts that are not None
        parts = [p for p in [partner, area, site, year, season, transect, date_str, idx] if p is not None]
        return "_".join(parts) + ext

    @staticmethod
    def group_photos(photos: Iterable[Photo]) -> list[list[Photo]]:
        """Group photos with the same site, area, year, season, and transect."""

        groups: dict[tuple[str | None, str | None, str | None, str | None, str | None], list[Photo]] = {}
        for photo in photos:
            metadata = photo.metadata
            site: str | None = parse_str(metadata.get("site"))
            area: str | None = parse_str(metadata.get("area"))
            date = parse_date(metadata.get("date"))
            season: str | None = parse_str(metadata.get("season"))
            transect: str | None = parse_str(metadata.get("transect"))
            year = str(date.year) if date is not None else None
            key = (
                site,
                area,
                year,
                season,
                transect,
            )
            if key not in groups:
                groups[key] = []
            groups[key].append(photo)
        return list(groups.values())


def get_crop_param(photo: Photo) -> CropParams | None:
    """
    Return the last crop parameter associated with a photo, if any.

    :param photo: The photo whose parameters should be searched.
    :return: The last crop parameter, or None if the photo has no crop parameter.
    """

    for param in reversed(photo.params):
        if isinstance(param, CropParams):
            return param
    return None


def set_crop_param(photo: Photo, crop_param: CropParams) -> None:
    """
    Replace the last crop parameter associated with a photo or append one.

    :param photo: The photo whose parameters should be updated.
    :param crop_param: The crop parameter to replace or append.
    """

    for index in range(len(photo.params) - 1, -1, -1):
        if isinstance(photo.params[index], CropParams):
            photo.params[index] = crop_param
            return
    photo.params.append(crop_param)


def get_ruler_param(photo: Photo) -> RulerParams | None:
    """
    Return the last ruler parameter associated with a photo, if any.

    :param photo: The photo whose parameters should be searched.
    :return: The last ruler parameter, or None if the photo has no ruler parameter.
    """

    for param in reversed(photo.params):
        if isinstance(param, RulerParams):
            return param
    return None


def set_ruler_param(photo: Photo, ruler_param: RulerParams) -> None:
    """
    Replace the last ruler parameter associated with a photo or append one.

    :param photo: The photo whose parameters should be updated.
    :param ruler_param: The ruler parameter to replace or append.
    """

    for index in range(len(photo.params) - 1, -1, -1):
        if isinstance(photo.params[index], RulerParams):
            photo.params[index] = ruler_param
            return
    photo.params.append(ruler_param)


def get_lens_correction_params(photo: Photo) -> LensCorrectionParams | None:
    """
    Return the last lens-correction parameter associated with a photo, if any.

    :param photo: The photo whose parameters should be searched.
    :return: The last lens-correction parameter, or None if the photo has none.
    """

    for param in reversed(photo.params):
        if isinstance(param, LensCorrectionParams):
            return param
    return None


def set_lens_correction_params(photo: Photo, lens_correction_params: LensCorrectionParams) -> None:
    """
    Replace the last lens-correction parameter or append one.

    :param photo: The photo whose parameters should be updated.
    :param lens_correction_params: The lens-correction parameter to replace or append.
    """

    for index in range(len(photo.params) - 1, -1, -1):
        if isinstance(photo.params[index], LensCorrectionParams):
            photo.params[index] = lens_correction_params
            return
    photo.params.append(lens_correction_params)
