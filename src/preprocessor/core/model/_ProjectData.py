import csv
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from preprocessor.core.model import PhotoData, MetadataData
from preprocessor.model.project_path import ProjectPath


class ProjectData(BaseModel, validate_assignment=True):
    """A project with photos."""

    model_config = ConfigDict(
        extra="forbid",
    )

    project_file: Path | None = Field(default=None, exclude=True)
    """The file path where the project is or will be saved, or None. This field is not serialized/deserialized."""

    ################
    ## Properties ##
    ################

    photos: list[PhotoData] = []
    """The list of photos in the project."""
    photos_path: ProjectPath | None = None
    """The file path from which photos were last added, or None if not set."""
    export_path: ProjectPath | None = None
    """The file path where the photos will be exported to, or None if not set."""

    ##################
    ## IO functions ##
    ##################

    def to_json(self, project_dir: str | Path | None) -> str:
        """
        Save model data to a JSON string representation of the model.

        :param project_dir: The project directory used to resolve relative paths in the model.
        If None, relative paths are not resolved.
        """
        context = {"project_dir": Path(project_dir).resolve()} if project_dir is not None else {}
        return self.model_dump_json(
            context=context,
            indent=2,
            exclude_unset=True,
            exclude_defaults=True,
        )

    @classmethod
    def from_json(cls: type["ProjectData"], json_str: str, project_dir: str | Path | None) -> "ProjectData":
        """
        Load model data from a JSON string representation of the model.

        :param json_str: The JSON string to parse into the model.
        :param project_dir: The project directory used to resolve relative paths in the model.
        If None, relative paths are not resolved.
        :raises ValidationError: If the JSON data is invalid or incompatible with the model.
        """
        context = {"project_dir": Path(project_dir).resolve()} if project_dir is not None else {}
        new_data = ProjectData.model_validate_json(
            json_str,
            context=context,
        )
        return ProjectData.model_validate(new_data)

    @classmethod
    def load_from_file(cls: type["ProjectData"], project_file: str | Path) -> "ProjectData":
        """
        Load project JSON from the given file path and apply via deserialize().

        :param project_file: The file path to read the project JSON from.
        :raises FileNotFoundError: If the specified file does not exist.
        """
        p = Path(project_file)
        project_dir = p.parent.resolve() if p.parent else None
        if not p.exists():
            raise FileNotFoundError(str(p))
        with p.open("r", encoding="utf-8") as fh:
            json_str = fh.read()
        return cls.from_json(json_str, project_dir = project_dir)

    def save_to_file(self, project_file: str | Path) -> None:
        """
        Save the serialized project JSON to the given file path.
        Parent directories will be created if necessary.

        :param project_file: The file path to write the project JSON to.
        """
        p = Path(project_file)
        project_dir = p.parent.resolve() if p.parent else None
        if project_dir:
            project_dir.mkdir(parents=True, exist_ok=True)
        # Only then do we write out the changes
        json_str = self.to_json(project_dir=project_dir)
        with p.open("w", encoding="utf-8") as fh:
            fh.write(json_str)


    def write_to_csv_file(self, file: Path) -> None:
        """Write the metadata to a CSV file."""
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect="excel")
            writer.writerow(MetadataData.csv_headers())
            for photo in self.photos:
                md = photo.metadata
                writer.writerow(md.csv_row())