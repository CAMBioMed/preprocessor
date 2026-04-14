from typing import Iterable

from pydantic import BaseModel, ConfigDict

from preprocessor.core.model._MetadataData import MetadataData
from preprocessor.core.model._ColorCorrectionParams import ColorCorrectionParams
from preprocessor.core.model._LensCorrectionParams import LensCorrectionParams
from preprocessor.core.model._CropParams import CropParams
from preprocessor.core.model._ProjectPath import ProjectPath




class PhotoData(BaseModel, validate_assignment=True):
    """Parameters for photo processing."""

    model_config = ConfigDict(
        extra="forbid",
    )

    ######################
    ## Fixed properties ##
    ######################

    image_id: str
    """The unique identifier for the photo."""
    image_path: ProjectPath
    """The path to the photo file, relative to the project."""

    ######################
    ## Photo correction ##
    ######################

    color_correction: ColorCorrectionParams | None = None
    """The parameters for color correction, or None to not perform color correction."""
    lens_correction: LensCorrectionParams | None = None
    """The parameters for lens correction, or None to not perform lens correction."""
    crop: CropParams | None = None
    """The parameters for cropping the photo, or None to not crop the photo."""

    ##############
    ## Metadata ##
    ##############

    metadata: MetadataData = MetadataData()
    """The metadata for the photo."""

    @staticmethod
    def group_photos(photos: "Iterable[PhotoData]") -> "list[list[PhotoData]]":
        """Groups the photos in groups where the site, area, year, season, transect are the same."""
        groups: dict[tuple[str | None, str | None, str | None, str | None, str | None], list[PhotoData]] = {}
        for photo in photos:
            metadata = photo.metadata
            key = (metadata.site, metadata.area, str(metadata.date.year) if metadata.date else None, metadata.season, metadata.transect)
            if key not in groups:
                groups[key] = []
            groups[key].append(photo)
        return list(groups.values())

    def determine_filename(self, group_idx: int) -> str:
        """
        Determines the export filename of the photo with this metadata.

        :param group_idx: The index of the photo in its group (e.g. in its site, area, year, season, transect).
        :return: The export filename of the photo.
        """

        if self.metadata.filename is not None:
            return self.metadata.filename

        partner: str | None = self.metadata.partner
        area: str | None = self.metadata.area
        site: str | None = self.metadata.site
        year: str | None = str(self.metadata.date.year) if self.metadata.date is not None else None
        season: str | None = self.metadata.season
        transect: str | None = self.metadata.transect
        date: str | None = self.metadata.date.date().isoformat() if self.metadata.date is not None else None
        idx: str | None = f"{group_idx:03d}"
        ext: str = self.image_path.suffix.lower() if self.image_path.suffix else ".jpg"

        # Generate _ separated string of all the parts that are not None
        parts = [p for p in [partner, area, site, year, season, transect, date, idx] if p is not None]
        return "_".join(parts) + ext
