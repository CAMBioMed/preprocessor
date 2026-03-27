from pathlib import Path

from preprocessor.gui.qjobs import QJob
from preprocessor.model.photo_model import PhotoModel
from preprocessor.processing.fix_perspective import fix_perspective
from preprocessor.processing.load_image import load_image
from preprocessor.processing.save_image import save_image
from preprocessor.processing.undistort import undistort_photo


class ExportPhotoJob(QJob):
    photo: PhotoModel
    idx: int
    export_path: Path

    def __init__(self, photo: PhotoModel, idx: int, export_path: Path) -> None:
        super().__init__(name=photo.original_filename.name)
        self.photo = photo
        self.idx = idx
        self.export_path = export_path

    def process(self) -> None:
        # Prepare names/paths
        output_name = self.photo.output_filename(self.idx)
        output_path = self.export_path / output_name
        original_name = self.photo.original_filename.name
        self.update_status(f"Exporting to {output_name}...")

        # Prefer undistorted image when available. If undistort was canceled, stop export
        img = None
        try:
            # Provide a stop_checker callable so undistort_photo can cancel early
            img = undistort_photo(
                self.photo, progress_callback=None, stop_checker=self.cancel_token.is_cancelled
            )
        except Exception:
            # TODO: Append errors to status message
            # self.message.emit("error", f"Lens correction failed for {original_name}: {e}")
            # self.progress.emit(idx, total)
            img = None

        self.assert_not_cancelled()

        # If the lens correction failed, fall back to loading the original image
        if img is None:
            original_path = self.photo.original_filename
            img = load_image(str(original_path))

        if img is None:
            # Couldn't load image (either undistort failed & load failed)
            original_path = self.photo.original_filename
            self.update_status(f"Failed to load image: {original_path}")
            return

        self.assert_not_cancelled()

        # Ensure quadrat corners are set
        if self.photo.quadrat_corners:
            # Process perspective; guard against processing errors
            try:
                final_img = fix_perspective(
                    img,
                    list(self.photo.quadrat_corners),
                )
            except Exception as e:
                self.update_status(f"Processing failed for {original_name}: {e}", "error")
                return
        else:
            # No quadrat corners, skip perspective correction but still export the image
            final_img = img
            self.update_status(f"Quadrat corners not set for: {original_name}", "warning")

        # Save result
        ok = save_image(output_path, final_img)
        if not ok:
            self.update_status(f"Failed to save {original_name} to {output_path}", "error")
            return
