from __future__ import annotations

import json
import math
from pathlib import Path
from typing import cast
from uuid import UUID

import pytest
from pydantic import ValidationError

from preprocessor.core.serialization.crop_params import CropParams
from preprocessor.core.serialization.photo import Photo
from preprocessor.core.serialization.photo_set import PhotoSet
from preprocessor.core.serialization.project import Project
from preprocessor.core.serialization.project_file import ProjectFile
from preprocessor.core.serialization.ruler_params import RulerParams

PROJECT_ID = "11111111-1111-1111-1111-111111111111"
PHOTO_SET_ID = "22222222-2222-2222-2222-222222222222"
OTHER_PHOTO_SET_ID = "33333333-3333-3333-3333-333333333333"
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
            "photo_sets": [
                {
                    "id": PHOTO_SET_ID,
                    "name": "Set 1",
                    "metadata": {"set": "value"},
                    "photos": [photo_document()],
                },
            ],
        },
    }


def photo_sets_payload(raw_document: dict[str, object]) -> list[dict[str, object]]:
    """Return mutable photo-set payloads from a raw project document."""

    project = cast("dict[str, object]", raw_document["project"])
    return cast("list[dict[str, object]]", project["photo_sets"])


def first_photo_payload(raw_document: dict[str, object]) -> dict[str, object]:
    """Return the first mutable photo payload from a raw project document."""

    photo_set = photo_sets_payload(raw_document)[0]
    photos = cast("list[dict[str, object]]", photo_set["photos"])
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
    assert project_file.project.photo_sets[0].id == UUID(PHOTO_SET_ID)
    assert loaded.project.id == UUID(PROJECT_ID)
    assert loaded.project.photo_sets[0].id == UUID(PHOTO_SET_ID)
    assert loaded.project.photo_sets[0].photos[0].width == 4000
    assert loaded.project.photo_sets[0].photos[0].height == 3000


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
    assert dumped["project"]["photo_sets"][0]["photos"][0]["quadrat"] == corners
    assert project_file.project.photo_sets[0].photos[0].quadrat == (
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (0.0, 5.0),
    )


def test_should_round_trip_crop_and_ruler_params_when_project_file_is_loaded(tmp_path: Path) -> None:
    """Should round-trip crop and ruler parameters when a project file is loaded."""

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
    ]

    # Act
    project_file = ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})
    dumped = project_file.model_dump_json(context={"project_dir": tmp_path})
    loaded = ProjectFile.model_validate_json(dumped, context={"project_dir": tmp_path})
    params = loaded.project.photo_sets[0].photos[0].params

    # Assert
    assert isinstance(params[0], CropParams)
    assert params[0].quadrat == ((0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0))
    assert isinstance(params[1], RulerParams)
    assert params[1].points == ((1.0, 2.0), (3.0, 4.0))


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
    assert project_file.project.photo_sets[0].photos[0].quadrat is None


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


def test_should_fail_when_photo_ids_are_duplicated_across_photo_sets(tmp_path: Path) -> None:
    """Should fail when photo IDs are duplicated across photo sets."""

    # Arrange
    raw_document = project_document()
    photo_sets = photo_sets_payload(raw_document)
    photo_sets.append(
        {
            "id": OTHER_PHOTO_SET_ID,
            "name": "Set 2",
            "metadata": {},
            "photos": [photo_document(PHOTO_ID.upper())],
        },
    )

    # Act / Assert
    with pytest.raises(ValidationError, match=f"duplicate photo id: {PHOTO_ID}"):
        ProjectFile.model_validate(raw_document, context={"project_dir": tmp_path})


def test_should_fail_when_photo_set_uuids_are_duplicated(tmp_path: Path) -> None:
    """Should fail when photo set UUIDs are duplicated."""

    # Arrange
    raw_document = project_document()
    photo_sets = photo_sets_payload(raw_document)
    photo_sets.append(
        {
            "id": PHOTO_SET_ID,
            "name": "Duplicate set",
            "metadata": {},
            "photos": [photo_document(OTHER_PHOTO_ID)],
        },
    )

    # Act / Assert
    with pytest.raises(ValidationError, match=f"duplicate photo set id: {PHOTO_SET_ID}"):
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


def test_should_return_fresh_shallow_overlays_when_metadata_resolvers_are_called() -> None:
    """Should return fresh shallow overlays when metadata resolvers are called."""

    # Arrange
    project = Project(
        id=UUID(PROJECT_ID),
        name="Example project",
        metadata={"shared": "project", "project_only": {"nested": 1}},
        photo_sets=[],
    )
    photo_set = PhotoSet(
        id=UUID(PHOTO_SET_ID),
        name="Set 1",
        metadata={"shared": "set", "set_only": "value"},
        photos=[],
    )
    photo = Photo(
        id=PHOTO_ID,
        original_filename=Path("photos/image.jpg"),
        metadata={"shared": "photo", "photo_only": "value"},
        width=4000,
        height=3000,
    )

    # Act
    photo_set_metadata = project.metadata_for_photo_set(photo_set)
    photo_metadata = project.metadata_for_photo(photo_set, photo)
    photo_metadata["shared"] = "changed"

    # Assert
    assert photo_set_metadata == {"shared": "set", "project_only": {"nested": 1}, "set_only": "value"}
    assert photo_metadata == {
        "shared": "changed",
        "project_only": {"nested": 1},
        "set_only": "value",
        "photo_only": "value",
    }
    assert project.metadata == {"shared": "project", "project_only": {"nested": 1}}
    assert photo_set.metadata == {"shared": "set", "set_only": "value"}
    assert photo.metadata == {"shared": "photo", "photo_only": "value"}
