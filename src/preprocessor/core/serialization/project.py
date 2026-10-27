"""Top-level project models and metadata resolution helpers."""

from __future__ import annotations

from typing import Self
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from preprocessor.core.serialization.folder import Folder
from preprocessor.core.serialization.photo_container import PhotoContainer


class Project(PhotoContainer):
    """A project containing top-level photos and a folder tree."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(
        description="The unique identifier for this project.",
    )
    name: str = Field(
        description="The display name of the project.",
    )

    @model_validator(mode="after")
    def validate_unique_identifiers(self) -> Self:
        """Reject duplicate folder UUIDs and duplicate photo IDs."""

        folder_ids: set[UUID] = set()
        for folder in self.iter_folders():
            if folder.id in folder_ids:
                msg = f"duplicate folder id: {folder.id}"
                raise ValueError(msg)
            folder_ids.add(folder.id)

        photo_ids: set[str] = set()
        for photo in self.iter_photos():
            if photo.id in photo_ids:
                msg = f"duplicate photo id: {photo.id}"
                raise ValueError(msg)
            photo_ids.add(photo.id)

        return self


Project.model_rebuild(_types_namespace={"Folder": Folder})
