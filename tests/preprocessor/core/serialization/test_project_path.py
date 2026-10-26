from __future__ import annotations

import os
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from preprocessor.core.serialization import ProjectPath


class PathDocument(BaseModel):
    """Test document carrying a project-aware path."""

    path: ProjectPath


class CustomPathLike(os.PathLike[str]):
    def __init__(self, path: str) -> None:
        self.path = path

    def __fspath__(self) -> str:
        return self.path


def test_should_resolve_relative_input_against_explicit_context_when_project_path_is_validated(tmp_path: Path) -> None:
    """Should resolve relative input against explicit context when a project path is validated."""

    # Arrange
    project_dir = tmp_path / "project"
    raw_path = "photos/image.jpg"

    # Act
    document = PathDocument.model_validate({"path": raw_path}, context={"project_dir": project_dir})

    # Assert
    assert document.path == (project_dir / raw_path).resolve()


def test_should_preserve_absolute_input_when_project_path_is_validated(tmp_path: Path) -> None:
    """Should preserve absolute input when a project path is validated."""

    # Arrange
    absolute_path = (tmp_path / "outside" / "image.jpg").resolve()
    project_dir = tmp_path / "project"

    # Act
    document = PathDocument.model_validate({"path": str(absolute_path)}, context={"project_dir": project_dir})

    # Assert
    assert document.path == absolute_path


def test_should_accept_path_like_input_when_project_path_is_validated(tmp_path: Path) -> None:
    """Should accept path-like input when a project path is validated."""

    # Arrange
    project_dir = tmp_path / "project"
    raw_path = CustomPathLike(os.path.join("photos", "image.jpg"))

    # Act
    document = PathDocument.model_validate({"path": raw_path}, context={"project_dir": project_dir})

    # Assert
    assert document.path == (project_dir / "photos/image.jpg").resolve()


def test_should_report_validation_error_when_project_path_input_is_unsupported() -> None:
    """Should report a validation error when a project path input is unsupported."""

    # Arrange

    # Act
    with pytest.raises(ValidationError) as exc_info:
        PathDocument.model_validate({"path": object()})

    # Assert
    errors = exc_info.value.errors(include_url=False)
    assert len(errors) == 1
    assert errors[0]["msg"] == "Value error, project path must be a string or path-like value"


def test_should_serialize_relative_path_in_python_and_json_modes_when_path_is_inside_project_directory(
    tmp_path: Path,
) -> None:
    """Should serialize a relative path in Python and JSON modes when inside the project directory."""

    # Arrange
    project_dir = tmp_path / "project"
    document = PathDocument.model_validate(
        {"path": "photos/image.jpg"},
        context={"project_dir": project_dir},
    )

    # Act
    dumps = (
        document.model_dump(context={"project_dir": project_dir}),
        document.model_dump(mode="json", context={"project_dir": project_dir}),
    )

    # Assert
    for dumped in dumps:
        assert dumped["path"] == str(Path("photos/image.jpg"))
        assert isinstance(dumped["path"], str)


def test_should_serialize_absolute_path_in_python_and_json_modes_when_path_is_outside_project_directory(
    tmp_path: Path,
) -> None:
    """Should serialize an absolute path in Python and JSON modes when outside the project directory."""

    # Arrange
    project_dir = tmp_path / "project"
    outside_path = (tmp_path / "outside" / "image.jpg").resolve()
    document = PathDocument.model_validate({"path": outside_path}, context={"project_dir": project_dir})

    # Act
    dumps = (
        document.model_dump(context={"project_dir": project_dir}),
        document.model_dump(mode="json", context={"project_dir": project_dir}),
    )

    # Assert
    for dumped in dumps:
        assert dumped["path"] == str(outside_path)
        assert isinstance(dumped["path"], str)


def test_should_use_current_directory_when_project_context_is_absent() -> None:
    """Should use the current directory when project context is absent."""

    # Arrange
    raw_path = "photos/image.jpg"

    # Act
    document = PathDocument.model_validate({"path": raw_path})
    dumped = document.model_dump(mode="json")

    # Assert
    assert document.path == (Path.cwd() / raw_path).resolve()
    assert dumped["path"] == str((Path.cwd() / raw_path).resolve())


@pytest.mark.parametrize(
    "context",
    ["not a dictionary", {"project_dir": object()}],
)
def test_should_emit_absolute_path_when_serialization_context_is_malformed(
    context: object,
    tmp_path: Path,
) -> None:
    """Should emit an absolute path when the serialization context is malformed."""

    # Arrange
    absolute_path = (tmp_path / "photos" / "image.jpg").resolve()
    document = PathDocument(path=absolute_path)

    # Act
    dumps = (
        document.model_dump(context=context),
        document.model_dump(mode="json", context=context),
    )

    # Assert
    for dumped in dumps:
        assert dumped == {"path": str(absolute_path)}
