from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from preprocessor.core.model import PhotoData
from preprocessor.core.model._MetadataData import MetadataData
from preprocessor.core.model._ColorCorrectionParams import ColorCorrectionParams
from preprocessor.core.model._LensCorrectionParams import LensCorrectionParams
from preprocessor.core.model._CropParams import CropParams
from preprocessor.core.type_corners import Corners
from preprocessor.core.types import LensVector, CameraMatrix
from preprocessor.model.project_path import ProjectPath




class ProjectData(BaseModel, validate_assignment=True):
    """A project with photos."""

    model_config = ConfigDict(
        extra="forbid",
    )

    #######################
    ## Schema properties ##
    #######################

    schema_version: int = Field(default=2, ge=2)
    """The schema version."""

    ######################
    ## Fixed properties ##
    ######################

    photos: list[PhotoData] = []
    """The list of photos in the project."""
    photos_path: ProjectPath | None = None
    """The file path from which photos were last added, or None if not set."""
    export_path: ProjectPath | None = None
    """The file path where the photos will be exported to, or None if not set."""
