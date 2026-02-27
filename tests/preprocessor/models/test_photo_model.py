import pytest
from pathlib import Path

from PySide6.QtCore import Slot
from pytestqt.qtbot import QtBot

from preprocessor.model.photo_model import PhotoModel, PhotoData


class TestPhotoModel:
    @staticmethod
    def _assert_property_getter_setter_and_signal(
        qtbot: QtBot,
        model: PhotoModel,
        prop_name: str,
        initial_value: object,
        new_value: object,
        field_signal_name: str,
    ) -> None:
        """Helper to assert getter, setter, and per-field signal emission.

        - Verifies initial getter equals initial_value.
        - Setting the same value does not emit signals.
        - Setting a new value emits the per-field signal and updates the property.
        """
        getter = lambda: getattr(model, prop_name)
        field_signal = getattr(model, field_signal_name)

        # initial
        assert getter() == initial_value

        # setting same value shouldn't emit
        with qtbot.assertNotEmitted(model.on_changed):
            with qtbot.assertNotEmitted(field_signal):
                setattr(model, prop_name, initial_value)

        # setting a different value emits the field signal
        with qtbot.waitSignal(field_signal, timeout=1000):
            setattr(model, prop_name, new_value)

        assert getter() == new_value

    def test_properties_getter_setter_and_signals(self, qtbot: QtBot) -> None:
        # Arrange: base PhotoModel with defaults
        model = PhotoModel(PhotoData(original_filename=Path("base.jpg"), width=100, height=200))

        # original_filename
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "original_filename", Path("base.jpg"), Path("img_001.jpg"), "on_original_filename_changed"
        )

        # width and height
        self._assert_property_getter_setter_and_signal(qtbot, model, "width", 100, 640, "on_width_changed")
        self._assert_property_getter_setter_and_signal(qtbot, model, "height", 200, 480, "on_height_changed")

        # quadrat_corners (None -> list)
        corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "quadrat_corners", None, corners, "on_quadrat_corners_changed"
        )

        # red/blue shifts
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "red_shift", None, (0.3, -0.2), "on_red_shift_changed"
        )
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "blue_shift", None, (0.0, 0.5), "on_blue_shift_changed"
        )

        # camera matrix and distortion coefficients
        cam = ((1000.0, 0.0, 512.0), (0.0, 1000.0, 384.0), (0.0, 0.0, 1.0))
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "camera_matrix", None, cam, "on_camera_matrix_changed"
        )

        distortion = [0.01, -0.02, 0.0, 0.0]
        self._assert_property_getter_setter_and_signal(
            qtbot, model, "distortion_coefficients", None, distortion, "on_distortion_coefficients_changed"
        )

    def test_quadrat_corners(self) -> None:
        # Arrange
        photo = PhotoModel(
            PhotoData(
                original_filename=Path("img_001.jpg"),
                width=1024,
                height=768,
            )
        )

        raised_quadrat_corners_changed = False
        raised_changed = False

        @Slot()
        def handle_quadrat() -> None:
            nonlocal raised_quadrat_corners_changed
            raised_quadrat_corners_changed = True

        @Slot()
        def handle_changed() -> None:
            nonlocal raised_changed
            raised_changed = True

        photo.on_quadrat_corners_changed.connect(handle_quadrat)
        photo.on_changed.connect(handle_changed)

        # Assert initial state (quadrat_corners normalizes empty lists to None in the data model)
        assert photo.quadrat_corners is None
        assert not raised_quadrat_corners_changed
        assert not raised_changed

        # Act: set quadrat corners
        corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        photo.quadrat_corners = corners  # type: ignore[assignment]

        # Assert: property set and both signals fired
        assert photo.quadrat_corners == corners
        assert raised_quadrat_corners_changed
        assert raised_changed

        # Act: set same value again -> no signals
        raised_quadrat_corners_changed = False
        raised_changed = False
        photo.quadrat_corners = corners

        # Assert: no signals fired when value unchanged
        assert not raised_quadrat_corners_changed
        assert not raised_changed

        # Act: clear the value
        photo.quadrat_corners = []

        # Assert: property cleared and signals fired
        # Setting an empty list via the setter leaves an empty list on the runtime model
        assert photo.quadrat_corners == []
        assert raised_quadrat_corners_changed
        assert raised_changed

    def test_serialize_deserialize(self) -> None:
        # Arrange
        photo0 = PhotoModel(
            PhotoData(
                original_filename=Path("img_001.jpg"),
                width=1024,
                height=768,
            )
        )

        # Assert: defaults set (quadrat_corners defaults to None)
        assert photo0.original_filename == Path("img_001.jpg")
        assert photo0.quadrat_corners is None
        assert photo0.red_shift is None
        assert photo0.blue_shift is None

        # Act: Serialize and deserialize
        json_str0: str = photo0._data.model_dump_json()
        photo1: PhotoModel = PhotoModel(PhotoData.model_validate_json(json_str0))

        # Assert: values read
        assert photo1.original_filename == photo0.original_filename
        assert photo1.quadrat_corners == photo0.quadrat_corners
        assert photo1.red_shift == photo0.red_shift
        assert photo1.blue_shift == photo0.blue_shift
        assert photo1.camera_matrix == photo0.camera_matrix
        assert photo1.distortion_coefficients == photo0.distortion_coefficients

        # Act: Set some values
        corners = [(0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)]
        camera = (
            (1000.0, 0.0, 512.0),
            (0.0, 1000.0, 384.0),
            (0.0, 0.0, 1.0),
        )
        distortion = [0.01, -0.02, 0.0, 0.0]
        photo1.original_filename = Path("img_001.jpg")
        photo1.quadrat_corners = corners
        photo1.red_shift = (0.3, -0.2)
        photo1.blue_shift = (0.0, 0.5)
        photo1.camera_matrix = camera
        photo1.distortion_coefficients = distortion

        # Assert: verify values set
        assert photo1.original_filename == Path("img_001.jpg")
        assert photo1.quadrat_corners == corners
        assert photo1.red_shift == (0.3, -0.2)
        assert photo1.blue_shift == (0.0, 0.5)
        assert photo1.camera_matrix == camera
        assert photo1.distortion_coefficients == distortion

        # Act: Serialize and deserialize
        json_str1: str = photo1._data.model_dump_json()
        photo2: PhotoModel = PhotoModel(PhotoData.model_validate_json(json_str1))

        # Assert: verify values read
        assert photo2.original_filename == Path("img_001.jpg")
        assert photo2.quadrat_corners == corners
        assert photo2.red_shift == (0.3, -0.2)
        assert photo2.blue_shift == (0.0, 0.5)
        assert photo2.camera_matrix == camera
        assert photo2.distortion_coefficients == distortion

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_signals(self, qtbot: QtBot) -> None:
        # Arrange: Create a fresh model and verify signals and value
        photo1 = PhotoModel(
            PhotoData(
                original_filename=Path("tmp"),
                width=1024,
                height=768,
            )
        )

        with qtbot.waitSignal(photo1.on_original_filename_changed, raising=True):
            photo1.original_filename = Path("img_001.jpg")

        with qtbot.waitSignal(photo1.on_quadrat_corners_changed, raising=True):
            photo1.quadrat_corners = [(0.1, 0.2), (1.1, 0.2), (1.1, 1.2), (0.1, 1.2)]

        with qtbot.waitSignal(photo1.on_red_shift_changed, raising=True):
            photo1.red_shift = (0.3, -0.2)

        with qtbot.waitSignal(photo1.on_blue_shift_changed, raising=True):
            photo1.blue_shift = (0.0, 0.5)

        with qtbot.waitSignal(photo1.on_camera_matrix_changed, raising=True):
            photo1.camera_matrix = (
                (1000.0, 0.0, 512.0),
                (0.0, 1000.0, 384.0),
                (0.0, 0.0, 1.0),
            )

        with qtbot.waitSignal(photo1.on_distortion_coefficients_changed, raising=True):
            photo1.distortion_coefficients = [0.01, -0.02, 0.0, 0.0]

        with qtbot.waitSignal(photo1.on_changed, raising=True):
            # Any change
            photo1.original_filename = Path("img_002.jpg")
