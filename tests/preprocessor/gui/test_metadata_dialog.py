from datetime import datetime
from pathlib import Path
from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QDateTimeEdit, QDoubleSpinBox, QSpinBox
from pytestqt.qtbot import QtBot

from preprocessor.gui.metadata_dialog import MetadataDialog
from preprocessor.gui.model._QApplicationState import QApplicationState
from preprocessor.gui.model._QPhotoModel import QPhotoModel

from preprocessor.gui.utils import _dt_to_qdatetime


def _make_photo(metadata: dict[str, Any] | None = None) -> QPhotoModel:
    # Create a minimal QPhotoModel with a given metadata dict
    data: dict[str, Any] = {
        "image_id": "test_photo",
        "original_filename": Path("IMG_TEST.JPG").resolve(),
    }
    if metadata is not None:
        data["metadata"] = metadata
    return QPhotoModel(data=data)


def test_metadata_dialog_copy_from_current_and_apply(qtbot: QtBot) -> None:
    """Copy metadata from the current photo into the dialog and apply to selected photos."""
    with qtbot.capture_exceptions():
        app_model: QApplicationState = QApplicationState()

        # Create a current photo with metadata
        current_meta: dict[str, object] = {
            "date": datetime.fromisoformat("2024-06-01T12:00:00"),
            "partner": "PartnerA",
            "area": "Area1",
            "site": "SiteX",
            "season": "Season2024",
            "transect": "Transect5",
            "height": 10,
            "latitude": 45.0,
            "longitude": -120.0,
            "depth": "5m",
            "camera": "Canon EOS 5D",
            "photographer": "Alice",
            "water_quality": "Clear",
            "strobes": "On",
            "framing": "Tight",
            "white_balance_card": "Yes",
            "comments": "A sample comment",
        }
        current_photo: QPhotoModel = _make_photo(metadata=current_meta)
        app_model.current_photo = current_photo

        # Create a target photo with empty metadata
        target_photo: QPhotoModel = _make_photo(metadata={})

        dlg: MetadataDialog = MetadataDialog(app_model, [target_photo])
        qtbot.addWidget(dlg)

        # Ensure the Copy From Current Photo button is enabled and click it
        assert dlg.ui.btnCopyFromCurrentPhoto.isEnabled()
        qtbot.mouseClick(dlg.ui.btnCopyFromCurrentPhoto, Qt.MouseButton.LeftButton)

        # After copying, the text fields should contain the values from current_photo
        dte_date: QDateTimeEdit = dlg.ui.dteDate
        txt_partner: QLineEdit = dlg.ui.txtPartner
        txt_area: QLineEdit = dlg.ui.txtArea
        txt_site: QLineEdit = dlg.ui.txtSite
        txt_season: QLineEdit = dlg.ui.txtSeason
        txt_transect: QLineEdit = dlg.ui.txtTransect
        txt_height: QSpinBox = dlg.ui.numHeight
        txt_latitude: QDoubleSpinBox = dlg.ui.numLatitude
        txt_longitude: QDoubleSpinBox = dlg.ui.numLongitude
        txt_depth: QLineEdit = dlg.ui.txtDepth
        txt_camera: QLineEdit = dlg.ui.txtCamera
        txt_photographer: QLineEdit = dlg.ui.txtPhotographer
        txt_water_quality: QLineEdit = dlg.ui.txtWaterQuality
        txt_strobes: QLineEdit = dlg.ui.txtStrobes
        txt_framing: QLineEdit = dlg.ui.txtFraming
        txt_white_balance_card: QLineEdit = dlg.ui.txtWhiteBalanceCard
        txt_comments: QLineEdit = dlg.ui.txtComments

        assert dte_date.dateTime().toPython() == datetime.fromisoformat("2024-06-01T12:00:00")
        assert txt_partner.text() == "PartnerA"
        assert txt_area.text() == "Area1"
        assert txt_site.text() == "SiteX"
        assert txt_season.text() == "Season2024"
        assert txt_transect.text() == "Transect5"
        assert txt_height.value() == 10
        assert txt_latitude.value() == 45.0
        assert txt_longitude.value() == -120.0
        assert txt_depth.text() == "5m"
        assert txt_camera.text() == "Canon EOS 5D"
        assert txt_photographer.text() == "Alice"
        assert txt_water_quality.text() == "Clear"
        assert txt_strobes.text() == "On"
        assert txt_framing.text() == "Tight"
        assert txt_white_balance_card.text() == "Yes"
        assert txt_comments.text() == "A sample comment"

        # Click Apply to write changes back to the selected photo(s)
        qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

        # The selected target photo's metadata should now be updated
        assert target_photo.metadata.date == datetime.fromisoformat("2024-06-01T12:00:00")
        assert target_photo.metadata.partner == "PartnerA"
        assert target_photo.metadata.area == "Area1"
        assert target_photo.metadata.site == "SiteX"
        assert target_photo.metadata.season == "Season2024"
        assert target_photo.metadata.transect == "Transect5"
        assert target_photo.metadata.height == 10
        assert target_photo.metadata.latitude == 45.0
        assert target_photo.metadata.longitude == -120.0
        assert target_photo.metadata.depth == "5m"
        assert target_photo.metadata.camera == "Canon EOS 5D"
        assert target_photo.metadata.photographer == "Alice"
        assert target_photo.metadata.water_quality == "Clear"
        assert target_photo.metadata.strobes == "On"
        assert target_photo.metadata.framing == "Tight"
        assert target_photo.metadata.white_balance_card == "Yes"
        assert target_photo.metadata.comments == "A sample comment"


