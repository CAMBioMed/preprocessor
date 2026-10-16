"""Thumbnail dock integration contract for the thumbnail cache."""

import os
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from pytestqt.qtbot import QtBot

from preprocessor.core.model import PhotoData
from preprocessor.gui.model import QPhotoModel
from preprocessor.gui.thumbnail_dock_widget import ThumbnailDockWidget


def test_should_refresh_retained_icon_and_cache_when_source_becomes_newer(qtbot: QtBot, tmp_path: Path) -> None:
    """Should refresh a retained icon and cache entry when its source becomes newer."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    Image.new("RGB", (40, 20), "red").save(source)
    photo = QPhotoModel(PhotoData(image_id="photo", original_filename=source))
    dock = ThumbnailDockWidget()
    qtbot.addWidget(dock)
    dock.update_thumbnails([photo], project_file)
    item = dock.ui.thumbnailListWidget.item(0)
    assert item is not None
    cache_path = next((tmp_path / ".cache").glob("*.png"))
    Image.new("RGB", (40, 20), "blue").save(source)
    os.utime(source, ns=(source.stat().st_atime_ns, cache_path.stat().st_mtime_ns + 1))

    # Act
    dock.update_thumbnails([photo], project_file)

    # Assert
    assert dock.ui.thumbnailListWidget.item(0) is item
    icon = item.icon().pixmap(QSize(120, 120)).toImage()
    assert icon.pixelColor(icon.width() // 2, icon.height() // 2).name() == "#0000ff"
    cache = QPixmap(str(cache_path)).toImage()
    assert cache.pixelColor(cache.width() // 2, cache.height() // 2).name() == "#0000ff"
