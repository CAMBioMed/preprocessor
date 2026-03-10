from datetime import datetime, timezone
from typing import Any, cast

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QDialog, QWidget, QLineEdit, QCheckBox, QPlainTextEdit, QDateTimeEdit

from preprocessor.gui.ui_metadata_dialog import Ui_MetadataDialog
from preprocessor.gui.utils import _dt_to_qdatetime
from preprocessor.model.metadata_model import MetadataModel
from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel

_DIFFERENT = object()
"""Marker object to denote a metadata field has various values across selected photos"""


class MetadataDialog(QDialog):
    current_project: ProjectModel
    selected_photos: list[PhotoModel]
    ui: Ui_MetadataDialog

    def __init__(
        self, current_project: ProjectModel, selected_photos: list[PhotoModel], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.current_project = current_project
        self.selected_photos = selected_photos
        self.ui = Ui_MetadataDialog()
        self.ui.setupUi(self)
        self._connect_signals()
        self._set_initial_state()

    def _connect_signals(self) -> None:
        self.ui.chkDate.checkStateChanged.connect(lambda: self._update_metadata_datetime("date"))
        self.ui.chkPartner.checkStateChanged.connect(lambda: self._update_metadata_textbox("partner"))
        self.ui.chkArea.checkStateChanged.connect(lambda: self._update_metadata_textbox("area"))
        self.ui.chkSite.checkStateChanged.connect(lambda: self._update_metadata_textbox("site"))
        self.ui.chkSeason.checkStateChanged.connect(lambda: self._update_metadata_textbox("season"))
        self.ui.chkTransect.checkStateChanged.connect(lambda: self._update_metadata_textbox("transect"))
        self.ui.chkHeight.checkStateChanged.connect(lambda: self._update_metadata_textbox("height"))
        self.ui.chkLatitude.checkStateChanged.connect(lambda: self._update_metadata_textbox("latitude"))
        self.ui.chkLongitude.checkStateChanged.connect(lambda: self._update_metadata_textbox("longitude"))
        self.ui.chkDepth.checkStateChanged.connect(lambda: self._update_metadata_textbox("depth"))
        self.ui.chkCamera.checkStateChanged.connect(lambda: self._update_metadata_textbox("camera"))
        self.ui.chkPhotographer.checkStateChanged.connect(lambda: self._update_metadata_textbox("photographer"))
        self.ui.chkWaterQuality.checkStateChanged.connect(lambda: self._update_metadata_textbox("water_quality"))
        self.ui.chkStrobes.checkStateChanged.connect(lambda: self._update_metadata_textbox("strobes"))
        self.ui.chkFraming.checkStateChanged.connect(lambda: self._update_metadata_textbox("framing"))
        self.ui.chkWhiteBalanceCard.checkStateChanged.connect(
            lambda: self._update_metadata_textbox("white_balance_card")
        )
        self.ui.chkComments.checkStateChanged.connect(lambda: self._update_metadata_plaintextedit("comments"))

        self.ui.btnCancel.clicked.connect(self.reject)
        self.ui.btnApply.clicked.connect(self._apply_changes)

    def _set_initial_state(self) -> None:
        self._initialize_metadata_datetime("date")
        self._initialize_metadata_textbox("partner")
        self._initialize_metadata_textbox("area")
        self._initialize_metadata_textbox("site")
        self._initialize_metadata_textbox("season")
        self._initialize_metadata_textbox("transect")
        self._initialize_metadata_textbox("height")
        self._initialize_metadata_textbox("latitude")
        self._initialize_metadata_textbox("longitude")
        self._initialize_metadata_textbox("depth")
        self._initialize_metadata_textbox("camera")
        self._initialize_metadata_textbox("photographer")
        self._initialize_metadata_textbox("water_quality")
        self._initialize_metadata_textbox("strobes")
        self._initialize_metadata_textbox("framing")
        self._initialize_metadata_textbox("white_balance_card")
        self._initialize_metadata_plaintextedit("comments")

    def _initialize_metadata_textbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        textbox: QLineEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            textbox.setText(str(common_value) if common_value is not None else "")
        else:
            checkbox.setChecked(False)
            textbox.setText("")
        self._update_metadata_textbox(field_name)

    def _initialize_metadata_plaintextedit(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        textbox: QPlainTextEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            textbox.setPlainText(str(common_value) if common_value is not None else "")
        else:
            checkbox.setChecked(False)
            textbox.setPlainText("")
        self._update_metadata_plaintextedit(field_name)

    def _initialize_metadata_datetime(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        datebox: QDateTimeEdit = getattr(self.ui, f"dte{field_name.capitalize()}")
        common_value = self._determine_common_metadata_value(field_name)

        if common_value is not _DIFFERENT:
            checkbox.setChecked(True)
            datebox.setDateTime(_dt_to_qdatetime(common_value))
        else:
            checkbox.setChecked(False)
            datebox.setDateTime(QDateTime())
        self._update_metadata_datetime(field_name)

    def _update_metadata_textbox(self, field_name: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        textbox: QLineEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
        common_textbox: QLineEdit = getattr(self.ui, f"txt{field_name.capitalize()}CommonValue")
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
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        textbox: QPlainTextEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
        common_textbox: QPlainTextEdit = getattr(self.ui, f"txt{field_name.capitalize()}CommonValue")
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
        checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
        datebox: QDateTimeEdit = getattr(self.ui, f"dte{field_name.capitalize()}")
        common_datebox: QDateTimeEdit = getattr(self.ui, f"dte{field_name.capitalize()}CommonValue")
        placeholder_textbox: QDateTimeEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
        overriding = checkbox.isChecked()

        common_value = self._determine_common_metadata_value(field_name)
        datebox.setVisible(overriding)
        common_datebox.setVisible(not overriding and common_value is not _DIFFERENT)
        placeholder_textbox.setVisible(not overriding and common_value is _DIFFERENT)
        common_datebox.setDateTime(_dt_to_qdatetime(common_value))

    def _determine_common_metadata_value(self, attr_name: str) -> Any | None:
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

    def _apply_changes(self) -> None:
        for field_name in [
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
        ]:
            checkbox: QCheckBox = getattr(self.ui, f"chk{field_name.capitalize()}")
            if checkbox.isChecked():
                new_value: Any
                if field_name == "comments":
                    plaintextedit: QPlainTextEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
                    new_value = plaintextedit.toPlainText()
                elif field_name == "date":
                    datebox: QDateTimeEdit = getattr(self.ui, f"dte{field_name.capitalize()}")
                    new_value = datebox.dateTime().toPython()
                else:
                    textbox: QLineEdit = getattr(self.ui, f"txt{field_name.capitalize()}")
                    new_value = textbox.text()
                for photo in self.selected_photos:
                    setattr(photo.metadata, field_name, new_value)
        self.accept()
