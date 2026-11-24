from __future__ import annotations

from abc import ABC
from collections.abc import Iterator
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from preprocessor.core.serialization.photo import Photo

if TYPE_CHECKING:
    from preprocessor.core.serialization.folder import Folder


class PhotoContainer(BaseModel, ABC, validate_assignment=True):
    """Base class for containers of photos and nested folders."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, JsonValue] = Field(
        description="The container-level metadata.",
    )
    photos: list[Photo] = Field(
        description="The photos contained in the container.",
    )
    folders: list[Folder] = Field(
        description="The subfolders contained in the container.",
    )

    def iter_folders(self) -> Iterator[Folder]:
        """Iterate over all descendant folders."""
        for folder in self.folders:
            yield from folder.iter_folders()

    def iter_photos(self) -> Iterator[Photo]:
        """Iterate over all descendant photos."""
        yield from self.photos

        for folder in self.folders:
            yield from folder.iter_photos()

    def iter_photos_with_metadata(
        self,
        inherited_metadata: dict[str, JsonValue] | None = None,
    ) -> Iterator[tuple[Photo, dict[str, JsonValue]]]:
        """Iterate over photos with resolved metadata."""
        metadata = {
            **(inherited_metadata or {}),
            **self.metadata,
        }

        for photo in self.photos:
            yield photo, {**metadata, **photo.metadata}

        for folder in self.folders:
            yield from folder.iter_photos_with_metadata(metadata)
