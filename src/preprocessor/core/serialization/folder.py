"""Folder models for project files."""

from collections.abc import Iterator
from uuid import UUID

from pydantic import ConfigDict, Field

from preprocessor.core.serialization.photo import Photo
from preprocessor.core.serialization.photo_container import PhotoContainer


class Folder(PhotoContainer):
    """A named collection of folders and photos with shared metadata."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(
        description="The unique identifier for the folder within a project.",
    )
    name: str = Field(
        description="The display name of the folder.",
    )

    def iter_folders(self) -> Iterator["Folder"]:
        """Yield this folder and all descendant folders."""
        yield self

        for folder in self.folders:
            yield from folder.iter_folders()

    def iter_photos(self) -> Iterator[Photo]:
        """Yield all photos in this folder and its descendants."""
        yield from self.photos

        for folder in self.folders:
            yield from folder.iter_photos()


PhotoContainer.model_rebuild(_types_namespace={"Folder": Folder})
Folder.model_rebuild(_types_namespace={"Folder": Folder})
