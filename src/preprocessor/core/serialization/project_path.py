"""Context-aware filesystem paths for project-file models."""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Annotated, TypeGuard

from pydantic import PlainSerializer, PlainValidator
from pydantic_core.core_schema import SerializationInfo, ValidationInfo


def _is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    """Return whether a value is a dictionary with object keys and values."""

    return isinstance(value, dict)


def _path_string(value: object) -> str | None:
    """Return the string represented by a supported path value."""

    if isinstance(value, str):
        return value
    if not isinstance(value, PathLike):
        return None

    path = value.__fspath__()
    return path if isinstance(path, str) else None


def _project_dir_from_context(context: object) -> Path | None:
    """Return the project directory supplied to Pydantic validation or serialization."""

    if not _is_object_dict(context):
        return None

    project_dir = _path_string(context.get("project_dir"))
    return Path(project_dir).resolve() if project_dir is not None else None


def _validate_project_path(value: object, info: ValidationInfo) -> Path:
    """Resolve a project-file path against validation context or the current directory."""

    path_value = _path_string(value)
    if path_value is None:
        msg = "project path must be a string or path-like value"
        raise ValueError(msg)
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()

    project_dir = _project_dir_from_context(info.context) or Path.cwd().resolve()
    return (project_dir / path).resolve()


def _serialize_project_path(path: Path, info: SerializationInfo) -> str:
    """Serialize a project-file path relative to context when possible."""

    absolute_path = Path(path).resolve()
    project_dir = _project_dir_from_context(info.context)
    if project_dir is not None:
        try:
            return str(absolute_path.relative_to(project_dir))
        except ValueError:
            return str(absolute_path)
    return str(absolute_path)


type ProjectPath = Annotated[
    Path,
    PlainValidator(_validate_project_path),
    PlainSerializer(_serialize_project_path, return_type=str),
]
"""A path that resolves relative values against the project file directory."""
