import sys
from typing import cast

from PySide6 import QtGui
from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtGui import QAction, QIcon, QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QDockWidget, QWidget
from PySide6.QtUiTools import QUiLoader

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.ui_loader import UILoader
from preprocessor._version import __version__

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
# from ui_form import Ui_MyWindow
# from ui_form import Ui_MyDockWidget

loader = QUiLoader()


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("CAMBioMed Preprocessor")
        self.resize(400, 200)
        self.settings = QSettings("CAMBioMed", "Preprocessor")

        self.create_menu()
        self.create_toolbar()
        self.create_central_widget()
        self.create_properties_dock()
        self.create_statusbar()

        self.read_settings()

    def create_menu(self) -> None:
        """Create the main window menu."""
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.setStatusTip("Show the About dialog")
        about_action.triggered.connect(lambda: show_about_dialog(self))
        help_menu.addAction(about_action)

    def create_toolbar(self) -> None:
        """Create the main window toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        # toolbar.setMovable(False)

        def toolbar_button_clicked(s: str) -> None:
            print("click", s)

        button_action = QAction(QIcon("src/preprocessor/icons/fugue16/bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(toolbar_button_clicked)
        button_action.setCheckable(False)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("src/preprocessor/icons/fugue32/bookmark.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(toolbar_button_clicked)
        button_action2.setCheckable(False)
        toolbar.addAction(button_action2)

    def create_statusbar(self) -> None:
        """Create the main window status bar."""
        self.statusBar().showMessage(f"Preprocessor {QtGui.QGuiApplication.applicationVersion()} ready")

    def create_central_widget(self) -> None:
        """Create the central widget."""
        central_widget = QWidget() # placeholder
        central_widget.setStyleSheet("background-color: purple;")
        self.setCentralWidget(central_widget)

    def create_properties_dock(self) -> None:
        """Create a dock widget."""
        dock = cast(QDockWidget, UILoader.load("properties_dock"))
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.write_settings()
        super().closeEvent(event)
        event.accept()

    def write_settings(self) -> None:
        """Write window settings to persistent storage."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def read_settings(self) -> None:
        """Read window settings from persistent storage."""
        self.restoreGeometry(cast(QByteArray, self.settings.value("geometry", QByteArray())))
        self.restoreState(cast(QByteArray, self.settings.value("windowState", QByteArray())))


def show_application() -> None:
    """Show the main application window."""
    # Disable allocation limit
    QtGui.QImageReader.setAllocationLimit(0)

    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
