from datetime import datetime
from typing import Any, ClassVar

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QDialog, QWidget, QLineEdit, QCheckBox, QPlainTextEdit, QDateTimeEdit, QDoubleSpinBox

from preprocessor.gui.ui_metadata_dialog import Ui_MetadataDialog
from preprocessor.gui.utils import _dt_to_qdatetime
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.photo_model import PhotoModel
from preprocessor.utils import to_upper_camel_case

_DIFFERENT = object()
"""Marker object to denote a metadata field has various values across selected photos"""


class MetadataDialog(QDialog):
    application_model: ApplicationModel
    selected_photos: list[PhotoModel]
    ui: Ui_MetadataDialog

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

    def __init__(
        self, application_model: ApplicationModel, selected_photos: list[PhotoModel], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.application_model = application_model
        self.selected_photos = selected_photos
        self.ui = Ui_MetadataDialog()
        self.ui.setupUi(self)
        self._connect_signals()
        self._set_initial_state()

    def _connect_signals(self) -> None:
        for field_name in self.fields:
            checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
            if field_name == "comments":
                checkbox.checkStateChanged.connect(lambda _, fn=field_name: self._update_metadata_plaintextedit(fn))
            elif field_name == "date":
                checkbox.checkStateChanged.connect(lambda _, fn=field_name: self._update_metadata_datetime(fn))
            elif field_name in ["latitude", "longitude"]:
                checkbox.checkStateChanged.connect(lambda _, fn=field_name: self._update_metadata_doublespinbox(fn))
            else:
                checkbox.checkStateChanged.connect(lambda _, fn=field_name: self._update_metadata_textbox(fn))

        self.ui.btnCopyFromCurrentPhoto.clicked.connect(self._handle_copy_from_current_photo)
        self.ui.btnCancel.clicked.connect(self.reject)
        self.ui.btnApply.clicked.connect(self._apply_changes)

    def _set_initial_state(self) -> None:
        for field_name in self.fields:
            if field_name == "comments":
                self._initialize_metadata_plaintextedit(field_name)
            elif field_name == "date":
                self._initialize_metadata_datetime(field_name)
            elif field_name in ["latitude", "longitude"]:
                self._initialize_metadata_doublespinbox(field_name)
            else:
                self._initialize_metadata_textbox(field_name)
        selected_photo_count = len(self.selected_photos)
        all_photo_count = len(self.application_model.current_project.photos)
        has_current_photo = self.application_model.current_photo is not None
        if selected_photo_count == 1:
            self.ui.lblSelection.setText(f"1/{all_photo_count}: {self.selected_photos[0].name}")
            self.ui.btnCopyFromCurrentPhoto.setEnabled(
                has_current_photo and self.selected_photos[0] != self.application_model.current_photo
            )
        else:
            self.ui.lblSelection.setText(f"{selected_photo_count}/{all_photo_count} photos selected")
            self.ui.btnCopyFromCurrentPhoto.setEnabled(has_current_photo)

    def _initialize_metadata_textbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        textbox: QLineEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not None and common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            textbox.setText(str(common_value) if common_value is not None else "")
        else:
            checkbox.setChecked(False)
            textbox.setText("")
        self._update_metadata_textbox(field_name)

    def _initialize_metadata_plaintextedit(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        textbox: QPlainTextEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not None and common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            textbox.setPlainText(str(common_value) if common_value is not None else "")
        else:
            checkbox.setChecked(False)
            textbox.setPlainText("")
        self._update_metadata_plaintextedit(field_name)

    def _initialize_metadata_datetime(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        datebox: QDateTimeEdit = getattr(self.ui, f"dte{to_upper_camel_case(field_name)}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not None and common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            datebox.setDateTime(_dt_to_qdatetime(common_value))
        else:
            checkbox.setChecked(False)
            datebox.setDateTime(QDateTime())
        self._update_metadata_datetime(field_name)


    def _initialize_metadata_doublespinbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        spinbox: QDoubleSpinBox = getattr(self.ui, f"num{to_upper_camel_case(field_name)}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not None and common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            spinbox.setValue(common_value)
        else:
            checkbox.setChecked(False)
            spinbox.setValue(0.0)
        self._update_metadata_doublespinbox(field_name)

    def _update_metadata_textbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        textbox: QLineEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
        common_textbox: QLineEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}CommonValue")
        overriding = checkbox.isChecked()

        common_value = self._determine_common_metadata_value(field_name)
        placeholder = (
            "(various)" if common_value is _DIFFERENT else str(common_value) if common_value is not None else ""
        )
        textbox.setPlaceholderText(placeholder)
        common_textbox.setPlaceholderText(placeholder)

        textbox.setVisible(overriding)
        common_textbox.setVisible(not overriding)

    def _update_metadata_plaintextedit(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        textbox: QPlainTextEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
        common_textbox: QPlainTextEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}CommonValue")
        overriding = checkbox.isChecked()

        common_value = self._determine_common_metadata_value(field_name)
        placeholder = (
            "(various)" if common_value is _DIFFERENT else str(common_value) if common_value is not None else ""
        )
        textbox.setPlaceholderText(placeholder)
        common_textbox.setPlaceholderText(placeholder)

        textbox.setVisible(overriding)
        common_textbox.setVisible(not overriding)

    def _update_metadata_datetime(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        datebox: QDateTimeEdit = getattr(self.ui, f"dte{to_upper_camel_case(field_name)}")
        common_datebox: QDateTimeEdit = getattr(self.ui, f"dte{to_upper_camel_case(field_name)}CommonValue")
        various_textbox: QDateTimeEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}Various")
        overriding = checkbox.isChecked()

        common_value = self._determine_common_metadata_value(field_name)
        datebox.setVisible(overriding)
        common_datebox.setVisible(not overriding and common_value is not _DIFFERENT)
        various_textbox.setVisible(not overriding and common_value is _DIFFERENT)
        common_datebox.setDateTime(_dt_to_qdatetime(common_value) if common_value is not _DIFFERENT and common_value is not None else QDateTime())

    def _update_metadata_doublespinbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
        spinbox: QDoubleSpinBox = getattr(self.ui, f"num{to_upper_camel_case(field_name)}")
        common_spinbox: QDoubleSpinBox = getattr(self.ui, f"num{to_upper_camel_case(field_name)}CommonValue")
        various_textbox: QDoubleSpinBox = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}Various")
        overriding = checkbox.isChecked()

        common_value = self._determine_common_metadata_value(field_name)
        spinbox.setVisible(overriding)
        common_spinbox.setVisible(not overriding and common_value is not _DIFFERENT)
        various_textbox.setVisible(not overriding and common_value is _DIFFERENT)
        common_spinbox.setValue(common_value if common_value is not _DIFFERENT and common_value is not None else 0.0)

    def _determine_common_metadata_value(self, attr_name: str) -> Any | None:  # noqa: ANN401
        """
        Return the value of `attr_name` from metadata if all selected photos share the same value,
        otherwise return None. Attributes are not nested, so use getattr on metadata.
        """
        if not self.selected_photos:
            return None
        first_val = getattr(self.selected_photos[0].metadata, attr_name, None)
        for p in self.selected_photos:
            if getattr(p.metadata, attr_name, None) != first_val:
                return _DIFFERENT
        return first_val

    def _handle_copy_from_current_photo(self) -> None:
        current_photo = self.application_model.current_photo
        if not current_photo:
            return
        for field_name in self.fields:
            checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
            checkbox.setChecked(True)
            value = getattr(current_photo.metadata, field_name, None)
            if field_name == "comments":
                textbox: QPlainTextEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
                textbox.setPlainText(str(value) if value is not None else "")
            elif field_name == "date":
                datebox: QDateTimeEdit = getattr(self.ui, f"dte{to_upper_camel_case(field_name)}")
                if isinstance(value, datetime):
                    datebox.setDateTime(_dt_to_qdatetime(value))
                else:
                    datebox.setDateTime(QDateTime())
            else:
                lineedit: QLineEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
                lineedit.setText(str(value) if value is not None else "")

    def _apply_changes(self) -> None:
        for field_name in self.fields:
            checkbox: QCheckBox = getattr(self.ui, f"chk{to_upper_camel_case(field_name)}")
            if checkbox.isChecked():
                new_value: Any
                if field_name == "comments":
                    plaintextedit: QPlainTextEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
                    new_value = plaintextedit.toPlainText()
                elif field_name == "date":
                    datebox: QDateTimeEdit = getattr(self.ui, f"dte{to_upper_camel_case(field_name)}")
                    new_value = datebox.dateTime().toPython()
                elif field_name in ["latitude", "longitude"]:
                    spinbox: QDoubleSpinBox = getattr(self.ui, f"num{to_upper_camel_case(field_name)}")
                    new_value = spinbox.value()
                else:
                    textbox: QLineEdit = getattr(self.ui, f"txt{to_upper_camel_case(field_name)}")
                    new_value = textbox.text()
                for photo in self.selected_photos:
                    setattr(photo.metadata, field_name, new_value)
        self.accept()
