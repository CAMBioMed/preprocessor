from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QWidget

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.icons import GuiIcons
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.gui.thumbnail_dock_widget import ThumbnailDockWidget
from preprocessor.gui.thumbnail_list_widget import ThumbnailListWidget
from preprocessor.gui.ui_main import Ui_Main
from preprocessor.model.application_model import ApplicationModel


class MainWindow2(QMainWindow):
    ui: Ui_Main
    model: ApplicationModel

    properties_dock: PropertiesDockWidget
    """The dock widget showing properties."""
    thumbnail_dock: ThumbnailDockWidget
    """The dock widget showing image thumbnails."""
    central_widget: QImageEditor
    """The central widget showing the image."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self._setup_icons()
        self._setup_keyboard_shortcuts()
        self._create_thumbnail_dock()

        self.model = ApplicationModel()
        self._connect_signals()

        self.read_settings()

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # File menu
        self.ui.menuFile_NewProject.setIcon(GuiIcons.ProjectNew)
        self.ui.menuFile_OpenProject.setIcon(GuiIcons.ProjectOpen)
        self.ui.menuFile_SaveProject.setIcon(GuiIcons.ProjectSave)
        self.ui.menuFile_SaveProjectAs.setIcon(GuiIcons.ProjectSaveAs)
        self.ui.menuFile_Exit.setIcon(GuiIcons.ApplicationExit)

        # Help menu
        self.ui.menuHelp_About.setIcon(GuiIcons.HelpAbout)

    def _setup_keyboard_shortcuts(self) -> None:
        """
        Set up keyboard shortcuts for actions.

        As Qt Creator/Designer does not support setting StandardKey shortcuts,
        we do it manually here. See:
        https://forum.qt.io/topic/6259/qt-designer-does-not-support-qkeysequence-standardkey
        """
        # File menu
        self.ui.menuFile_NewProject.setShortcut(QKeySequence.StandardKey.New)
        self.ui.menuFile_OpenProject.setShortcut(QKeySequence.StandardKey.Open)
        self.ui.menuFile_SaveProject.setShortcut(QKeySequence.StandardKey.Save)
        self.ui.menuFile_SaveProjectAs.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.ui.menuFile_Exit.setShortcut(QKeySequence.StandardKey.Quit)

        # Help menu
        self.ui.menuHelp_About.setShortcut(QKeySequence.StandardKey.HelpContents)

    def _create_thumbnail_dock(self) -> None:
        """Create the thumbnail list dock widget."""
        self.thumbnail_dock = ThumbnailDockWidget(self)
        self.thumbnail_dock.setAllowedAreas(
            Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.thumbnail_dock)

    def _connect_signals(self) -> None:
        """Connect signals to slots."""
        # File menu
        self.ui.menuFile_Exit.triggered.connect(self.close)

        # Help menu
        self.ui.menuHelp_About.triggered.connect(self.on_help_about)

        # When a thumbnail is selected, either show stored result or schedule processing
        # self.thumbnail_dock.on_thumbnail_selected.connect(self._display_image)

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
