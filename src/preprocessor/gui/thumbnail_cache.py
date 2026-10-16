"""Disposable on-disk cache for project thumbnail pixmaps."""

import hashlib
import logging
import shutil
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap

_LOGGER = logging.getLogger(__name__)
_WARNING_TEMPLATE = "Thumbnail cache %s failed for %s: %s"


class ThumbnailCache:
    """Provide scaled image thumbnails backed by a disposable project cache."""

    def __init__(self, project_file: Path | None) -> None:
        """Initialize the cache adjacent to ``project_file``.

        ``None`` denotes an unsaved project and bypasses on-disk caching.
        """
        self._cache_directory = project_file.parent.resolve() / ".cache" if project_file is not None else None

    def get_thumbnail(self, image_path: Path, size: QSize) -> QPixmap | None:
        """Return a smoothly scaled pixmap from cache or ``image_path``.

        A fresh cache entry is preferred. Cache failures are logged at ``WARNING`` level
        and bypassed or regenerated. ``None`` is returned when the source image cannot
        be loaded.
        """
        if self._cache_directory is None:
            return self._load_source_thumbnail(image_path, size)

        try:
            source_mtime_ns = image_path.stat().st_mtime_ns
        except OSError:
            return self._load_source_thumbnail(image_path, size)

        cache_file = self._cache_file(image_path, size)
        if cache_file is None:
            return self._load_source_thumbnail(image_path, size)

        try:
            cache_stat = cache_file.stat()
        except FileNotFoundError:
            pass
        except OSError as error:
            self._warn("file inspection", cache_file, error)
        else:
            if cache_stat.st_mtime_ns >= source_mtime_ns:
                cached_thumbnail = self._load_cached_thumbnail(cache_file)
                if cached_thumbnail is not None:
                    return cached_thumbnail

        thumbnail = self._load_source_thumbnail(image_path, size)
        if thumbnail is None:
            return None

        if self._prepare_cache_directory():
            self._write_cache_thumbnail(cache_file, thumbnail)
        return thumbnail

    def _cache_file(self, image_path: Path, size: QSize) -> Path | None:
        """Return the cache filename for ``image_path`` and ``size``, or ``None`` on resolution failure."""
        if self._cache_directory is None:
            return None
        try:
            resolved_path = image_path.resolve()
        except OSError:
            return None
        digest = hashlib.sha256(str(resolved_path).encode("utf-8")).hexdigest()
        return self._cache_directory / f"{digest}-{size.width()}x{size.height()}.png"

    def _load_cached_thumbnail(self, cache_file: Path) -> QPixmap | None:
        """Load a valid PNG cache entry, or return ``None`` after logging its read failure."""
        try:
            with cache_file.open("rb") as file:
                is_png = file.read(8) == b"\x89PNG\r\n\x1a\n"
        except OSError as error:
            self._warn("file read", cache_file, error)
            return None

        if not is_png:
            self._warn("file read", cache_file, "expected a PNG file")
            return None

        thumbnail = QPixmap(str(cache_file))
        if thumbnail.isNull():
            self._warn("file read", cache_file, "Qt returned a null pixmap")
            return None
        return thumbnail

    def _write_cache_thumbnail(self, cache_file: Path, thumbnail: QPixmap) -> None:
        """Store ``thumbnail`` in ``cache_file``, replacing a blocking cache entry once if needed."""
        if self._save_thumbnail(cache_file, thumbnail):
            return

        try:
            self._remove_cache_entry(cache_file)
        except OSError as error:
            self._warn("file write", cache_file, f"could not remove existing cache entry: {error}")
            return

        if not self._save_thumbnail(cache_file, thumbnail):
            self._warn("file write", cache_file, "Qt failed to save PNG after replacing cache entry")

    @staticmethod
    def _save_thumbnail(cache_file: Path, thumbnail: QPixmap) -> bool:
        """Save ``thumbnail`` to ``cache_file`` as PNG, returning whether Qt reported success."""
        try:
            return thumbnail.save(str(cache_file), "PNG")
        except OSError:
            return False

    @staticmethod
    def _remove_cache_entry(cache_file: Path) -> None:
        """Remove any file-system entry at ``cache_file`` so a thumbnail write can be retried."""
        try:
            if cache_file.is_dir() and not cache_file.is_symlink():
                shutil.rmtree(cache_file)
            else:
                cache_file.unlink()
        except FileNotFoundError:
            pass

    def _load_source_thumbnail(self, image_path: Path, size: QSize) -> QPixmap | None:
        """Load ``image_path`` and return it smoothly scaled to fit ``size``, or ``None`` if unloadable."""
        source_pixmap = QPixmap(str(image_path))
        if source_pixmap.isNull():
            return None
        return source_pixmap.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def _prepare_cache_directory(self) -> bool:
        """Create the cache directory and its ignore file when the directory does not yet exist."""
        if self._cache_directory is None:
            return False
        try:
            self._cache_directory.mkdir()
        except FileExistsError as error:
            if self._cache_directory.is_dir():
                return True
            self._warn("directory creation", self._cache_directory, error)
            return False
        except OSError as error:
            self._warn("directory creation", self._cache_directory, error)
            return False

        ignore_file = self._cache_directory / ".gitignore"
        try:
            with ignore_file.open("x", encoding="utf-8") as file:
                file.write("*\n")
        except FileExistsError:
            if ignore_file.is_file():
                return True
            self._warn("ignore-file creation", ignore_file, "path is not a regular file")
            return False
        except OSError as error:
            self._warn("ignore-file creation", ignore_file, error)
            return False
        return True

    @staticmethod
    def _warn(operation: str, path: Path, error: Exception | str) -> None:
        """Log a cache failure for ``path`` without interrupting thumbnail loading."""
        _LOGGER.warning(_WARNING_TEMPLATE, operation, path, error)