def test_metadata_dialog_apply_all_checked_to_multiple_photos(qtbot: QtBot) -> None:
    """Apply common metadata to multiple selected photos."""
    with qtbot.capture_exceptions():
        app_model: QApplicationState = QApplicationState()

        # No current photo needed here
        photo1: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2024-06-01T12:00:00"),
                "partner": "PartnerA",
                "area": "Area1",
                "site": "SiteX",
                "season": "Season2024",
                "transect": "Transect5",
                "height": 10,
                "latitude": 45.0,
                "longitude": -120.0,
                "depth": "5m",
                "camera": "Canon EOS 5D",
                "photographer": "Alice",
                "water_quality": "Clear",
                "strobes": "On",
                "framing": "Tight",
                "white_balance_card": "Yes",
                "comments": "A sample comment",
            }
        )
        photo2: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2026-01-02T01:23:45"),
                "partner": "PartnerB",
                "area": "Area2",
                "site": "SiteY",
                "season": "Season2026",
                "transect": "Transect10",
                "height": 20,
                "latitude": 42.0,
                "longitude": -110.0,
                "depth": "10m",
                "camera": "Canon EOS 6D",
                "photographer": "Bob",
                "water_quality": "Murky",
                "strobes": "Off",
                "framing": "Wide",
                "white_balance_card": "No",
                "comments": "Another comment",
            }
        )

        dlg: MetadataDialog = MetadataDialog(app_model, [photo1, photo2])
        qtbot.addWidget(dlg)

        # Manually set values for all fields
        dlg.ui.dteDate.setDateTime(_dt_to_qdatetime(datetime.fromisoformat("2025-12-31T23:59:59")))
        dlg.ui.txtPartner.setText("PartnerX")
        dlg.ui.txtArea.setText("AreaY")
        dlg.ui.txtSite.setText("SiteZ")
        dlg.ui.txtSeason.setText("Season2025")
        dlg.ui.txtTransect.setText("Transect15")
        dlg.ui.numHeight.setValue(15)
        dlg.ui.numLatitude.setValue(40.0)
        dlg.ui.numLongitude.setValue(-100.0)
        dlg.ui.txtDepth.setText("15m")
        dlg.ui.txtCamera.setText("Nikon D850")
        dlg.ui.txtPhotographer.setText("Charlie")
        dlg.ui.txtWaterQuality.setText("Moderate")
        dlg.ui.txtStrobes.setText("Auto")
        dlg.ui.txtFraming.setText("Medium")
        dlg.ui.txtWhiteBalanceCard.setText("Yes")
        dlg.ui.txtComments.setText("Updated comment")

        # Check the boxes to indicate we want to set these fields
        dlg.ui.chkDate.setChecked(True)
        dlg.ui.chkPartner.setChecked(True)
        dlg.ui.chkArea.setChecked(True)
        dlg.ui.chkSite.setChecked(True)
        dlg.ui.chkSeason.setChecked(True)
        dlg.ui.chkTransect.setChecked(True)
        dlg.ui.chkHeight.setChecked(True)
        dlg.ui.chkLatitude.setChecked(True)
        dlg.ui.chkLongitude.setChecked(True)
        dlg.ui.chkDepth.setChecked(True)
        dlg.ui.chkCamera.setChecked(True)
        dlg.ui.chkPhotographer.setChecked(True)
        dlg.ui.chkWaterQuality.setChecked(True)
        dlg.ui.chkStrobes.setChecked(True)
        dlg.ui.chkFraming.setChecked(True)
        dlg.ui.chkWhiteBalanceCard.setChecked(True)
        dlg.ui.chkComments.setChecked(True)

        # Apply changes
        qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

        assert photo1.metadata.date == datetime.fromisoformat("2025-12-31T23:59:59")
        assert photo1.metadata.partner == "PartnerX"
        assert photo1.metadata.area == "AreaY"
        assert photo1.metadata.site == "SiteZ"
        assert photo1.metadata.season == "Season2025"
        assert photo1.metadata.transect == "Transect15"
        assert photo1.metadata.height == 15
        assert photo1.metadata.latitude == 40.0
        assert photo1.metadata.longitude == -100.0
        assert photo1.metadata.depth == "15m"
        assert photo1.metadata.camera == "Nikon D850"
        assert photo1.metadata.photographer == "Charlie"
        assert photo1.metadata.water_quality == "Moderate"
        assert photo1.metadata.strobes == "Auto"
        assert photo1.metadata.framing == "Medium"
        assert photo1.metadata.white_balance_card == "Yes"
        assert photo1.metadata.comments == "Updated comment"

        assert photo2.metadata.date == datetime.fromisoformat("2025-12-31T23:59:59")
        assert photo2.metadata.partner == "PartnerX"
        assert photo2.metadata.area == "AreaY"
        assert photo2.metadata.site == "SiteZ"
        assert photo2.metadata.season == "Season2025"
        assert photo2.metadata.transect == "Transect15"
        assert photo2.metadata.height == 15
        assert photo2.metadata.latitude == 40.0
        assert photo2.metadata.longitude == -100.0
        assert photo2.metadata.depth == "15m"
        assert photo2.metadata.camera == "Nikon D850"
        assert photo2.metadata.photographer == "Charlie"
        assert photo2.metadata.water_quality == "Moderate"
        assert photo2.metadata.strobes == "Auto"
        assert photo2.metadata.framing == "Medium"
        assert photo2.metadata.white_balance_card == "Yes"
        assert photo2.metadata.comments == "Updated comment"


