"""Top-level project models and metadata resolution helpers."""

from pathlib import Path
from typing import Self
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from preprocessor.core.serialization.folder import Folder
from preprocessor.core.serialization.metadata_csv_writer import MetadataCsvWriter
from preprocessor.core.serialization.photo_container import PhotoContainer


def _project_context(project_dir: str | Path | None) -> dict[str, Path]:
    """Build validation and serialization context for project paths."""

    if project_dir is None:
        return {}
    return {"project_dir": Path(project_dir).resolve()}


class Project(PhotoContainer):
    """A project containing top-level photos and a folder tree."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(
        description="The unique identifier for this project.",
    )
    name: str = Field(
        description="The display name of the project.",
    )

    def to_json(self, project_dir: str | Path | None = None) -> str:
        """
        Serialize the project to JSON.

        :param project_dir: The project directory used to serialize paths relative to that directory.
            If None, paths are serialized as stored.
        :return: The serialized project JSON.
        """

        return self.model_dump_json(
            indent=2,
            context=_project_context(project_dir),
            exclude_unset=True,
            exclude_defaults=True,
        )

    @classmethod
    def from_json(
        cls: type["Project"],
        json_str: str,
        project_dir: str | Path | None = None,
    ) -> "Project":
        """
        Load a project from its JSON representation.

        :param json_str: The JSON string to parse into the project.
        :param project_dir: The project directory used to resolve relative paths.
            If None, relative paths are not resolved.
        :raises ValidationError: If the JSON data is invalid or incompatible with the project model.
        """

        new_project = cls.model_validate_json(
            json_str,
            context=_project_context(project_dir),
        )
        return cls.model_validate(new_project)

    @classmethod
    def load_from_file(cls, project_file: str | Path) -> "Project":
        """
        Load project JSON from the given file path.

        :param project_file: The file path to read the project JSON from.
        :raises FileNotFoundError: If the specified file does not exist.
        """

        path = Path(project_file)
        project_dir = path.parent.resolve() if path.parent else None
        if not path.exists():
            raise FileNotFoundError(str(path))
        with path.open("r", encoding="utf-8") as fh:
            json_str = fh.read()
        return cls.from_json(json_str, project_dir=project_dir)

    def save_to_file(self, project_file: str | Path) -> None:
        """
        Save the project JSON to the given file path.

        Parent directories are created if necessary.

        :param project_file: The file path to write the project JSON to.
        """

        path = Path(project_file)
        project_dir = path.parent.resolve() if path.parent else None
        if project_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        # Only then do we write out the changes
        json_str = self.to_json(project_dir=project_dir)
        with path.open("w", encoding="utf-8") as fh:
            fh.write(json_str)

    def write_to_csv_file(self, file: Path) -> None:
        """
        Write photo metadata to a CSV file.

        Metadata inherited from the project and folder hierarchy is included
        for each photo. Unknown metadata fields are ignored because the CSV
        format is defined by :class:`MetadataCsvWriter`.

        :param file: The CSV file path to write.
        """

        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("w", newline="", encoding="utf-8") as csvfile:
            writer = MetadataCsvWriter(csvfile)
            for _, metadata in self.iter_photos_with_metadata():
                writer.write_row(metadata)

    @model_validator(mode="after")
    def validate_unique_identifiers(self) -> Self:
        """Reject duplicate folder UUIDs and duplicate photo IDs."""

        folder_ids: set[UUID] = set()
        for folder in self.iter_folders():
            if folder.id in folder_ids:
                msg = f"duplicate folder id: {folder.id}"
                raise ValueError(msg)
            folder_ids.add(folder.id)

        photo_ids: set[str] = set()
        for photo in self.iter_photos():
            if photo.id in photo_ids:
                msg = f"duplicate photo id: {photo.id}"
                raise ValueError(msg)
            photo_ids.add(photo.id)

        return self


Project.model_rebuild(_types_namespace={"Folder": Folder})
