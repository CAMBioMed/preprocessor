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


def test_should_resolve_relative_input_when_project_directory_context_is_present(tmp_path: Path) -> None:
    """Should resolve relative input when project directory context is present."""
    project_dir = tmp_path / "project"

    document = PathDocument.model_validate(
        {"path": "photos/image.jpg"},
        context={"project_dir": project_dir},
    )

    assert document.path == (project_dir / "photos/image.jpg").resolve()


def test_should_preserve_absolute_input_when_model_is_validated(tmp_path: Path) -> None:
    """Should preserve absolute input when the model is validated."""
    absolute_path = (tmp_path / "photos/image.jpg").resolve()

    document = PathDocument.model_validate(
        {"path": absolute_path},
        context={"project_dir": tmp_path / "other-project"},
    )

    assert document.path == absolute_path


def test_should_accept_path_like_input_when_model_is_validated(tmp_path: Path) -> None:
    """Should accept path-like input when the model is validated."""
    project_dir = tmp_path / "project"

    document = PathDocument.model_validate(
        {"path": CustomPathLike(os.path.join("photos", "image.jpg"))},
        context={"project_dir": project_dir},
    )

    assert document.path == (project_dir / "photos/image.jpg").resolve()


def test_should_report_validation_error_when_input_is_unsupported() -> None:
    """Should report a validation error when input is unsupported."""
    with pytest.raises(ValidationError) as exc_info:
        PathDocument.model_validate({"path": object()})

    errors = exc_info.value.errors(include_url=False)
    assert len(errors) == 1
    assert errors[0]["msg"] == "Value error, project path must be a string or path-like value"


def test_should_use_current_directory_when_relative_input_has_no_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Should use the current directory when relative input has no context."""
    monkeypatch.chdir(tmp_path)

    document = PathDocument.model_validate({"path": "photos/image.jpg"})

    assert document.path == (tmp_path / "photos/image.jpg").resolve()


@pytest.mark.parametrize(
    "context",
    ["not a dictionary", {"project_dir": object()}],
)
def test_should_use_current_directory_when_context_is_malformed(
    context: object,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Should use the current directory when context is malformed."""
    monkeypatch.chdir(tmp_path)

    document = PathDocument.model_validate({"path": "photos/image.jpg"}, context=context)

    assert document.path == (tmp_path / "photos/image.jpg").resolve()


def test_should_serialize_inside_and_outside_paths_when_python_and_json_modes_are_used(tmp_path: Path) -> None:
    """Should serialize inside and outside paths when Python and JSON modes are used."""
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
def test_should_emit_absolute_path_when_serialization_context_is_malformed(
    context: object,
    tmp_path: Path,
) -> None:
    """Should emit an absolute path when serialization context is malformed."""
    absolute_path = (tmp_path / "photos/image.jpg").resolve()
    document = PathDocument(path=absolute_path)

    assert document.model_dump(context=context) == {"path": str(absolute_path)}
    assert document.model_dump(mode="json", context=context) == {"path": str(absolute_path)}
