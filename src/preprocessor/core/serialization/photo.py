"""Photo metadata models for project files."""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, Field, JsonValue, PositiveInt, field_validator

from preprocessor.core.serialization import Point2D, ProjectPath
from preprocessor.core.serialization.metadata import parse_date, parse_str


class Photo(BaseModel, validate_assignment=True):
    """A source photo, its metadata, and its annotations."""

    model_config = ConfigDict(
        extra="forbid",
    )

    id: str = Field(
        description="The unique identifier of the photo.",
    )
    original_filename: ProjectPath = Field(
        description="The path to the original image file.",
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
        ext: str = self.original_filename.suffix.lower() if self.original_filename.suffix else ".jpg"

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

