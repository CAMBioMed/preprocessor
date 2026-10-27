"""Versioned project-file document model."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from preprocessor.core.serialization.folder import Folder
from preprocessor.core.serialization.project import Project


class ProjectFile(BaseModel, validate_assignment=True):
    """A versioned on-disk project-file document."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = Field(
        description="Project-file schema version. Only version 1 is supported.",
    )
    project: Project = Field(
        description="Project payload stored in the document.",
    )


ProjectFile.model_rebuild(_types_namespace={"Folder": Folder})


def _context(project_dir: Path | None) -> dict[str, Path] | None:
    """Return Pydantic context for project-directory-aware path handling."""

    if project_dir is None:
        return None
    return {"project_dir": project_dir}


def loads_project(project_json: str, *, project_dir: Path | None = None) -> ProjectFile:
    """Load a project file from a JSON string."""

    return ProjectFile.model_validate_json(project_json, context=_context(project_dir))


def dumps_project(project_file: ProjectFile, *, project_dir: Path | None = None) -> str:
    """Dump a project file to human-readable JSON with one trailing newline."""

    return f"{project_file.model_dump_json(indent=2, context=_context(project_dir))}\n"


def read_project(path: Path) -> ProjectFile:
    """Read a UTF-8 project file from the filesystem."""

    resolved_path = path.resolve()
    return loads_project(resolved_path.read_text(encoding="utf-8"), project_dir=resolved_path.parent)


def write_project(project_file: ProjectFile, path: Path) -> None:
    """Write a UTF-8 project file to the filesystem, creating parent directories."""

    resolved_path = path.resolve()
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_path.write_text(dumps_project(project_file, project_dir=resolved_path.parent), encoding="utf-8")
