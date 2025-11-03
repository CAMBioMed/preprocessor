import sys
import traceback
from pathlib import Path

import cv2
from cv2.typing import MatLike
from PySide6 import QtGui
from PySide6.QtCore import QSize, QUrl
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider


def show_ui():
    # Disable allocation limit
    QtGui.QImageReader.setAllocationLimit(0)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # Ensure the QML import path includes the module directory
    engine.addImportPath(str(Path(__file__).resolve().parent))

    # Register an image provider named 'cvimg' so QML can request images via image://cvimg/<id>
    image_file = Path(__file__).resolve().parent / "images" / "Kea5_3a.JPG"
    engine.addImageProvider("cvimg", CVImageProvider(image_file))

    qml_file = Path(__file__).resolve().parent / "hello_world.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


# Load an image and convert it to grayscale using OpenCV
def show_image(image_path: str) -> MatLike:
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


# Based on: https://stackoverflow.com/a/35857856/146622
def as_bgr888_qimage(img: MatLike) -> QImage:
    height, width, _channels = img.shape
    bytes_per_line = 3 * width
    qimage = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
    return qimage


# Based on: https://stackoverflow.com/a/35857856/146622
def as_8_qimage(img: MatLike) -> QImage:
    height, width = img.shape
    bytes_per_line = 1 * width
    qimage = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
    return qimage


class CVImageProvider(QQuickImageProvider):
    """Provides images to QML by loading them with OpenCV and converting to QImage."""

    def __init__(self, image_path: Path):
        # Use getattr to read the Image enum if present; otherwise fall back to the integer value (1).
        image_type = getattr(QQuickImageProvider, "Image", 1)
        super().__init__(image_type)
        self._image_path = str(image_path)

    def requestImage(self, _id: str, _size: QSize, _requestedSize: QSize) -> QImage:
        # Qt's signature provides a 'size' output parameter (here provided as an instance we can ignore),
        # and a requestedSize indicating the size requested by QML. We ignore both for now and return
        # the full image. The 'id' parameter can be used to select different images.
        try:
            img = show_image(self._image_path)
            qimg = as_8_qimage(img)
            return qimg
        except Exception as exc:
            print(traceback.format_exc())
            print(f"CVImageProvider: failed to provide image: {exc}", file=sys.stderr)
            return QImage()
