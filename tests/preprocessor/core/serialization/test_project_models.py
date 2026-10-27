from __future__ import annotations

import json
import math
from pathlib import Path
from typing import cast
from uuid import UUID

import pytest
from pydantic import ValidationError

from preprocessor.core.serialization.crop_params import CropParams
from preprocessor.core.serialization.folder import Folder
from preprocessor.core.serialization.lens_correction_params import LensCorrectionParams
from preprocessor.core.serialization.photo import Photo
from preprocessor.core.serialization.project import Project
from preprocessor.core.serialization.project_file import ProjectFile
from preprocessor.core.serialization.ruler_params import RulerParams

PROJECT_ID = "11111111-1111-1111-1111-111111111111"
FOLDER_ID = "22222222-2222-2222-2222-222222222222"
NESTED_FOLDER_ID = "44444444-4444-4444-4444-444444444444"
TOP_LEVEL_PHOTO_ID = "c" * 64
PHOTO_ID = "a" * 64
OTHER_PHOTO_ID = "b" * 64


def photo_document(photo_id: str = PHOTO_ID) -> dict[str, object]:
    """Return a valid photo document for model tests."""

    return {
        "id": photo_id,
        "original_filename": "photos/image.jpg",
        "width": 4000,
        "height": 3000,
        "metadata": {"photo": "value"},
    }


def project_document() -> dict[str, object]:
    """Return a valid project-file document for model tests."""

    return {
        "schema_version": 1,
        "project": {
            "id": PROJECT_ID,
            "name": "Example project",
            "metadata": {"project": "value"},
            "photos": [photo_document(TOP_LEVEL_PHOTO_ID)],
            "folders": [
                {
                    "id": FOLDER_ID,
                    "name": "Folder 1",
                    "metadata": {"folder": "value"},
                    "photos": [photo_document()],
                    "folders": [
                        {
                            "id": NESTED_FOLDER_ID,
                            "name": "Nested folder",
                            "metadata": {"nested": "value"},
                            "photos": [photo_document(OTHER_PHOTO_ID)],
                            "folders": [],
                        },
                    ],
                },
            ],
        },
    }


def folders_payload(raw_document: dict[str, object]) -> list[dict[str, object]]:
    """Return mutable folder payloads from a raw project document."""

    project = cast("dict[str, object]", raw_document["project"])
    return cast("list[dict[str, object]]", project["folders"])


def first_folder_payload(raw_document: dict[str, object]) -> dict[str, object]:
    """Return the first mutable folder payload from a raw project document."""

    return folders_payload(raw_document)[0]


def first_photo_payload(raw_document: dict[str, object]) -> dict[str, object]:
    """Return the first mutable photo payload from the first folder."""

    folder = first_folder_payload(raw_document)
    photos = cast("list[dict[str, object]]", folder["photos"])
    return photos[0]


def test_should_validate_shape_and_round_trip_uuids_when_project_file_is_loaded(tmp_path: Path) -> None:
    """Should validate shape and round-trip UUIDs when a project file is loaded."""

    # Arrange
    raw_document = project_document()

    # Act
    project_file = ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})
    dumped = project_file.model_dump_json(context={"project_dir": tmp_path})
    loaded = ProjectFile.model_validate_json(dumped, context={"project_dir": tmp_path})

    # Assert
    assert project_file.project.id == UUID(PROJECT_ID)
    assert project_file.project.photos[0].id == TOP_LEVEL_PHOTO_ID
    assert project_file.project.folders[0].id == UUID(FOLDER_ID)
    assert project_file.project.folders[0].folders[0].id == UUID(NESTED_FOLDER_ID)
    assert loaded.project.id == UUID(PROJECT_ID)
    assert loaded.project.photos[0].id == TOP_LEVEL_PHOTO_ID
    assert loaded.project.folders[0].id == UUID(FOLDER_ID)
    assert loaded.project.folders[0].folders[0].id == UUID(NESTED_FOLDER_ID)
    assert loaded.project.folders[0].photos[0].width == 4000
    assert loaded.project.folders[0].photos[0].height == 3000


