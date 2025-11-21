from enum import Enum

from PySide6.QtCore import QObject, Signal

from preprocessor.gui.properties_dock_model import PropertiesDockModel


class ViewMode(Enum):
    ORIGINAL = "Original"
    PROCESSED = "Processed"
    CONTOURS = "Contours"
    LINES = "Lines"
    RECTANGLES = "Rectangles"


class MainWindowModel(QObject):
    on_changed: Signal = Signal()

    _properties_model: PropertiesDockModel = PropertiesDockModel()
    on_properties_model_changed: Signal = Signal(PropertiesDockModel)

    def __init__(self) -> None:
        super().__init__()
        self._properties_model.on_changed.connect(self._handle_properties_model_changed)

    def _handle_properties_model_changed(self) -> None:
        self.on_properties_model_changed.emit(self._properties_model)
        self.on_changed.emit()

    _image_path: str | None = None
    on_image_path_changed: Signal = Signal(str)

    @property
    def image_path(self) -> str | None:
        return self._image_path

    @image_path.setter
    def image_path(self, path: str | None) -> None:
        if self._image_path != path:
            self._image_path = path
            # FIXME: Will this work if the path is None?
            self.on_image_path_changed.emit(path)
            self.on_changed.emit()

    _view_mode: ViewMode = ViewMode.PROCESSED
    on_view_mode_changed: Signal = Signal(ViewMode)

    @property
    def view_mode(self) -> ViewMode:
        return self._view_mode

    @view_mode.setter
    def view_mode(self, mode: ViewMode) -> None:
        if self._view_mode != mode:
            self._view_mode = mode
            self.on_view_mode_changed.emit(mode)
            self.on_changed.emit()

    _view_show_debug: bool = False
    on_view_show_debug_changed: Signal = Signal(bool)

    @property
    def view_show_debug(self) -> bool:
        return self._view_show_debug

    @view_show_debug.setter
    def view_show_debug(self, show: bool) -> None:
        if self._view_show_debug != show:
            self._view_show_debug = show
            self.on_view_show_debug_changed.emit(show)
            self.on_changed.emit()
