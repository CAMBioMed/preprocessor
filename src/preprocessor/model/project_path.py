from pathlib import Path
from typing import Annotated, Any

from pydantic import PlainSerializer, AfterValidator
from pydantic_core.core_schema import ValidationInfo, SerializationInfo


def _parse_project_path(v: Any, info: ValidationInfo) -> Path:
    """Pydantic validator to parse a path relative to the project directory."""

    p = Path(v) if not isinstance(v, Path) else v
    if p.is_absolute():
        return p.resolve()

    project_dir = (info.context or {}).get("project_dir")
    if project_dir is None:
        raise ValueError("Project directory must be set in context for parsing project paths")
    project_dir = Path(project_dir).resolve()

    return (project_dir / p).resolve()

def _dump_project_path(v: Path, info: SerializationInfo) -> str:
    """Pydantic serializer to dump a path as relative to the project directory if possible."""

    p = v.resolve()

    project_dir = (info.context or {}).get("project_dir")
    if project_dir is None:
        return p.as_posix()
    project_dir = Path(project_dir).resolve()

    try:
        relative_path = p.relative_to(project_dir, walk_up=False)
        return relative_path.as_posix()
    except ValueError:
        return p.as_posix()

ProjectPath = Annotated[
    Path,
    AfterValidator(_parse_project_path),
    PlainSerializer(_dump_project_path),
]
"""A Pydantic type for file paths that are stored relative to the project directory."""