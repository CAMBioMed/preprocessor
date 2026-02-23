from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.ui_editor_dock import Ui_EditorDock
from preprocessor.model.photo_model import PhotoModel


class EditorDockWidget(QDockWidget):
    ui: Ui_EditorDock

    on_autodetect_quadrat_clicked: Signal = Signal()

    current_photo: PhotoModel | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_EditorDock()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnCropping_QuadratAutodetect.clicked.connect(self.on_autodetect_quadrat_clicked.emit)
        self.ui.sldLensCorrection_Distortion.valueChanged.connect(self._handle_distortion_changed)

    def update_with_photo(self, photo: PhotoModel | None) -> None:
        """Update the editor fields with the data from the given photo model."""
        self.current_photo = photo

        enabled = photo is not None
        self.ui.btnCropping_QuadratAutodetect.setEnabled(enabled)
        self.ui.sldLensCorrection_Distortion.setEnabled(enabled)

        distortion = photo.distortion_coefficients[0] if photo and photo.distortion_coefficients else 0.0
        value = int(distortion * 100.0)  # Slider is scaled by 100 for better precision
        self.ui.sldLensCorrection_Distortion.setValue(value)

    def _handle_distortion_changed(self, value: float) -> None:
        """Handle changes to the distortion slider and update the photo model."""
        if self.current_photo is None:
            return
        # Update the distortion coefficient k1 in the photo model (k1, k2, p1, p2, k3, ...)
        current_distortion = self.current_photo.distortion_coefficients or [0.0, 0.0, 0.0, 0.0, 0.0]
        k1 = float(value) / 100.0  # Slider is scaled by 100 for better precision
        new_distortion = [k1, *current_distortion[1:]]  # Update k1, keep the rest unchanged
        self.current_photo.distortion_coefficients = new_distortion
