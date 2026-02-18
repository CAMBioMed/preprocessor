from PySide6.QtGui import QIcon, QPixmap
from importlib import resources as _importlib_resources


def icon_from_resource(relpath: str) -> QIcon:
    """Load an icon from package resources under preprocessor/<relpath>."""
    data = _importlib_resources.files("preprocessor").joinpath(relpath).read_bytes()
    pm = QPixmap()
    pm.loadFromData(data)
    return QIcon(pm)
