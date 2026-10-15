from pathlib import Path

import pytest
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtTest import QSignalSpy

from preprocessor.core.model import PhotoData
from preprocessor.gui.model import QPhotoModel
from preprocessor.gui.tree_dock_model import TreeDockModel


def _photo(path: Path, image_id: str) -> QPhotoModel:
    return QPhotoModel(PhotoData(image_id=image_id, original_filename=path.resolve()))


def test_builds_only_required_hierarchy_with_roles(tmp_path: Path) -> None:
    """The tree contains the root and only photo directory ancestry."""
    # Arrange
    project_directory = (tmp_path / "project").resolve()
    project_directory.mkdir()
    (project_directory / "unrelated").mkdir()
    root_photo = _photo(project_directory / "ABC.jpg", "root")
    nested_photo = _photo(project_directory / "x" / "y" / "ABC.jpg", "nested")
    model = TreeDockModel()

    # Act
    model.set_photos([root_photo, nested_photo], project_directory=project_directory)
    root_index = model.index(0, 0)
    x_index = model.index(0, 0, root_index)
    y_index = model.index(0, 0, x_index)

    # Assert
    assert model.rowCount() == 1
    assert model.rowCount(root_index) == 1
    assert model.rowCount(x_index) == 1
    assert model.rowCount(y_index) == 0
    assert model.parent(root_index) == QModelIndex()
    assert model.parent(x_index) == root_index
    assert model.parent(y_index) == x_index
    assert model.data(root_index) == project_directory.name
    assert model.data(y_index) == "y"
    assert model.data(y_index, Qt.ItemDataRole.ToolTipRole) == str(project_directory / "x" / "y")
    assert not model.index_for_directory(project_directory / "unrelated").isValid()


def test_rejects_invalid_and_foreign_indexes(tmp_path: Path) -> None:
    """Invalid model coordinates and foreign indexes have no tree data."""
    # Arrange
    project_directory = tmp_path.resolve()
    model = TreeDockModel()
    model.set_photos([_photo(project_directory / "ABC.jpg", "root")], project_directory=project_directory)
    foreign_model = QStandardItemModel(1, 1)
    foreign_index = foreign_model.index(0, 0)

    # Act
    negative = model.index(-1, 0)
    wrong_column = model.index(0, 1)
    out_of_range = model.index(1, 0)
    below_foreign = model.index(0, 0, foreign_index)

    # Assert
    assert not negative.isValid()
    assert not wrong_column.isValid()
    assert not out_of_range.isValid()
    assert not below_foreign.isValid()
    assert model.rowCount(foreign_index) == 0
    assert model.columnCount(foreign_index) == 0
    assert model.data(foreign_index) is None
    assert model.flags(foreign_index) == Qt.ItemFlag.NoItemFlags
    assert model.directory_for_index(foreign_index) is None


def test_groups_only_direct_photos_in_flat_order(tmp_path: Path) -> None:
    """Directory photo groups preserve input order and exclude descendants."""
    # Arrange
    project_directory = tmp_path.resolve()
    first = _photo(project_directory / "x" / "first.jpg", "first")
    descendant = _photo(project_directory / "x" / "y" / "child.jpg", "child")
    second = _photo(project_directory / "x" / "second.jpg", "second")
    model = TreeDockModel()

    # Act
    model.set_photos([first, descendant, second], project_directory=project_directory)
    direct_photos = model.photos_in_directory(project_directory / "x")
    direct_photos.clear()

    # Assert
    assert model.photos_in_directory(project_directory / "x") == [first, second]
    assert model.photos_in_directory(project_directory) == []
    assert model.photos_in_directory(project_directory / "missing") == []
    assert model.photos_in_directory(None) == []


def test_initial_activation_is_deterministic_and_case_insensitive(tmp_path: Path) -> None:
    """Initial activation uses case-insensitive path order with a stable tie-breaker."""
    # Arrange
    project_directory = tmp_path.resolve()
    upper = _photo(project_directory / "A" / "upper.jpg", "upper")
    lower = _photo(project_directory / "a" / "lower.jpg", "lower")
    later = _photo(project_directory / "b" / "later.jpg", "later")
    model = TreeDockModel()

    # Act
    model.set_photos([later, lower, upper], project_directory=project_directory)

    # Assert
    assert model.active_directory == project_directory / "A"


