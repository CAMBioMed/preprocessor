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
    """Return the resolved project directory from a supported Pydantic context."""

    if not _is_object_dict(context):
        return None

    project_dir = _path_string(context.get("project_dir"))
    return Path(project_dir).resolve() if project_dir is not None else None


def _validate_project_path(value: object, info: ValidationInfo) -> Path:
    """Validate and resolve a project path."""

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
    """Serialize a path relative to the project directory when possible."""

    resolved_path = path.resolve()
    project_dir = _project_dir_from_context(info.context)
    if project_dir is None:
        return str(resolved_path)

    try:
        relative_path = resolved_path.relative_to(project_dir, walk_up=False)
        # NOTE: We use str() here to preserve backslashes on Windows,
        # which Path.as_posix() would convert to forward slashes.
        return str(relative_path)
    except ValueError:
        return str(resolved_path)


ProjectPath = Annotated[
    Path,
    PlainValidator(_validate_project_path),
    PlainSerializer(_serialize_project_path, return_type=str),
]
"""A Pydantic type for file paths that are stored relative to the project directory."""
