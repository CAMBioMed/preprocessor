from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import QMainWindow, QWidget

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.gui.thumbnail_list_widget import ThumbnailListWidget
from preprocessor.gui.ui_main import Ui_Main
from preprocessor.model.application_model import ApplicationModel


class MainWindow2(QMainWindow):
    ui: Ui_Main
    model: ApplicationModel

    properties_dock: PropertiesDockWidget
    """The dock widget showing properties."""
    thumbnail_dock: ThumbnailListWidget
    """The dock widget showing image thumbnails."""
    central_widget: QImageEditor
    """The central widget showing the image."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.model = ApplicationModel()
        self._connect_signals()

        self.read_settings()

    def _connect_signals(self) -> None:
        self.ui.menuHelp_About.triggered.connect(self.on_help_about)
        self.ui.menuFile_Exit.triggered.connect(self.close)

    def on_help_about(self) -> None:
        show_about_dialog(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.write_settings()
        super().closeEvent(event)
        event.accept()

    def write_settings(self) -> None:
        """Write window settings to persistent storage."""
        self.model.main_window_geometry = self.saveGeometry()
        self.model.main_window_state = self.saveState()
        self.model.write_settings()

    def read_settings(self) -> None:
        """Read window settings from persistent storage."""
        self.model.read_settings()
        self.restoreGeometry(self.model.main_window_geometry)
        self.restoreState(self.model.main_window_state)
