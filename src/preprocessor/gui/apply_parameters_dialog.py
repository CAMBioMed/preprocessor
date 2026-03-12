from PySide6.QtWidgets import QDialog, QWidget, QCheckBox

from preprocessor.gui.ui_apply_parameters_dialog import Ui_ApplyParametersDialog
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.photo_model import PhotoModel


class ApplyParametersDialog(QDialog):
    application_model: ApplicationModel
    selected_photos: list[PhotoModel]
    ui: Ui_ApplyParametersDialog

    def __init__(
        self, application_model: ApplicationModel, selected_photos: list[PhotoModel], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.application_model = application_model
        self.selected_photos = selected_photos
        self.ui = Ui_ApplyParametersDialog()
        self.ui.setupUi(self)
        self.ui.chkColorCorrection.setEnabled(False)  # Not implemented yet
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnCancel.clicked.connect(self.reject)
        self.ui.btnApply.clicked.connect(self._apply_changes)

    def _apply_changes(self) -> None:
        current_photo = self.application_model.current_photo
        if not current_photo:
            return

        copy_color_correction = self.ui.chkColorCorrection.isChecked()
        copy_camera = self.ui.chkCamera.isChecked()
        copy_lens_correction = self.ui.chkLensCorrection.isChecked()
        copy_crop = self.ui.chkCrop.isChecked()

        for photo in self.selected_photos:
            if copy_color_correction:
                # Not implemented yet
                pass
            if copy_camera:
                photo.camera_matrix = current_photo.camera_matrix
            if copy_lens_correction:
                photo.distortion_coefficients = current_photo.distortion_coefficients
            if copy_crop:
                photo.quadrat_corners = current_photo.quadrat_corners
        self.accept()
