import os
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from preprocessor.core.model import ProjectPath


class PathDocument(BaseModel):
    path: ProjectPath


class CustomPathLike(os.PathLike[str]):
    def __init__(self, path: str) -> None:
        self.path = path

    def __fspath__(self) -> str:
        return self.path


def test_relative_input_resolves_against_context_project_directory(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"

    document = PathDocument.model_validate(
        {"path": "photos/image.jpg"},
        context={"project_dir": project_dir},
    )

    assert document.path == (project_dir / "photos/image.jpg").resolve()


def test_absolute_input_is_preserved(tmp_path: Path) -> None:
    absolute_path = (tmp_path / "photos/image.jpg").resolve()

    document = PathDocument.model_validate(
        {"path": absolute_path},
        context={"project_dir": tmp_path / "other-project"},
    )

    assert document.path == absolute_path


def test_path_like_input_is_accepted(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"

    document = PathDocument.model_validate(
        {"path": CustomPathLike(os.path.join("photos", "image.jpg"))},
        context={"project_dir": project_dir},
    )

    assert document.path == (project_dir / "photos/image.jpg").resolve()


def test_unsupported_input_reports_controlled_validation_error() -> None:
    with pytest.raises(ValidationError) as exc_info:
        PathDocument.model_validate({"path": object()})

    errors = exc_info.value.errors(include_url=False)
    assert len(errors) == 1
    assert errors[0]["msg"] == "Value error, project path must be a string or path-like value"


def test_relative_input_without_context_uses_current_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    document = PathDocument.model_validate({"path": "photos/image.jpg"})

    assert document.path == (tmp_path / "photos/image.jpg").resolve()


@pytest.mark.parametrize(
    "context",
    ["not a dictionary", {"project_dir": object()}],
)
def test_relative_input_with_malformed_context_uses_current_directory(
    context: object,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    document = PathDocument.model_validate({"path": "photos/image.jpg"}, context=context)

    assert document.path == (tmp_path / "photos/image.jpg").resolve()


def test_inside_and_outside_paths_serialize_in_python_and_json_modes(tmp_path: Path) -> None:
    project_dir = (tmp_path / "project").resolve()
    inside_path = project_dir / "photos/image.jpg"
    outside_path = (tmp_path / "outside/image.jpg").resolve()
    context = {"project_dir": project_dir}

    inside_document = PathDocument(path=inside_path)
    outside_document = PathDocument(path=outside_path)

    for dump in (
        inside_document.model_dump(context=context),
        inside_document.model_dump(mode="json", context=context),
    ):
        assert dump == {"path": os.path.join("photos", "image.jpg")}
        assert isinstance(dump["path"], str)

    for dump in (
        outside_document.model_dump(context=context),
        outside_document.model_dump(mode="json", context=context),
    ):
        assert dump == {"path": str(outside_path)}
        assert isinstance(dump["path"], str)


@pytest.mark.parametrize(
    "context",
    ["not a dictionary", {"project_dir": object()}],
)
def test_malformed_serialization_context_emits_absolute_path(
    context: object,
    tmp_path: Path,
) -> None:
    absolute_path = (tmp_path / "photos/image.jpg").resolve()
    document = PathDocument(path=absolute_path)

    assert document.model_dump(context=context) == {"path": str(absolute_path)}
    assert document.model_dump(mode="json", context=context) == {"path": str(absolute_path)}
