from datetime import datetime
from typing import Any, ClassVar

from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator, Field

from preprocessor.model.qmodel import QModel


class MetadataData(BaseModel, validate_assignment=True):
    """The metadata for a single photo in the project."""

    # Serialization JSON version
    SERIAL_VERSION: ClassVar[int] = 1

    filename: str | None = Field(max_length=200, default=None)
    """The filename of the photo, or None if not set."""
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
    height: int | None = Field(gt=0, default=None)
    """The number of centimeters of substrate the image covers, or None if not set."""
    latitude: float | None = Field(gt=-90.0, lt=90.0, default=None)
    """The latitude information, or None if not set."""
    longitude: float | None = Field(gt=-180.0, lt=180.0, default=None)
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


class MetadataModel(QModel[MetadataData]):
    on_filename_changed: Signal = Signal(object)
    on_date_changed: Signal = Signal(object)
    on_partner_changed: Signal = Signal(object)
    on_area_changed: Signal = Signal(object)
    on_site_changed: Signal = Signal(object)
    on_season_changed: Signal = Signal(object)
    on_transect_changed: Signal = Signal(object)
    on_height_changed: Signal = Signal(object)
    on_latitude_changed: Signal = Signal(object)
    on_longitude_changed: Signal = Signal(object)
    on_depth_changed: Signal = Signal(object)
    on_camera_changed: Signal = Signal(object)
    on_photographer_changed: Signal = Signal(object)
    on_water_quality_changed: Signal = Signal(object)
    on_strobes_changed: Signal = Signal(object)
    on_framing_changed: Signal = Signal(object)
    on_white_balance_card_changed: Signal = Signal(object)
    on_comments_changed: Signal = Signal(object)

    def __init__(self, data: MetadataData | dict[str, Any] | None = None) -> None:
        super().__init__(model_cls=MetadataData, data=data)

    @property
    def filename(self) -> str | None:
        return self._data.filename

    @filename.setter
    def filename(self, value: str | None) -> None:
        self._set_field("filename", value)

    @property
    def date(self) -> datetime | None:
        return self._data.date

    @date.setter
    def date(self, value: datetime | None) -> None:
        self._set_field("date", value)

    @property
    def partner(self) -> str | None:
        return self._data.partner

    @partner.setter
    def partner(self, value: str | None) -> None:
        self._set_field("partner", value)

    @property
    def area(self) -> str | None:
        return self._data.area

    @area.setter
    def area(self, value: str | None) -> None:
        self._set_field("area", value)

    @property
    def site(self) -> str | None:
        return self._data.site

    @site.setter
    def site(self, value: str | None) -> None:
        self._set_field("site", value)

    @property
    def season(self) -> str | None:
        return self._data.season

    @season.setter
    def season(self, value: str | None) -> None:
        self._set_field("season", value)

    @property
    def transect(self) -> str | None:
        return self._data.transect

    @transect.setter
    def transect(self, value: str | None) -> None:
        self._set_field("transect", value)

    @property
    def height(self) -> int | None:
        return self._data.height

    @height.setter
    def height(self, value: int | None) -> None:
        self._set_field("height", value)

    @property
    def latitude(self) -> float | None:
        return self._data.latitude

    @latitude.setter
    def latitude(self, value: float | None) -> None:
        self._set_field("latitude", value)

    @property
    def longitude(self) -> float | None:
        return self._data.longitude

    @longitude.setter
    def longitude(self, value: float | None) -> None:
        self._set_field("longitude", value)

    @property
    def depth(self) -> str | None:
        return self._data.depth

    @depth.setter
    def depth(self, value: str | None) -> None:
        self._set_field("depth", value)

    @property
    def camera(self) -> str | None:
        return self._data.camera

    @camera.setter
    def camera(self, value: str | None) -> None:
        self._set_field("camera", value)

    @property
    def photographer(self) -> str | None:
        return self._data.photographer

    @photographer.setter
    def photographer(self, value: str | None) -> None:
        self._set_field("photographer", value)

    @property
    def water_quality(self) -> str | None:
        return self._data.water_quality

    @water_quality.setter
    def water_quality(self, value: str | None) -> None:
        self._set_field("water_quality", value)

    @property
    def strobes(self) -> str | None:
        return self._data.strobes

    @strobes.setter
    def strobes(self, value: str | None) -> None:
        self._set_field("strobes", value)

    @property
    def framing(self) -> str | None:
        return self._data.framing

    @framing.setter
    def framing(self, value: str | None) -> None:
        self._set_field("framing", value)

    @property
    def white_balance_card(self) -> str | None:
        return self._data.white_balance_card

    @white_balance_card.setter
    def white_balance_card(self, value: str | None) -> None:
        self._set_field("white_balance_card", value)

    @property
    def comments(self) -> str | None:
        return self._data.comments

    @comments.setter
    def comments(self, value: str | None) -> None:
        self._set_field("comments", value)