def test_metadata_dialog_apply_checked_to_multiple_photos_1(qtbot: QtBot) -> None:
    """Apply common metadata to multiple selected photos."""
    with qtbot.capture_exceptions():
        app_model: QApplicationState = QApplicationState()

        # No current photo needed here
        photo1: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2024-06-01T12:00:00"),
                "partner": "PartnerA",
                "area": "Area1",
                "site": "SiteX",
                "season": "Season2024",
                "transect": "Transect5",
                "height": 10,
                "latitude": 45.0,
                "longitude": -120.0,
                "depth": "5m",
                "camera": "Canon EOS 5D",
                "photographer": "Alice",
                "water_quality": "Clear",
                "strobes": "On",
                "framing": "Tight",
                "white_balance_card": "Yes",
                "comments": "A sample comment",
            }
        )
        photo2: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2026-01-02T01:23:45"),
                "partner": "PartnerB",
                "area": "Area2",
                "site": "SiteY",
                "season": "Season2026",
                "transect": "Transect10",
                "height": 20,
                "latitude": 42.0,
                "longitude": -110.0,
                "depth": "10m",
                "camera": "Canon EOS 6D",
                "photographer": "Bob",
                "water_quality": "Murky",
                "strobes": "Off",
                "framing": "Wide",
                "white_balance_card": "No",
                "comments": "Another comment",
            }
        )

        dlg: MetadataDialog = MetadataDialog(app_model, [photo1, photo2])
        qtbot.addWidget(dlg)

        # Manually set values for all fields
        dlg.ui.dteDate.setDateTime(_dt_to_qdatetime(datetime.fromisoformat("2025-12-31T23:59:59")))
        dlg.ui.txtPartner.setText("PartnerX")
        dlg.ui.txtArea.setText("AreaY")
        dlg.ui.txtSite.setText("SiteZ")
        dlg.ui.txtSeason.setText("Season2025")
        dlg.ui.txtTransect.setText("Transect15")
        dlg.ui.numHeight.setValue(15)
        dlg.ui.numLatitude.setValue(40.0)
        dlg.ui.numLongitude.setValue(-100.0)
        dlg.ui.txtDepth.setText("15m")
        dlg.ui.txtCamera.setText("Nikon D850")
        dlg.ui.txtPhotographer.setText("Charlie")
        dlg.ui.txtWaterQuality.setText("Moderate")
        dlg.ui.txtStrobes.setText("Auto")
        dlg.ui.txtFraming.setText("Medium")
        dlg.ui.txtWhiteBalanceCard.setText("Yes")
        dlg.ui.txtComments.setText("Updated comment")

        # Check the boxes to indicate we want to set these fields
        dlg.ui.chkDate.setChecked(True)
        dlg.ui.chkPartner.setChecked(False)
        dlg.ui.chkArea.setChecked(True)
        dlg.ui.chkSite.setChecked(False)
        dlg.ui.chkSeason.setChecked(True)
        dlg.ui.chkTransect.setChecked(False)
        dlg.ui.chkHeight.setChecked(True)
        dlg.ui.chkLatitude.setChecked(False)
        dlg.ui.chkLongitude.setChecked(True)
        dlg.ui.chkDepth.setChecked(False)
        dlg.ui.chkCamera.setChecked(True)
        dlg.ui.chkPhotographer.setChecked(False)
        dlg.ui.chkWaterQuality.setChecked(True)
        dlg.ui.chkStrobes.setChecked(False)
        dlg.ui.chkFraming.setChecked(True)
        dlg.ui.chkWhiteBalanceCard.setChecked(False)
        dlg.ui.chkComments.setChecked(True)

        # Apply changes
        qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

        assert photo1.metadata.date == datetime.fromisoformat("2025-12-31T23:59:59")
        assert photo1.metadata.partner == "PartnerA"  # Unchanged
        assert photo1.metadata.area == "AreaY"
        assert photo1.metadata.site == "SiteX"  # Unchanged
        assert photo1.metadata.season == "Season2025"
        assert photo1.metadata.transect == "Transect5"  # Unchanged
        assert photo1.metadata.height == 15
        assert photo1.metadata.latitude == 45.0  # Unchanged
        assert photo1.metadata.longitude == -100.0
        assert photo1.metadata.depth == "5m"  # Unchanged
        assert photo1.metadata.camera == "Nikon D850"
        assert photo1.metadata.photographer == "Alice"  # Unchanged
        assert photo1.metadata.water_quality == "Moderate"
        assert photo1.metadata.strobes == "On"  # Unchanged
        assert photo1.metadata.framing == "Medium"
        assert photo1.metadata.white_balance_card == "Yes"  # Unchanged
        assert photo1.metadata.comments == "Updated comment"

        assert photo2.metadata.date == datetime.fromisoformat("2025-12-31T23:59:59")
        assert photo2.metadata.partner == "PartnerB"  # Unchanged
        assert photo2.metadata.area == "AreaY"
        assert photo2.metadata.site == "SiteY"  # Unchanged
        assert photo2.metadata.season == "Season2025"
        assert photo2.metadata.transect == "Transect10"  # Unchanged
        assert photo2.metadata.height == 15
        assert photo2.metadata.latitude == 42.0  # Unchanged
        assert photo2.metadata.longitude == -100.0
        assert photo2.metadata.depth == "10m"  # Unchanged
        assert photo2.metadata.camera == "Nikon D850"
        assert photo2.metadata.photographer == "Bob"  # Unchanged
        assert photo2.metadata.water_quality == "Moderate"
        assert photo2.metadata.strobes == "Off"  # Unchanged
        assert photo2.metadata.framing == "Medium"
        assert photo2.metadata.white_balance_card == "No"  # Unchanged
        assert photo2.metadata.comments == "Updated comment"


