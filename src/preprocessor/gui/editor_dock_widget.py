from typing import ClassVar

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDockWidget, QWidget, QLineEdit, QLabel, QPlainTextEdit, QDateTimeEdit, QDoubleSpinBox

from preprocessor.gui.ui_editor_dock import Ui_EditorDock
from preprocessor.gui.utils import _dt_to_qdatetime
from preprocessor.model.photo_model import PhotoModel
from preprocessor.utils import to_upper_camel_case


class EditorDockWidget(QDockWidget):
    ui: Ui_EditorDock

    on_autodetect_quadrat_clicked: Signal = Signal()
    on_edit_metadata_clicked: Signal = Signal()

    current_photo: PhotoModel | None = None

    fields: ClassVar[list[str]] = [
        "date",
        "partner",
        "area",
        "site",
        "season",
        "transect",
        "height",
        "latitude",
        "longitude",
        "depth",
        "camera",
        "photographer",
        "water_quality",
        "strobes",
        "framing",
        "white_balance_card",
        "comments",
    ]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_EditorDock()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnCropping_QuadratAutodetect.clicked.connect(self.on_autodetect_quadrat_clicked.emit)
        self.ui.sldLensCorrection_Distortion.valueChanged.connect(self._handle_distortion_changed)
        self.ui.btnMetadataEdit.clicked.connect(self.on_edit_metadata_clicked.emit)

    def update_with_photo(self, photo: PhotoModel | None) -> None:
        """Update the editor fields with the data from the given photo model."""
        self.current_photo.on_metadata_changed.disconnect(self._handle_metadata_changed) if self.current_photo else None
        self.current_photo = photo
        self.current_photo.on_metadata_changed.connect(self._handle_metadata_changed) if self.current_photo else None

        enabled = photo is not None
        self.ui.btnCropping_QuadratAutodetect.setEnabled(enabled)
        self.ui.sldLensCorrection_Distortion.setEnabled(enabled)

        distortion = photo.distortion_coefficients[0] if photo and photo.distortion_coefficients else 0.0
        value = int(distortion * 100.0)  # Slider is scaled by 100 for better precision
        self.ui.sldLensCorrection_Distortion.setValue(value)

        self._update_metadata_fields()

    def _handle_metadata_changed(self) -> None:
        """Handle changes to the photo's metadata and update the editor fields."""
        self._update_metadata_fields()

    def _update_metadata_fields(self) -> None:
        # Update the metadata fields
        for field_name in self.fields:
            if field_name == "comments":
                self._display_metadata_plaintextedit(field_name)
            elif field_name == "date":
                self._display_metadata_datetime(field_name)
            elif field_name in {"latitude", "longitude"}:
                self._display_metadata_doublespinbox(field_name)
            else:
                self._display_metadata_textbox(field_name)

    def _display_metadata_plaintextedit(self, field_name: str) -> None:
        label: QLabel = getattr(self.ui, f"lblMetadata{to_upper_camel_case(field_name)}")
        textbox: QPlainTextEdit = getattr(self.ui, f"txtMetadata{to_upper_camel_case(field_name)}")
        value = getattr(self.current_photo.metadata, field_name, "") if self.current_photo else ""

        label.setVisible(bool(value))
        textbox.setVisible(bool(value))
        textbox.setPlainText(str(value))

    def _display_metadata_datetime(self, field_name: str) -> None:
        label: QLabel = getattr(self.ui, f"lblMetadata{to_upper_camel_case(field_name)}")
        datebox: QDateTimeEdit = getattr(self.ui, f"dteMetadata{to_upper_camel_case(field_name)}")
        value = getattr(self.current_photo.metadata, field_name, None) if self.current_photo else None

        label.setVisible(bool(value))
        datebox.setVisible(bool(value))
        datebox.setDateTime(_dt_to_qdatetime(value))

    def _display_metadata_doublespinbox(self, field_name: str) -> None:
        label: QLabel = getattr(self.ui, f"lblMetadata{to_upper_camel_case(field_name)}")
        spinbox: QDoubleSpinBox = getattr(self.ui, f"numMetadata{to_upper_camel_case(field_name)}")
        value = getattr(self.current_photo.metadata, field_name, None) if self.current_photo else None

        label.setVisible(bool(value))
        spinbox.setVisible(bool(value))
        spinbox.setValue(value if value is not None else 0.0)

    def _display_metadata_textbox(self, field_name: str) -> None:
        label: QLabel = getattr(self.ui, f"lblMetadata{to_upper_camel_case(field_name)}")
        textbox: QLineEdit = getattr(self.ui, f"txtMetadata{to_upper_camel_case(field_name)}")
        value = getattr(self.current_photo.metadata, field_name, "") if self.current_photo else ""

        label.setVisible(bool(value))
        textbox.setVisible(bool(value))
        textbox.setText(str(value))

    def _handle_distortion_changed(self, value: float) -> None:
        """Handle changes to the distortion slider and update the photo model."""
        if self.current_photo is None:
            return
        # Update the distortion coefficient k1 in the photo model (k1, k2, p1, p2, k3, ...)
        current_distortion = self.current_photo.distortion_coefficients or [0.0, 0.0, 0.0, 0.0, 0.0]
        k1 = float(value) / 100.0  # Slider is scaled by 100 for better precision
        new_distortion = [k1, *current_distortion[1:]]  # Update k1, keep the rest unchanged
        self.current_photo.distortion_coefficients = new_distortion
