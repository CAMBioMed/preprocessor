"""Top-level project models and metadata resolution helpers."""

from __future__ import annotations

from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from preprocessor.core.serialization.photo import Photo
from preprocessor.core.serialization.photo_set import PhotoSet


class Project(BaseModel, validate_assignment=True):
    """A project containing photo sets and project-level metadata."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(
        description="Unique identifier for this project.",
    )
    name: str = Field(
        description="Display-only project name.",
    )
    metadata: dict[str, JsonValue] = Field(
        description="Project-level metadata values.",
    )
    photo_sets: list[PhotoSet] = Field(
        description="Photo sets contained in the project.",
    )

    @model_validator(mode="after")
    def validate_unique_identifiers(self) -> Self:
        """Reject duplicate photo-set UUIDs and duplicate photo IDs."""

        photo_set_ids: set[UUID] = set()
        photo_ids: set[str] = set()
        for photo_set in self.photo_sets:
            if photo_set.id in photo_set_ids:
                msg = f"duplicate photo set id: {photo_set.id}"
                raise ValueError(msg)
            photo_set_ids.add(photo_set.id)

            for photo in photo_set.photos:
                if photo.id in photo_ids:
                    msg = f"duplicate photo id: {photo.id}"
                    raise ValueError(msg)
                photo_ids.add(photo.id)
        return self

    def metadata_for_photo_set(self, photo_set: PhotoSet) -> dict[str, JsonValue]:
        """Return a fresh shallow metadata overlay for a photo set."""

        return {**self.metadata, **photo_set.metadata}

    def metadata_for_photo(self, photo_set: PhotoSet, photo: Photo) -> dict[str, JsonValue]:
        """Return a fresh shallow metadata overlay for a photo."""

        return {**self.metadata, **photo_set.metadata, **photo.metadata}
