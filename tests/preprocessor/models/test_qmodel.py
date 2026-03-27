from pathlib import Path

import pytest
from PySide6.QtCore import Signal
from pydantic import BaseModel

from preprocessor.model.project_path import ProjectPath
from preprocessor.model.qmodel import QModel


class ExampleData(BaseModel, validate_assignment=True):
    """A simple Pydantic model for testing."""

    name: str
    path: ProjectPath | None


class ExampleQModel(QModel[ExampleData]):
    """A simple QModel subclass for testing."""

    on_name_changed: Signal = Signal(str)
    on_path_changed: Signal = Signal(object)

    def __init__(self, data: ExampleData | dict[str, object] | None) -> None:
        super().__init__(model_cls=ExampleData, data=data)

    @property
    def name(self) -> str:
        return self._data.name

    @name.setter
    def name(self, value: str) -> None:
        self._set_field("name", value)

    @property
    def path(self) -> Path | None:
        return self._data.path

    @path.setter
    def path(self, value: Path | None) -> None:
        self._set_field("path", value)


# class TestQModel:
#     """Tests for the QModel class."""
#
#     def test_path_attr_stores_relative_path_when_resource_is_inside_project_dir(self, tmp_path: Path) -> None:
#         """Should store the path relative to the project directory, when the resource is inside the project directory."""
#         # Arrange
#         project_dir = tmp_path / "project"
#         resource = project_dir / "images" / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data)
#
#         # Act
#         stored_path = model._data.path
#         abs_path = model.path
#
#         # Assert: stored path is relative to the project dir
#         assert stored_path is not None
#         assert not stored_path.is_absolute()
#         assert stored_path == Path("images") / "img.jpg"
#         # Assert: path property returns the absolute path
#         assert abs_path is not None
#         assert abs_path.is_absolute()
#         assert abs_path == resource.resolve()
#
#     def test_path_attr_stores_absolute_path_when_resource_is_outside_project_dir(self, tmp_path: Path) -> None:
#         """Should store the absolute path, when the resource is outside the project directory."""
#         # Arrange
#         project_dir = tmp_path / "project"
#         resource = tmp_path / "other" / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data)
#
#         # Act
#         stored_path = model._data.path
#         abs_path = model.path
#
#         # Assert: stored path remains absolute
#         assert stored_path is not None
#         assert stored_path.is_absolute()
#         assert stored_path == resource
#         assert stored_path == resource.resolve()
#         # Assert: path property returns the absolute path
#         assert abs_path is not None
#         assert abs_path.is_absolute()
#         assert abs_path == resource.resolve()
#
#     def test_path_attr_stores_absolute_path_when_project_dir_is_none(self, tmp_path: Path) -> None:
#         """Should store the absolute path, when the project directory is None."""
#         # Arrange
#         resource = tmp_path / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data=data)
#
#         # Act
#         stored_path = model._data.path
#         abs_path = model.path
#
#         # Assert: stored path remains absolute
#         assert stored_path is not None
#         assert stored_path.is_absolute()
#         assert stored_path == resource
#         assert stored_path == resource.resolve()
#         # Assert: path property returns the absolute path
#         assert abs_path is not None
#         assert abs_path.is_absolute()
#         assert abs_path == resource.resolve()
#
#     def test_set_project_path_updates_stored_path_to_absolute_when_outside_project(self, tmp_path: Path) -> None:
#         """Should update the stored path to absolute when the project directory changes and the resource is outside the new project directory."""
#         # Arrange
#         project1_dir = tmp_path / "project1"
#         project2_dir = tmp_path / "project2"
#         resource = project1_dir / "images" / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data)
#
#         # Act
#         stored_path1 = model._data.path
#         abs_path1 = model.path
#
#         # Assert: stored path is relative to the project dir
#         assert stored_path1 is not None
#         assert not stored_path1.is_absolute()
#         assert stored_path1 == Path("images") / "img.jpg"
#         # Assert: path property returns the absolute path
#         assert abs_path1 is not None
#         assert abs_path1.is_absolute()
#         assert abs_path1 == resource.resolve()
#
#         # Act
#         # model.set_project_dir(project2_dir)
#         stored_path2 = model._data.path
#         abs_path2 = model.path
#
#         # Assert: stored path is now absolute
#         assert stored_path2 is not None
#         assert stored_path2.is_absolute()
#         assert stored_path2 == resource
#         assert stored_path2 == resource.resolve()
#         # Assert: path property returns the absolute path
#         assert abs_path2 is not None
#         assert abs_path2.is_absolute()
#         assert abs_path2 == resource.resolve()
#
#     def test_set_project_path_updates_stored_path_to_relative_when_inside_project(self, tmp_path: Path) -> None:
#         """Should update the stored path to be relative to the new project directory, when the resource is inside the new project directory."""
#         # Arrange
#         project1_dir = tmp_path / "project1"
#         project2_dir = tmp_path / "project2"
#         resource = project2_dir / "images" / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data)
#
#         # Act
#         stored_path1 = model._data.path
#         abs_path1 = model.path
#
#         # Assert: stored path is absolute
#         assert stored_path1 is not None
#         assert stored_path1.is_absolute()
#         assert stored_path1 == resource
#         assert stored_path1 == resource.resolve()
#         # Assert: path property returns the absolute path
#         assert abs_path1 is not None
#         assert abs_path1.is_absolute()
#         assert abs_path1 == resource.resolve()
#
#         # Act
#         model.set_project_dir(project2_dir)
#         stored_path2 = model._data.path
#         abs_path2 = model.path
#
#         # Assert: stored path is now relative to the project dir
#         assert stored_path2 is not None
#         assert not stored_path2.is_absolute()
#         assert stored_path2 == Path("images") / "img.jpg"
#         # Assert: path property returns the absolute path
#         assert abs_path2 is not None
#         assert abs_path2.is_absolute()
#         assert abs_path2 == resource.resolve()
#
#     def test_set_project_path_updates_stored_path_to_absolute_when_none(self, tmp_path: Path) -> None:
#         """Should update the stored path to absolute when the project directory is set to None."""
#         # Arrange
#         project1_dir = tmp_path / "project1"
#         resource = project1_dir / "images" / "img.jpg"
#         data = ExampleData(name="test", path=resource)
#         model = ExampleQModel(data)
#
#         # Act
#         stored_path1 = model._data.path
#         abs_path1 = model.path
#
#         # Assert: stored path is relative to the project dir
#         assert stored_path1 is not None
#         assert not stored_path1.is_absolute()
#         assert stored_path1 == Path("images") / "img.jpg"
#         # Assert: path property returns the absolute path
#         assert abs_path1 is not None
#         assert abs_path1.is_absolute()
#         assert abs_path1 == resource.resolve()
#
#         # Act
#         # model.set_project_dir(None)
#         stored_path2 = model._data.path
#         abs_path2 = model.path
#
#         # Assert: stored path is now absolute
#         assert stored_path2 is not None
#         assert stored_path2.is_absolute()
#         assert stored_path2 == resource
#         assert stored_path2 == resource.resolve()
#         # Assert: path property returns the absolute path
#         assert abs_path2 is not None
#         assert abs_path2.is_absolute()
#         assert abs_path2 == resource.resolve()