def test_metadata_dialog_apply_checked_to_multiple_photos_2(qtbot: QtBot) -> None:
    """Apply common metadata to multiple selected photos."""
    with qtbot.capture_exceptions():
        app_model: QApplicationState = QApplicationState()

        # No current photo needed here
        photo1: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2024-06-01T12:00:00"),
                "partner": "PartnerA",
                "area": "Area1",
                "site": "SiteX",
                "season": "Season2024",
                "transect": "Transect5",
                "height": 10,
                "latitude": 45.0,
                "longitude": -120.0,
                "depth": "5m",
                "camera": "Canon EOS 5D",
                "photographer": "Alice",
                "water_quality": "Clear",
                "strobes": "On",
                "framing": "Tight",
                "white_balance_card": "Yes",
                "comments": "A sample comment",
            }
        )
        photo2: QPhotoModel = _make_photo(
            metadata={
                "date": datetime.fromisoformat("2026-01-02T01:23:45"),
                "partner": "PartnerB",
                "area": "Area2",
                "site": "SiteY",
                "season": "Season2026",
                "transect": "Transect10",
                "height": 20,
                "latitude": 42.0,
                "longitude": -110.0,
                "depth": "10m",
                "camera": "Canon EOS 6D",
                "photographer": "Bob",
                "water_quality": "Murky",
                "strobes": "Off",
                "framing": "Wide",
                "white_balance_card": "No",
                "comments": "Another comment",
            }
        )

        dlg: MetadataDialog = MetadataDialog(app_model, [photo1, photo2])
        qtbot.addWidget(dlg)

        # Manually set values for all fields
        dlg.ui.dteDate.setDateTime(_dt_to_qdatetime(datetime.fromisoformat("2025-12-31T23:59:59")))
        dlg.ui.txtPartner.setText("PartnerX")
        dlg.ui.txtArea.setText("AreaY")
        dlg.ui.txtSite.setText("SiteZ")
        dlg.ui.txtSeason.setText("Season2025")
        dlg.ui.txtTransect.setText("Transect15")
        dlg.ui.numHeight.setValue(15)
        dlg.ui.numLatitude.setValue(40.0)
        dlg.ui.numLongitude.setValue(-100.0)
        dlg.ui.txtDepth.setText("15m")
        dlg.ui.txtCamera.setText("Nikon D850")
        dlg.ui.txtPhotographer.setText("Charlie")
        dlg.ui.txtWaterQuality.setText("Moderate")
        dlg.ui.txtStrobes.setText("Auto")
        dlg.ui.txtFraming.setText("Medium")
        dlg.ui.txtWhiteBalanceCard.setText("Yes")
        dlg.ui.txtComments.setText("Updated comment")

        # Check the boxes to indicate we want to set these fields
        dlg.ui.chkDate.setChecked(False)
        dlg.ui.chkPartner.setChecked(True)
        dlg.ui.chkArea.setChecked(False)
        dlg.ui.chkSite.setChecked(True)
        dlg.ui.chkSeason.setChecked(False)
        dlg.ui.chkTransect.setChecked(True)
        dlg.ui.chkHeight.setChecked(False)
        dlg.ui.chkLatitude.setChecked(True)
        dlg.ui.chkLongitude.setChecked(False)
        dlg.ui.chkDepth.setChecked(True)
        dlg.ui.chkCamera.setChecked(False)
        dlg.ui.chkPhotographer.setChecked(True)
        dlg.ui.chkWaterQuality.setChecked(False)
        dlg.ui.chkStrobes.setChecked(True)
        dlg.ui.chkFraming.setChecked(False)
        dlg.ui.chkWhiteBalanceCard.setChecked(True)
        dlg.ui.chkComments.setChecked(False)

        # Apply changes
        qtbot.mouseClick(dlg.ui.btnApply, Qt.MouseButton.LeftButton)

        assert photo1.metadata.date == datetime.fromisoformat("2024-06-01T12:00:00")  # Unchanged
        assert photo1.metadata.partner == "PartnerX"
        assert photo1.metadata.area == "Area1"  # Unchanged
        assert photo1.metadata.site == "SiteZ"
        assert photo1.metadata.season == "Season2024"  # Unchanged
        assert photo1.metadata.transect == "Transect15"
        assert photo1.metadata.height == 10  # Unchanged
        assert photo1.metadata.latitude == 40.0
        assert photo1.metadata.longitude == -120.0  # Unchanged
        assert photo1.metadata.depth == "15m"
        assert photo1.metadata.camera == "Canon EOS 5D"  # Unchanged
        assert photo1.metadata.photographer == "Charlie"
        assert photo1.metadata.water_quality == "Clear"  # Unchanged
        assert photo1.metadata.strobes == "Auto"
        assert photo1.metadata.framing == "Tight"  # Unchanged
        assert photo1.metadata.white_balance_card == "Yes"
        assert photo1.metadata.comments == "A sample comment"  # Unchanged

        assert photo2.metadata.date == datetime.fromisoformat("2026-01-02T01:23:45")  # Unchanged
        assert photo2.metadata.partner == "PartnerX"
        assert photo2.metadata.area == "Area2"  # Unchanged
        assert photo2.metadata.site == "SiteZ"
        assert photo2.metadata.season == "Season2026"  # Unchanged
        assert photo2.metadata.transect == "Transect15"
        assert photo2.metadata.height == 20  # Unchanged
        assert photo2.metadata.latitude == 40.0
        assert photo2.metadata.longitude == -110.0  # Unchanged
        assert photo2.metadata.depth == "15m"
        assert photo2.metadata.camera == "Canon EOS 6D"  # Unchanged
        assert photo2.metadata.photographer == "Charlie"
        assert photo2.metadata.water_quality == "Murky"  # Unchanged
        assert photo2.metadata.strobes == "Auto"
        assert photo2.metadata.framing == "Wide"  # Unchanged
        assert photo2.metadata.white_balance_card == "Yes"
        assert photo2.metadata.comments == "Another comment"  # Unchanged
