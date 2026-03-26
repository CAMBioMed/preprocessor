
from pathlib import Path

import pytest

from preprocessor.model.project_path import ProjectPath


class TestProjectPath:
    """Tests for the ProjectPath class."""

    def test_init_requires_absolute_path(self) -> None:
        """Should raise an error, when initializing a ProjectPath with a relative path."""
        # Arrange
        relative = Path("some/relative/path.jpg")

        # Act / Assert
        with pytest.raises(ValueError):
            ProjectPath(relative, None)

    def test_path_returns_relative_path_when_resource_is_inside_project_dir(self, tmp_path: Path) -> None:
        """Should return the path relative to the project directory, when the resource is inside the project directory."""
        # Arrange
        project_dir = tmp_path / "project"
        resource = project_dir / "images" / "img.jpg"

        # Act
        pp = ProjectPath(resource, project_dir)

        # Assert: stored path is relative to the project dir
        assert not pp.path.is_absolute()
        assert pp.path == Path("images") / "img.jpg"
        # And as_absolute returns the original absolute path
        assert pp.as_absolute() == resource.resolve()

    def test_path_returns_absolute_path_when_resource_is_outside_project_dir(self, tmp_path: Path) -> None:
        """Should return the absolute path, when the resource is outside the project directory."""
        # Arrange
        project_dir = tmp_path / "project"

        resource = tmp_path / "other" / "img.jpg"

        # Act
        pp = ProjectPath(resource, project_dir)

        # Assert: stored path remains absolute and as_absolute returns the resource
        assert pp.path.is_absolute()
        assert pp.path == resource
        assert pp.as_absolute() == resource.resolve()

    def test_path_returns_absolute_path_when_project_dir_is_none(self, tmp_path: Path) -> None:
        """Should return the absolute path, when the project directory is None."""
        # Arrange
        resource = tmp_path / "img.jpg"

        # Act
        pp = ProjectPath(resource, None)

        # Assert
        assert pp.path.is_absolute()
        assert pp.as_absolute() == resource.resolve()

    def test_update_with_same_project_dir_returns_equivalent_path(self, tmp_path: Path) -> None:
        # Arrange
        project_dir = tmp_path / "project"
        resource = project_dir / "images" / "img.jpg"
        resource.parent.mkdir(parents=True)
        resource.write_text("x")

        pp = ProjectPath(resource, project_dir)

        # Act
        updated = pp.update(project_dir)

        # Assert: should be the same as original
        assert updated.path == pp.path
        assert updated.as_absolute() == pp.as_absolute()

    def test_update_to_inside_project_dir_makes_path_relative(self, tmp_path: Path) -> None:
        """Should store the path as relative, when the resource is inside the new project directory."""
        # Arrange
        project1 = tmp_path / "project1"
        project2 = tmp_path / "project2"
        project2_img = project2 / "images" / "img.jpg"
        project2_img.parent.mkdir(parents=True)
        project2_img.write_text("x")

        pp = ProjectPath(project2_img, None)

        # Act: update to a project dir that contains the resource
        updated = pp.update(project2)

        # Assert: should still resolve to the same absolute path
        assert updated.as_absolute() == pp.as_absolute()
        # But should now be stored as a relative path since it's inside project2
        assert not updated.path.is_absolute()
        assert updated.path == Path("images") / "img.jpg"

    def test_update_to_outside_project_dir_makes_path_absolute(self, tmp_path: Path) -> None:
        """Should store the path as absolute, when the resource is not in the new project directory."""
        # Arrange
        project1 = tmp_path / "project1"
        project2 = tmp_path / "project2"
        project1_img = project1 / "images" / "img.jpg"
        project1_img.parent.mkdir(parents=True)
        project1_img.write_text("x")

        pp = ProjectPath(project1_img, project1)

        # Act: update to a different project dir
        updated = pp.update(project2)

        # Assert: should still resolve to the same absolute path
        assert updated.as_absolute() == pp.as_absolute()
        # But should now be relative to project2, which means it should be stored as an absolute path since it's outside of project2
        assert updated.path.is_absolute()
        assert updated.path == project1_img

    def test_update_to_none_makes_path_absolute(self, tmp_path: Path) -> None:
        """Should store the path as absolute, when the new project directory is None."""
        # Arrange
        project_dir = tmp_path / "project"
        resource = project_dir / "images" / "img.jpg"
        resource.parent.mkdir(parents=True)
        resource.write_text("x")

        pp = ProjectPath(resource, project_dir)

        # Act: update to None
        updated = pp.update(None)

        # Assert: should still resolve to the same absolute path
        assert updated.as_absolute() == pp.as_absolute()
        # But should now be stored as an absolute path since there's no project dir
        assert updated.path.is_absolute()
        assert updated.path == resource
