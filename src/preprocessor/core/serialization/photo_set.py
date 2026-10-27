"""Photo-set models for project files."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from preprocessor.core.serialization.photo import Photo


class PhotoSet(BaseModel, validate_assignment=True):
    """A named collection of photos with shared metadata."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(
        description="Unique identifier identifying the photo set within a project.",
    )
    name: str = Field(
        description="Caller-facing name of the photo set.",
    )
    metadata: dict[str, JsonValue] = Field(
        description="Raw photo-set-level metadata values.",
    )
    photos: list[Photo] = Field(
        description="Photos contained in the photo set.",
    )
