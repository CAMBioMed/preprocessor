from pydantic import BaseModel, ConfigDict

from datetime import datetime
from typing import Any, ClassVar

from pydantic import BaseModel, field_validator, Field

class MetadataData(BaseModel, validate_assignment=True):
    """The metadata for a single photo in the project."""

    model_config = ConfigDict(
        extra="forbid",
    )

    filename: str | None = Field(max_length=200, default=None)
    """The export filename of the photo, or None if not set."""
    date: datetime | None = Field(default=None)
    """The date the photo was taken, or None if not set."""
    partner: str | None = Field(max_length=50, default=None)
    """The partner name for the photo, or None if not set."""
    area: str | None = Field(max_length=50, default=None)
    """The area name for the photo, or None if not set."""
    site: str | None = Field(max_length=50, default=None)
    """The site name for the photo, or None if not set."""
    season: str | None = Field(max_length=50, default=None)
    """The season name for the photo, or None if not set."""
    transect: str | None = Field(max_length=50, default=None)
    """The transect information for the photo, or None if not set."""
    height: int | None = Field(ge=0, default=None)
    """The number of centimeters of substrate the image covers, or None if not set."""
    latitude: float | None = Field(ge=-90.0, le=90.0, default=None)
    """The latitude information, or None if not set."""
    longitude: float | None = Field(ge=-180.0, le=180.0, default=None)
    """The longitude information, or None if not set."""
    depth: str | None = Field(max_length=45, default=None)
    """The depth information, or None if not set."""
    camera: str | None = Field(max_length=200, default=None)
    """The camera information, or None if not set."""
    photographer: str | None = Field(max_length=45, default=None)
    """The photographer information, or None if not set."""
    water_quality: str | None = Field(max_length=45, default=None)
    """The water quality information, or None if not set."""
    strobes: str | None = Field(max_length=200, default=None)
    """The strobes information, or None if not set."""
    framing: str | None = Field(max_length=200, default=None)
    """The framing information, or None if not set."""
    white_balance_card: str | None = Field(max_length=200, default=None)
    """The white balance card information, or None if not set."""
    comments: str | None = Field(max_length=1000, default=None)
    """Any additional comments, or None if not set."""

    @field_validator("*", mode="before")
    @classmethod
    def _validate_str_fields(cls: type["MetadataData"], v: Any) -> Any:  # noqa: ANN401
        if v is not None and isinstance(v, str):
            if not v.strip():
                return None
            return v.strip()
        return v