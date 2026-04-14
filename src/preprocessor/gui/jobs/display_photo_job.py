from pathlib import Path

from preprocessor.core.model import PhotoData
from preprocessor.core.transform.lens_correct_transform import LensCorrectTransform
from preprocessor.core.transform.perspective_crop_transform import PerspectiveCropTransform
from preprocessor.core.transform.transform_image import transform_image
from preprocessor.core.types import ImageRGB
from preprocessor.gui.jobs.qjobs import QJob


class DisplayPhotoJob(QJob):
    """Job that applies the transformations to the photo to display it."""

    photo: PhotoData

    def __init__(self, photo: PhotoData) -> None:
        super().__init__(name=photo.original_filename.name)
        self.photo = photo

    def process(self) -> ImageRGB | None:
        self.update_status(f"Displaying...")

        new_img = transform_image(
            self.photo.original_filename,
            self.photo,
            None,
            transforms=[
                # TODO: Add color correction transform once implemented
                LensCorrectTransform(),
                # NOTE: We don't do PerspectiveCropTransform, because we want to display the image uncropped
            ],
            messages=self.reporter,
            progress=self.reporter,
        )

        return new_img