def test_should_preserve_four_corner_order_when_quadrat_round_trips_through_json(tmp_path: Path) -> None:
    """Should preserve four-corner order when a quadrat round-trips through JSON."""

    # Arrange
    raw_document = project_document()
    corners = [
        {"x": 0.0, "y": 0.0},
        {"x": 10.0, "y": 0.0},
        {"x": 10.0, "y": 5.0},
        {"x": 0.0, "y": 5.0},
    ]
    photo = first_photo_payload(raw_document)
    photo["quadrat"] = corners

    # Act
    project_file = ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})
    dumped = json.loads(project_file.model_dump_json(context={"project_dir": tmp_path}))

    # Assert
    assert dumped["project"]["folders"][0]["photos"][0]["quadrat"] == corners
    assert project_file.project.folders[0].photos[0].quadrat == (
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (0.0, 5.0),
    )


def test_should_round_trip_crop_ruler_and_lens_params_when_project_file_is_loaded(tmp_path: Path) -> None:
    """Should round-trip crop, ruler, and lens parameters when a project file is loaded."""

    # Arrange
    raw_document = project_document()
    first_photo_payload(raw_document)["params"] = [
        {
            "enabled": True,
            "quadrat": [
                {"x": 0.0, "y": 0.0},
                {"x": 10.0, "y": 0.0},
                {"x": 10.0, "y": 5.0},
                {"x": 0.0, "y": 5.0},
            ],
        },
        {
            "enabled": True,
            "points": [
                {"x": 1.0, "y": 2.0},
                {"x": 3.0, "y": 4.0},
            ],
        },
        {
            "enabled": True,
            "camera_matrix": [[1000.0, 0.0, 512.0], [0.0, 1000.0, 384.0], [0.0, 0.0, 1.0]],
            "coefficients": [0.1, -0.2, 0.0, 0.01],
        },
    ]

    # Act
    project_file = ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})
    dumped = project_file.model_dump_json(context={"project_dir": tmp_path})
    loaded = ProjectFile.model_validate_json(dumped, context={"project_dir": tmp_path})
    params = loaded.project.folders[0].photos[0].params

    # Assert
    assert isinstance(params[0], CropParams)
    assert params[0].quadrat == ((0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0))
    assert isinstance(params[1], RulerParams)
    assert params[1].points == ((1.0, 2.0), (3.0, 4.0))
    assert isinstance(params[2], LensCorrectionParams)
    assert params[2].camera_matrix == ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))
    assert params[2].coefficients == [0.1, -0.2, 0.0, 0.01]


@pytest.mark.parametrize("coordinate", ["x", "y"])
@pytest.mark.parametrize("value", [math.inf, -math.inf, math.nan])
def test_should_reject_non_finite_coordinates_when_quadrat_is_loaded(coordinate: str, value: float) -> None:
    """Should reject non-finite coordinates when a quadrat is loaded."""

    # Arrange
    raw_photo = photo_document()
    corners = [
        {"x": 0.0, "y": 0.0},
        {"x": 10.0, "y": 0.0},
        {"x": 10.0, "y": 5.0},
        {"x": 0.0, "y": 5.0},
    ]
    corners[0][coordinate] = value
    raw_photo["quadrat"] = corners

    # Act
    with pytest.raises(ValidationError) as error:
        Photo.model_validate(raw_photo)

    # Assert
    assert error.value.errors()


def test_should_default_quadrat_to_none_when_it_is_omitted(tmp_path: Path) -> None:
    """Should default a quadrat to None when it is omitted."""

    # Arrange
    raw_document = project_document()

    # Act
    project_file = ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})

    # Assert
    assert project_file.project.folders[0].photos[0].quadrat is None


def test_should_normalize_uppercase_value_when_photo_id_is_loaded() -> None:
    """Should normalize an uppercase value when a photo ID is loaded."""

    # Arrange
    raw_photo = photo_document("UPPERCASE-ID")

    # Act
    photo = Photo.model_validate(raw_photo)

    # Assert
    assert photo.id == "uppercase-id"


def test_should_fail_with_specified_message_when_photo_id_is_blank() -> None:
    """Should fail with the specified message when a photo ID is blank."""

    # Arrange
    raw_photo = photo_document("   ")

    # Act / Assert
    with pytest.raises(ValidationError, match="Photo ID must be non-blank"):
        Photo.model_validate(raw_photo)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("width", None),
        ("height", None),
        ("width", 0),
        ("height", 0),
        ("width", -1),
        ("height", -1),
    ],
)
def test_should_require_positive_integer_dimensions_when_photo_is_loaded(field: str, value: object) -> None:
    """Should require positive integer dimensions when a photo is loaded."""

    # Arrange
    raw_photo = photo_document()
    if value is None:
        del raw_photo[field]
    else:
        raw_photo[field] = value

    # Act / Assert
    with pytest.raises(ValidationError):
        Photo.model_validate(raw_photo)