def test_activation_persists_and_reset_selects_first_direct_directory(tmp_path: Path) -> None:
    """Rebuilds preserve a present active node unless reset is requested."""
    # Arrange
    project_directory = tmp_path.resolve()
    root = _photo(project_directory / "root.jpg", "root")
    nested = _photo(project_directory / "x" / "nested.jpg", "nested")
    added = _photo(project_directory / "x" / "added.jpg", "added")
    model = TreeDockModel()
    model.set_photos([root, nested], project_directory=project_directory)
    model.active_directory = project_directory / "x"

    # Act
    model.set_photos([root, nested, added], project_directory=project_directory)
    preserved = model.active_directory
    model.set_photos([root, nested], project_directory=project_directory, reset_active=True)

    # Assert
    assert preserved == project_directory / "x"
    assert model.active_directory == project_directory


def test_missing_active_directory_falls_back_to_first_direct_directory(tmp_path: Path) -> None:
    """Removing the active node activates the first remaining photo directory."""
    # Arrange
    project_directory = tmp_path.resolve()
    root = _photo(project_directory / "root.jpg", "root")
    nested = _photo(project_directory / "x" / "nested.jpg", "nested")
    model = TreeDockModel()
    model.set_photos([root, nested], project_directory=project_directory)
    model.active_directory = project_directory / "x"

    # Act
    model.set_photos([root], project_directory=project_directory)

    # Assert
    assert model.active_directory == project_directory


def test_structural_active_directory_persists_without_direct_photos(tmp_path: Path) -> None:
    """An active ancestor remains selected while it still has displayed descendants."""
    # Arrange
    project_directory = tmp_path.resolve()
    first = _photo(project_directory / "x" / "y" / "first.jpg", "first")
    second = _photo(project_directory / "x" / "z" / "second.jpg", "second")
    model = TreeDockModel()
    model.set_photos([first, second], project_directory=project_directory)
    model.active_directory = project_directory / "x"

    # Act
    model.set_photos([second], project_directory=project_directory)

    # Assert
    assert model.active_directory == project_directory / "x"
    assert model.photos_in_directory(model.active_directory) == []


def test_active_directory_rejects_absent_path(tmp_path: Path) -> None:
    """Explicit activation accepts only exact paths represented in the tree."""
    # Arrange
    project_directory = tmp_path.resolve()
    model = TreeDockModel()
    model.set_photos([_photo(project_directory / "root.jpg", "root")], project_directory=project_directory)

    # Act / Assert
    with pytest.raises(ValueError, match=r"^directory is not present in tree: "):
        model.active_directory = project_directory / "missing"


def test_empty_photos_clear_tree_without_project_directory(tmp_path: Path) -> None:
    """An empty photo iterable clears the tree and activation without a root."""
    # Arrange
    project_directory = tmp_path.resolve()
    model = TreeDockModel()
    model.set_photos([_photo(project_directory / "root.jpg", "root")], project_directory=project_directory)

    # Act
    model.set_photos([], project_directory=None)

    # Assert
    assert model.rowCount() == 0
    assert model.active_directory is None


def test_nonempty_photos_require_project_directory(tmp_path: Path) -> None:
    """Photos cannot build a tree without a project-directory root."""
    # Arrange
    photo = _photo(tmp_path / "root.jpg", "root")
    model = TreeDockModel()

    # Act / Assert
    with pytest.raises(ValueError, match="^project directory is required when photos are present$"):
        model.set_photos([photo], project_directory=None)


def test_photo_outside_project_directory_is_rejected(tmp_path: Path) -> None:
    """Photos outside the project directory violate the single-root invariant."""
    # Arrange
    project_directory = (tmp_path / "project").resolve()
    outside_photo = _photo(tmp_path / "outside.jpg", "outside")
    model = TreeDockModel()

    # Act / Assert
    with pytest.raises(
        ValueError,
        match=f"^photo path is outside project directory: {outside_photo.original_filename}$",
    ):
        model.set_photos([outside_photo], project_directory=project_directory)


def test_rebuild_emits_only_for_effective_activation_change(tmp_path: Path) -> None:
    """A rebuild emits activation once only when its final active path changes."""
    # Arrange
    project_directory = tmp_path.resolve()
    first = _photo(project_directory / "a" / "first.jpg", "first")
    second = _photo(project_directory / "b" / "second.jpg", "second")
    model = TreeDockModel()
    spy = QSignalSpy(model.on_active_directory_changed)

    # Act
    model.set_photos([first], project_directory=project_directory)
    model.set_photos([first, second], project_directory=project_directory)
    model.set_photos([second], project_directory=project_directory)

    # Assert
    assert spy.count() == 2
    assert spy.at(0) == [project_directory / "a"]
    assert spy.at(1) == [project_directory / "b"]
