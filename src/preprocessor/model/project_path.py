from pathlib import Path


class ProjectPath:
    """A path to a resource relative to the project file."""

    _project_dir: Path | None
    _path: Path

    def __init__(self, absolute_path: str | Path, project_dir: str | Path | None):
        """
        Initializes a ProjectPath.

        :param absolute_path: The absolute path to the resource.
        :param project_dir: The directory of the project file.
        """
        self._project_dir = Path(project_dir) if project_dir is not None else None

        # Store the path as absolute
        self._path = Path(absolute_path)
        if not self._path.is_absolute():
            raise ValueError("Path must be absolute.")

        # If we can store the path as relative to the project directory, let's do it. Otherwise, leave it unchanged.
        if self._project_dir is not None:
            try:
                self._path = self._path.relative_to(self._project_dir.resolve(), walk_up=False)
            except ValueError:
                # Unchanged
                pass

    def as_absolute(self) -> Path:
        """Returns the absolute path to the resource, resolving relative to the project directory if necessary."""
        if self._project_dir is None:
            return self._path.resolve()
        else:
            return (self._project_dir / self._path).resolve()

    @property
    def path(self) -> Path:
        """Returns the stored path, which is relative to the project directory if possible; otherwise, absolute."""
        return self._path

    def update(self, new_project_dir: str | Path | None) -> 'ProjectPath':
        """Returns a new ProjectPath with the same absolute path but updated to be relative to the new project directory if possible."""
        return ProjectPath(self.as_absolute(), new_project_dir)
