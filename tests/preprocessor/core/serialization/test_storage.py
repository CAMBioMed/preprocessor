from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from preprocessor.core.serialization.project_file import (
    ProjectFile,
    dumps_project,
    loads_project,
    read_project,
    write_project,
)


PROJECT_ID = "11111111-1111-1111-1111-111111111111"
PHOTO_SET_ID = "22222222-2222-2222-2222-222222222222"
PHOTO_ID = "a" * 64
RELATIVE_PHOTO_PATH = Path("photosets/set1/originals/img001.jpg")


def nested_project_document() -> dict[str, object]:
    """Return a representative nested project-file document."""

    return {
        "schema_version": 1,
        "project": {
            "id": PROJECT_ID,
            "name": "Example project",
            "metadata": {"shared": "project", "project_only": True},
            "photo_sets": [
                {
                    "id": PHOTO_SET_ID,
                    "name": "Set 1",
                    "metadata": {"shared": "set", "set_only": [1, 2]},
                    "photos": [
                        {
                            "id": PHOTO_ID,
                            "original_filename": str(RELATIVE_PHOTO_PATH),
                            "width": 4000,
                            "height": 3000,
                            "metadata": {"shared": "photo", "photo_only": {"nested": "value"}},
                            "quadrat": [
                                {"x": 0.0, "y": 0.0},
                                {"x": 10.0, "y": 0.0},
                                {"x": 10.0, "y": 5.0},
                                {"x": 0.0, "y": 5.0},
                            ],
                        },
                    ],
                },
            ],
        },
    }


def test_should_resolve_photo_paths_against_project_directory_when_project_is_loaded(tmp_path: Path) -> None:
    """Should resolve photo paths against the project directory when a project is loaded."""

    # Arrange
    project_json = json.dumps(nested_project_document())

    # Act
    project_file = loads_project(project_json, project_dir=tmp_path)

    # Assert
    photo = project_file.project.photo_sets[0].photos[0]
    assert photo.original_filename == (tmp_path / RELATIVE_PHOTO_PATH).resolve()


def test_should_emit_relative_path_metadata_quadrat_and_trailing_newline_when_project_is_dumped(tmp_path: Path) -> None:
    """Should emit relative path, metadata, quadrat, and trailing newline when a project is dumped."""

    # Arrange
    project_file = loads_project(json.dumps(nested_project_document()), project_dir=tmp_path)

    # Act
    project_json = dumps_project(project_file, project_dir=tmp_path)
    dumped = json.loads(project_json)

    # Assert
    assert project_json.endswith("\n")
    assert not project_json.endswith("\n\n")
    photo = dumped["project"]["photo_sets"][0]["photos"][0]
    assert photo["original_filename"] == str(RELATIVE_PHOTO_PATH)
    assert photo["width"] == 4000
    assert photo["height"] == 3000
    assert dumped["project"]["metadata"] == {"shared": "project", "project_only": True}
    assert dumped["project"]["photo_sets"][0]["metadata"] == {"shared": "set", "set_only": [1, 2]}
    assert photo["metadata"] == {"shared": "photo", "photo_only": {"nested": "value"}}
    assert photo["quadrat"] == [
        {"x": 0.0, "y": 0.0},
        {"x": 10.0, "y": 0.0},
        {"x": 10.0, "y": 5.0},
        {"x": 0.0, "y": 5.0},
    ]


def test_should_create_parent_and_round_trip_equal_model_when_project_is_written_and_read(tmp_path: Path) -> None:
    """Should create parents and round-trip an equal model when a project is written and read."""

    # Arrange
    project_file = loads_project(json.dumps(nested_project_document()), project_dir=tmp_path)
    output_path = tmp_path / "missing" / "nested" / "project.json"

    # Act
    write_project(project_file, output_path)
    loaded = read_project(output_path)

    # Assert
    assert output_path.exists()
    assert loaded == project_file


def test_should_surface_validation_error_when_project_json_is_malformed() -> None:
    """Should surface a validation error when project JSON is malformed."""

    # Arrange
    project_json = "{not json"

    # Act / Assert
    with pytest.raises(ValidationError):
        loads_project(project_json)


def test_should_surface_validation_error_when_project_schema_is_invalid() -> None:
    """Should surface a validation error when a project schema is invalid."""

    # Arrange
    project_json = json.dumps({"schema_version": 2, "project": {}})

    # Act / Assert
    with pytest.raises(ValidationError):
        loads_project(project_json)


def test_should_surface_os_error_when_project_file_is_missing(tmp_path: Path) -> None:
    """Should surface an OS error when a project file is missing."""

    # Arrange
    missing_path = tmp_path / "missing.json"

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        read_project(missing_path)


def test_should_return_project_file_json_when_project_is_dumped(tmp_path: Path) -> None:
    """Should return project-file JSON when a project is dumped."""

    # Arrange
    project_file = ProjectFile.model_validate(nested_project_document(), context={"project_dir": tmp_path})

    # Act
    project_json = dumps_project(project_file, project_dir=tmp_path)

    # Assert
    assert json.loads(project_json)["schema_version"] == 1
