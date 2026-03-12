from pathlib import Path
from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QPlainTextEdit
from pytestqt.qtbot import QtBot

from preprocessor.gui.metadata_dialog import MetadataDialog
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.photo_model import PhotoModel


def _make_photo(metadata: dict[str, Any] | None = None) -> PhotoModel:
    # Create a minimal PhotoModel with a given metadata dict
    data = {
        "original_filename": Path("IMG_TEST.JPG"),
        "width": 10,
        "height": 10,
    }
    if metadata is not None:
        data["metadata"] = metadata
    return PhotoModel(data=data)


def test_metadata_dialog_copy_from_current_and_apply(qtbot: QtBot) -> None:
    """Copy metadata from the current photo into the dialog and apply to selected photos."""
    app_model: ApplicationModel = ApplicationModel()

    # Create a current photo with metadata
    current_meta: dict[str, str] = {
        "photographer": "Alice",
        "camera": "Canon EOS 5D",
        "comments": "A sample comment",
    }
    current_photo: PhotoModel = _make_photo(metadata=current_meta)
    app_model.current_photo = current_photo

    # Create a target photo with empty metadata
    target_photo: PhotoModel = _make_photo(metadata={})

    dlg: MetadataDialog = MetadataDialog(app_model, [target_photo])
    qtbot.addWidget(dlg)

    # Ensure the Copy From Current Photo button is enabled and click it
    assert dlg.ui.btnCopyFromCurrentPhoto.isEnabled()
    qtbot.mouseClick(dlg.ui.btnCopyFromCurrentPhoto, Qt.MouseButton.LeftButton)

    # After copying, the text fields should contain the values from current_photo
    txt_photographer: QLineEdit = dlg.ui.txtPhotographer
    txt_camera: QLineEdit = dlg.ui.txtCamera
    txt_comments: QPlainTextEdit = dlg.ui.txtComments

    assert txt_photographer.text() == "Alice"
    assert txt_camera.text() == "Canon EOS 5D"
    assert txt_comments.toPlainText() == "A sample comment"

    # Click Apply to write changes back to the selected photo(s)
    qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

    # The selected target photo's metadata should now be updated
    assert target_photo.metadata.photographer == "Alice"
    assert target_photo.metadata.camera == "Canon EOS 5D"
    assert target_photo.metadata.comments == "A sample comment"


def test_metadata_dialog_apply_to_multiple_photos(qtbot: QtBot) -> None:
    """Apply common metadata to multiple selected photos."""
    app_model: ApplicationModel = ApplicationModel()

    # No current photo needed here
    photo1: PhotoModel = _make_photo(metadata={})
    photo2: PhotoModel = _make_photo(metadata={})

    dlg: MetadataDialog = MetadataDialog(app_model, [photo1, photo2])
    qtbot.addWidget(dlg)

    # Manually set the controls for partner and area
    # Check the boxes to indicate we want to set these fields
    dlg.ui.chkPartner.setChecked(True)
    dlg.ui.txtPartner.setText("PartnerX")
    dlg.ui.chkArea.setChecked(True)
    dlg.ui.txtArea.setText("AreaY")

    # Apply changes
    qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

    assert photo1.metadata.partner == "PartnerX"
    assert photo2.metadata.partner == "PartnerX"
    assert photo1.metadata.area == "AreaY"
    assert photo2.metadata.area == "AreaY"