def test_should_fail_when_photo_ids_are_duplicated_across_project_tree(tmp_path: Path) -> None:
    """Should fail when photo IDs are duplicated across the project tree."""

    # Arrange
    raw_document = project_document()
    project = cast("dict[str, object]", raw_document["project"])
    photos = cast("list[dict[str, object]]", project["photos"])
    photos.append(photo_document(PHOTO_ID.upper()))

    # Act / Assert
    with pytest.raises(ValidationError, match=f"duplicate photo id: {PHOTO_ID}"):
        ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})


def test_should_fail_when_folder_uuids_are_duplicated_in_project_tree(tmp_path: Path) -> None:
    """Should fail when folder UUIDs are duplicated in the project tree."""

    # Arrange
    raw_document = project_document()
    folders = cast("list[dict[str, object]]", first_folder_payload(raw_document)["folders"])
    nested_folder = folders[0]
    nested_folder["id"] = FOLDER_ID

    # Act / Assert
    with pytest.raises(ValidationError, match=f"duplicate folder id: {FOLDER_ID}"):
        ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})


def test_should_fail_when_schema_version_is_unsupported(tmp_path: Path) -> None:
    """Should fail when the schema version is unsupported."""

    # Arrange
    raw_document = project_document()
    raw_document["schema_version"] = 2

    # Act / Assert
    with pytest.raises(ValidationError):
        ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})


def test_should_fail_when_object_contains_unknown_field(tmp_path: Path) -> None:
    """Should fail when an object contains an unknown field."""

    # Arrange
    raw_document = project_document()
    cast("dict[str, object]", raw_document["project"])["unknown"] = "value"

    # Act / Assert
    with pytest.raises(ValidationError):
        ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})


def test_should_iterate_tree_and_resolve_inherited_metadata_when_project_is_traversed() -> None:
    """Should iterate the folder tree and resolve inherited metadata."""

    # Arrange
    top_level_photo = Photo(
        id=TOP_LEVEL_PHOTO_ID,
        original_filename=Path("photos/top.jpg"),
        metadata={"shared": "top", "top_only": "value"},
        width=4000,
        height=3000,
    )
    root_photo = Photo(
        id=PHOTO_ID,
        original_filename=Path("photos/root.jpg"),
        metadata={"shared": "photo", "photo_only": "value"},
        width=4000,
        height=3000,
    )
    nested_photo = Photo(
        id=OTHER_PHOTO_ID,
        original_filename=Path("photos/nested.jpg"),
        metadata={"nested_only": "value"},
        width=4000,
        height=3000,
    )
    nested_folder = Folder(
        id=UUID(NESTED_FOLDER_ID),
        name="Nested folder",
        metadata={"nested": "folder"},
        photos=[nested_photo],
        folders=[],
    )
    root_folder = Folder(
        id=UUID(FOLDER_ID),
        name="Folder 1",
        metadata={"shared": "folder", "folder_only": "value"},
        photos=[root_photo],
        folders=[nested_folder],
    )
    project = Project(
        id=UUID(PROJECT_ID),
        name="Example project",
        metadata={"shared": "project", "project_only": {"nested": 1}},
        photos=[top_level_photo],
        folders=[root_folder],
    )

    # Act
    folders = list(project.iter_folders())
    photos = list(project.iter_photos())
    resolved = list(project.iter_photos_with_metadata())
    resolved[0][1]["shared"] = "changed"

    # Assert
    assert [folder.id for folder in folders] == [UUID(FOLDER_ID), UUID(NESTED_FOLDER_ID)]
    assert [photo.id for photo in photos] == [TOP_LEVEL_PHOTO_ID, PHOTO_ID, OTHER_PHOTO_ID]
    assert [photo.id for photo, _ in resolved] == [TOP_LEVEL_PHOTO_ID, PHOTO_ID, OTHER_PHOTO_ID]
    assert resolved[0][1] == {
        "shared": "changed",
        "project_only": {"nested": 1},
        "top_only": "value",
    }
    assert resolved[1][1] == {
        "shared": "photo",
        "project_only": {"nested": 1},
        "folder_only": "value",
        "photo_only": "value",
    }
    assert resolved[2][1] == {
        "shared": "folder",
        "project_only": {"nested": 1},
        "folder_only": "value",
        "nested": "folder",
        "nested_only": "value",
    }
    assert project.metadata["shared"] == "project"
