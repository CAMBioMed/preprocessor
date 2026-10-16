"""Behavior contract for the disposable thumbnail cache."""

import logging
import os
import shutil
from pathlib import Path

import pytest
from PIL import Image
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from preprocessor.gui.thumbnail_cache import ThumbnailCache


@pytest.fixture(autouse=True)
def ensure_qapp(qapp: QApplication) -> QApplication:
    """Ensure QPixmap operations have a QApplication."""
    return qapp


_THUMBNAIL_SIZE = QSize(12, 12)


def _write_png(path: Path, color: str, size: tuple[int, int] = (40, 20)) -> None:
    """Write a solid-color PNG fixture to ``path``."""
    Image.new("RGB", size, color).save(path)


def _assert_pixmap_color(pixmap: QPixmap, color: str) -> None:
    """Assert that a returned thumbnail's central pixel has ``color``."""
    image = pixmap.toImage()
    assert image.pixelColor(image.width() // 2, image.height() // 2).name() == color


def _cache_png(cache_dir: Path) -> Path:
    """Return the sole PNG cache entry in ``cache_dir``."""
    cache_paths = list(cache_dir.glob("*.png"))
    assert len(cache_paths) == 1
    return cache_paths[0]


def _make_source_newer(source: Path, cache_path: Path) -> None:
    """Set ``source`` newer than ``cache_path`` with filesystem-resolution headroom."""
    source_mtime_ns = min(source.stat().st_mtime_ns, cache_path.stat().st_mtime_ns) - 4_000_000_000
    cache_mtime_ns = source_mtime_ns - 4_000_000_000
    os.utime(cache_path, ns=(cache_path.stat().st_atime_ns, cache_mtime_ns))
    os.utime(source, ns=(source.stat().st_atime_ns, source_mtime_ns))


def test_should_create_project_cache_and_return_proportional_thumbnail_when_first_requested(tmp_path: Path) -> None:
    """Should create cache artifacts and return a scaled thumbnail when first requested."""
    # Arrange
    source = tmp_path / "red.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")

    # Act
    thumbnail = ThumbnailCache(project_file).get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    assert thumbnail.size() == QSize(12, 6)
    _assert_pixmap_color(thumbnail, "#ff0000")
    cache_dir = tmp_path / ".cache"
    assert cache_dir.is_dir()
    assert (cache_dir / ".gitignore").read_text(encoding="utf-8") == "*\n"
    assert _cache_png(cache_dir).suffix == ".png"


def test_should_reuse_fresh_cache_entry_when_source_is_not_newer(tmp_path: Path) -> None:
    """Should return the fresh cached thumbnail when its source is not newer."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_path = _cache_png(tmp_path / ".cache")
    cache_mtime_ns = cache_path.stat().st_mtime_ns
    _write_png(source, "blue")
    os.utime(source, ns=(source.stat().st_atime_ns, cache_mtime_ns))

    # Act
    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#ff0000")
    assert cache_path.stat().st_mtime_ns == cache_mtime_ns


def test_should_regenerate_cache_entry_when_source_is_newer(tmp_path: Path) -> None:
    """Should replace a cache entry when its source has a newer timestamp."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_path = _cache_png(tmp_path / ".cache")
    _write_png(source, "blue")
    _make_source_newer(source, cache_path)

    # Act

    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#0000ff")
    _assert_pixmap_color(QPixmap(str(cache_path)), "#0000ff")
    assert cache_path.stat().st_mtime_ns >= source.stat().st_mtime_ns


def test_should_rebuild_cache_directory_without_warning_when_directory_is_deleted(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Should recreate the cache directory without warning when it was deleted."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_dir = tmp_path / ".cache"
    shutil.rmtree(cache_dir)
    caplog.clear()

    # Act
    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    assert cache_dir.is_dir()
    assert (cache_dir / ".gitignore").read_text(encoding="utf-8") == "*\n"
    assert _cache_png(cache_dir).exists()
    assert not [record for record in caplog.records if record.levelno >= logging.WARNING]


def test_should_bypass_cache_without_warning_when_project_is_unsaved(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Should return a source thumbnail without warning when the project is unsaved."""
    # Arrange
    source = tmp_path / "photo.png"
    _write_png(source, "blue")
    caplog.clear()

    # Act
    thumbnail = ThumbnailCache(None).get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#0000ff")
    assert not (tmp_path / ".cache").exists()
    assert not [record for record in caplog.records if record.levelno >= logging.WARNING]


def test_should_warn_and_return_source_thumbnail_when_regular_file_blocks_cache_directory(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Should bypass caching with a warning when a regular file blocks the cache directory."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache_path = tmp_path / ".cache"
    cache_path.write_text("blocked", encoding="utf-8")
    caplog.clear()

    # Act
    thumbnail = ThumbnailCache(project_file).get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#ff0000")
    assert "directory creation" in caplog.text
    assert str(cache_path) in caplog.text


def test_should_warn_and_regenerate_from_source_when_cache_png_is_corrupt(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Should warn and regenerate a thumbnail when a cache PNG is corrupt."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_path = _cache_png(tmp_path / ".cache")
    cache_path.write_bytes(b"not a png")
    os.utime(cache_path, ns=(cache_path.stat().st_atime_ns, source.stat().st_mtime_ns))
    caplog.clear()

    # Act
    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#ff0000")
    assert "file read" in caplog.text
    assert str(cache_path) in caplog.text


def test_should_return_none_without_cache_artifacts_when_source_is_invalid(tmp_path: Path) -> None:
    """Should return ``None`` without cache artifacts when the source image is invalid."""
    # Arrange
    source = tmp_path / "invalid.png"
    project_file = tmp_path / "project.pbproj"
    source.write_text("not an image", encoding="utf-8")

    # Act
    thumbnail = ThumbnailCache(project_file).get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is None
    assert not (tmp_path / ".cache").exists()


def test_should_replace_blocking_cache_entry_with_regenerated_thumbnail_when_initial_write_fails(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Should replace a blocking cache entry when the initial thumbnail write fails."""
    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_path = _cache_png(tmp_path / ".cache")
    cache_path.unlink()
    cache_path.mkdir()
    caplog.clear()

    # Act
    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#ff0000")
    assert cache_path.is_file()
    _assert_pixmap_color(QPixmap(str(cache_path)), "#ff0000")
    assert "file read" in caplog.text
    assert str(cache_path) in caplog.text


def test_should_warn_and_return_thumbnail_without_storing_when_cache_entry_cannot_be_replaced(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Should warn and return a thumbnail without storing it when a cache entry cannot be replaced."""

    # Arrange
    source = tmp_path / "photo.png"
    project_file = tmp_path / "project.pbproj"
    _write_png(source, "red")
    cache = ThumbnailCache(project_file)
    cache.get_thumbnail(source, _THUMBNAIL_SIZE)
    cache_dir = tmp_path / ".cache"
    cache_path = _cache_png(cache_dir)
    cache_path.unlink()
    cache_path.mkdir()

    def _raise_permission_error(_: Path) -> None:
        raise PermissionError("access denied")

    monkeypatch.setattr(ThumbnailCache, "_remove_cache_entry", staticmethod(_raise_permission_error))

    # Act
    thumbnail = cache.get_thumbnail(source, _THUMBNAIL_SIZE)

    # Assert
    assert thumbnail is not None
    _assert_pixmap_color(thumbnail, "#ff0000")
    assert cache_path.is_dir()
    assert "file write" in caplog.text
    assert str(cache_path) in caplog.text
