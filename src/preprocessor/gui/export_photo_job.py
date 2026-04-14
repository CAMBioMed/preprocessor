from pathlib import Path

from preprocessor.core.model import PhotoData
from preprocessor.core.transform import lens_correct_transform, perspective_crop_transform
from preprocessor.core.transform.lens_correct_transform import LensCorrectTransform
from preprocessor.core.transform.perspective_crop_transform import PerspectiveCropTransform
from preprocessor.core.transform.transform_image import transform_image
from preprocessor.gui.qjobs import QJob
from preprocessor.processing.fix_perspective import fix_perspective
from preprocessor.processing.load_image import load_image
from preprocessor.processing.save_image import save_image
from preprocessor.processing.undistort import undistort_photo


class ExportPhotoJob(QJob):
    photo: PhotoData
    group_idx: int
    export_path: Path

    def __init__(self, photo: PhotoData, group_idx: int, export_path: Path) -> None:
        super().__init__(name=photo.original_filename.name)
        self.photo = photo
        self.group_idx = group_idx
        self.export_path = export_path

    def process(self) -> None:
        # Prepare names/paths
        output_name = self.photo.determine_filename(self.group_idx)
        output_path = self.export_path / output_name
        self.update_status(f"Exporting to {output_name}...")

        transform_image(
            self.photo.original_filename,
            self.photo,
            output_path,
            transforms=[
                # TODO: Add color correction transform once implemented
                LensCorrectTransform(),
                PerspectiveCropTransform(),
            ],
            messages=self.reporter,
            progress=self.reporter,
        )
