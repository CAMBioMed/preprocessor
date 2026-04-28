from datetime import datetime
from typing import Any

from PySide6.QtCore import Signal

from preprocessor.core.model import MetadataData
from preprocessor.gui.model._QModel import QModel




class MetadataModel(QModel[MetadataData]):
    """The model for the metadata of a photo."""

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
