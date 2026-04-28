from datetime import datetime, UTC

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QIcon, QPixmap
from importlib import resources as _importlib_resources

from PySide6.QtWidgets import QFileDialog
from _pytest.monkeypatch import MonkeyPatch


def icon_from_resource(relpath: str) -> QIcon:
    """Load an icon from package resources under preprocessor/<relpath>."""
    data = _importlib_resources.files("preprocessor").joinpath(relpath).read_bytes()
    pm = QPixmap()
    pm.loadFromData(data)
    return QIcon(pm)


def _dt_to_qdatetime(dt: datetime | None) -> QDateTime:
    """Convert a Python datetime (naive or tz-aware) to a QDateTime."""
    if dt is None:
        return QDateTime.currentDateTime()
    # convert to seconds since epoch (UTC for aware datetimes)
    ts = dt.timestamp() if dt.tzinfo is None else dt.astimezone(UTC).timestamp()
    return QDateTime.fromMSecsSinceEpoch(int(ts * 1000))


def patch_getOpenFileName_dialog(result: str, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda parent, title, directory, filter: (result, "Stub (*.stub)"),
    )

def patch_getOpenFileNames_dialog(result: list[str], monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda parent, title, directory, filter: (result, "Stub (*.stub)"),
    )

def patch_getSaveFileName_dialog(result: str, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda parent, title, directory, filter: (result, "Stub (*.stub)"),
    )