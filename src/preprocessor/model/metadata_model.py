import datetime
from typing import Any, ClassVar

from PySide6.QtCore import Signal
from pydantic import BaseModel, field_validator

from preprocessor.model.qmodel import QModel


class MetadataData(BaseModel):
    """The metadata for a single photo in the project."""

    # Serialization JSON version
    SERIAL_VERSION: ClassVar[int] = 1

    date: datetime.date | None = None
    """The date the photo was taken, or None if not set."""
    partner: str | None = None
    """The partner name for the photo, or None if not set."""
    area: str | None = None
    """The area name for the photo, or None if not set."""
    site: str | None = None
    """The site name for the photo, or None if not set."""
    season: str | None = None
    """The season name for the photo, or None if not set."""
    transect: str | None = None
    """The transect information for the photo, or None if not set."""
    height: str | None = None
    """The height information, or None if not set."""
    latitude: str | None = None
    """The latitude information, or None if not set."""
    longitude: str | None = None
    """The longitude information, or None if not set."""
    depth: str | None = None
    """The depth information, or None if not set."""
    camera: str | None = None
    """The camera information, or None if not set."""
    photographer: str | None = None
    """The photographer information, or None if not set."""
    water_quality: str | None = None
    """The water quality information, or None if not set."""
    strobes: str | None = None
    """The strobes information, or None if not set."""
    framing: str | None = None
    """The framing information, or None if not set."""
    white_balance_card: str | None = None
    """The white balance card information, or None if not set."""
    comments: str | None = None
    """Any additional comments, or None if not set."""

    @field_validator('*', mode='after')
    @classmethod
    def _validate_str_fields(cls, v: Any) -> Any:
        if v is not None and isinstance(v, str):
            if not v.strip():
                return None
            return v.strip()
        return v

class MetadataModel(QModel[MetadataData]):
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
    def date(self) -> datetime.date | None:
        return self._data.date

    @date.setter
    def date(self, value: datetime.date | None) -> None:
        self._data.date = value
        self.on_date_changed.emit(value)

    @property
    def partner(self) -> str | None:
        return self._data.partner

    @partner.setter
    def partner(self, value: str | None) -> None:
        self._data.partner = value
        self.on_partner_changed.emit(value)

    @property
    def area(self) -> str | None:
        return self._data.area

    @area.setter
    def area(self, value: str | None) -> None:
        self._data.area = value
        self.on_area_changed.emit(value)

    @property
    def site(self) -> str | None:
        return self._data.site

    @site.setter
    def site(self, value: str | None) -> None:
        self._data.site = value
        self.on_site_changed.emit(value)

    @property
    def season(self) -> str | None:
        return self._data.season

    @season.setter
    def season(self, value: str | None) -> None:
        self._data.season = value
        self.on_season_changed.emit(value)

    @property
    def transect(self) -> str | None:
        return self._data.transect

    @transect.setter
    def transect(self, value: str | None) -> None:
        self._data.transect = value
        self.on_transect_changed.emit(value)

    @property
    def height(self) -> str | None:
        return self._data.height

    @height.setter
    def height(self, value: str | None) -> None:
        self._data.height = value
        self.on_height_changed.emit(value)

    @property
    def latitude(self) -> str | None:
        return self._data.latitude

    @latitude.setter
    def latitude(self, value: str | None) -> None:
        self._data.latitude = value
        self.on_latitude_changed.emit(value)

    @property
    def longitude(self) -> str | None:
        return self._data.longitude

    @longitude.setter
    def longitude(self, value: str | None) -> None:
        self._data.longitude = value
        self.on_longitude_changed.emit(value)

    @property
    def depth(self) -> str | None:
        return self._data.depth

    @depth.setter
    def depth(self, value: str | None) -> None:
        self._data.depth = value
        self.on_depth_changed.emit(value)

    @property
    def camera(self) -> str | None:
        return self._data.camera

    @camera.setter
    def camera(self, value: str | None) -> None:
        self._data.camera = value
        self.on_camera_changed.emit(value)

    @property
    def photographer(self) -> str | None:
        return self._data.photographer

    @photographer.setter
    def photographer(self, value: str | None) -> None:
        self._data.photographer = value
        self.on_photographer_changed.emit(value)

    @property
    def water_quality(self) -> str | None:
        return self._data.water_quality

    @water_quality.setter
    def water_quality(self, value: str | None) -> None:
        self._data.water_quality = value
        self.on_water_quality_changed.emit(value)

    @property
    def strobes(self) -> str | None:
        return self._data.strobes

    @strobes.setter
    def strobes(self, value: str | None) -> None:
        self._data.strobes = value
        self.on_strobes_changed.emit(value)

    @property
    def framing(self) -> str | None:
        return self._data.framing

    @framing.setter
    def framing(self, value: str | None) -> None:
        self._data.framing = value
        self.on_framing_changed.emit(value)

    @property
    def white_balance_card(self) -> str | None:
        return self._data.white_balance_card

    @white_balance_card.setter
    def white_balance_card(self, value: str | None) -> None:
        self._data.white_balance_card = value
        self.on_white_balance_card_changed.emit(value)

    @property
    def comments(self) -> str | None:
        return self._data.comments

    @comments.setter
    def comments(self, value: str | None) -> None:
        self._data.comments = value
        self.on_comments_changed.emit(value)
