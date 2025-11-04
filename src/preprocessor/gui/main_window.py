import sys
from typing import cast, Callable

import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSettings, QByteArray, QTimer, Signal
from PySide6.QtGui import QAction, QIcon, QCloseEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QDockWidget, QWidget, QFileDialog, QLabel, \
    QGridLayout
from cv2.typing import MatLike

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.ui_loader import UILoader
from preprocessor._version import __version__
from preprocessor.gui.worker import Worker, WorkerManager


class MainWindow(QMainWindow):
    """Main application window."""

    properties_dock: QDockWidget
    """The dock widget showing properties."""
    central_widget: QLabel
    """The central widget showing the image."""
    _debounce_timer: QTimer
    """Timer for debouncing image processing parameter changes."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("CAMBioMed Preprocessor")
        self.resize(400, 200)
        self.settings = QSettings("CAMBioMed", "Preprocessor")

        self.create_debounce_timer()

        self.create_menu()
        self.create_toolbar()
        self.create_central_widget()
        self.create_properties_dock()
        self.create_statusbar()

        self.read_settings()

    def create_debounce_timer(self) -> None:
        debounce_interval_ms = 150  # milliseconds
        self._debounce_timer = QtCore.QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(debounce_interval_ms)
        self._debounce_timer.timeout.connect(lambda: self._schedule_processing(self._current_image_path))

    def create_menu(self) -> None:
        """Create the main window menu."""
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")

        open_action = QAction("&Open", self)
        open_action.setStatusTip("Open an image")
        open_action.triggered.connect(self.on_open_file)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)

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
        self.central_widget = QLabel()
        self.central_widget.setScaledContents(True)
        self.central_widget.setStyleSheet("background-color: purple;")
        # central_widget_grid = QGridLayout()
        # central_widget_grid.addWidget(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def create_properties_dock(self) -> None:
        """Create a dock widget."""
        self.properties_dock = cast(QDockWidget, UILoader.load("properties_dock"))
        self.properties_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties_dock)

        # Update the image and numeric label whenever a slider value changes
        def _on_slider1_change(v: int) -> None:
            self.properties_dock.label.setText(str(v))
            # Start the timer to debounce rapid slider changes
            # If the timer is already running, it will be restarted
            self._debounce_timer.start()

        def _on_slider2_change(v: int) -> None:
            self.properties_dock.label_2.setText(str(v))
            # Start the timer to debounce rapid slider changes
            # If the timer is already running, it will be restarted
            self._debounce_timer.start()

        self.properties_dock.horizontalSlider.valueChanged.connect(_on_slider1_change)
        self.properties_dock.horizontalSlider_2.valueChanged.connect(_on_slider2_change)

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


    def on_open_file(self) -> None:
        path = QFileDialog.getOpenFileName(self, "Open")[0]
        if path: self._display_image(str(path))

    _current_image_path: str | None = None
    """Path to the currently displayed image, or None."""
    _latest_token: int = 0
    """Token to identify the latest processing request."""
    _worker_manager: WorkerManager = WorkerManager()

    def _display_image(self, image_path: str) -> None:
        """Schedule background processing of the image and show the result when ready."""
        self._current_image_path = str(image_path)
        # schedule background processing
        self._schedule_processing(self._current_image_path)

    def _schedule_processing(self, image_path: str) -> None:
        """Schedule a worker to process the image."""
        # Increment token to mark a new request
        self._latest_token += 1
        token = self._latest_token

        # Obtain current threshold values from sliders
        th1 = int(self.properties_dock.horizontalSlider.value())
        th2 = int(self.properties_dock.horizontalSlider_2.value())

        # Downscale the image for faster preview processing
        preview_max_side = 800

        worker = Worker(lambda progress_callback: self._process_image(image_path, th1, th2, preview_max_side, progress_callback))
        worker.signals.result.connect(lambda result: self._on_process_image_finished(result, token))
        worker.signals.progress.connect(lambda p: self.central_widget.setText(f"Processing... {int(p * 100)}% ({self._worker_manager.threadpool.maxThreadCount()})"))
        try:
            # Clear pixmap and show small text so users know processing is happening
            self.central_widget.setPixmap(QtGui.QPixmap())
            self.central_widget.setText("Processing...")
        except Exception:
            pass
        self._worker_manager.start(worker)

    def _process_image(self, image_path: str, threshold1: int, threshold2: int, preview_max_side: int, progress_callback: Signal) -> MatLike | None:
        """Process the image and return it."""
        import faulthandler

        faulthandler.enable()

        progress_callback.emit(0.1)
        if not image_path: return None
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None: return None

        h, w = img.shape[:2]

        # Downscale image for preview processing to speed up worker
        try:
            if preview_max_side and (h > preview_max_side or w > preview_max_side):
                scale = float(preview_max_side) / float(max(h, w))
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        except Exception:
            # if resizing fails for any reason, continue with original image
            pass
        progress_callback.emit(0.4)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        progress_callback.emit(0.6)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        progress_callback.emit(0.8)
        # WARNING: This seems to work better on the scaled down preview
        # than on the full image. Thus, generating the final image
        # full-scale will produce different results!
        edges = cv2.Canny(blurred, threshold1, threshold2)
        progress_callback.emit(1.0)
        return edges

    def _on_process_image_finished(self, result: MatLike | None, token: int) -> None:
        """Handle worker finished processing the image."""
        # Only update the display if this is the latest request
        if token != self._latest_token: return
        # Only update the display if there is a result
        if result is None: return

        def apply() -> None:
            try:
                h, w = result.shape[:2]
                bytes_per_line = result.strides[0]
                self._image_ref = result
                qformat = QtGui.QImage.Format.Format_Grayscale8
                qimg = QtGui.QImage(self._image_ref.data, w, h, bytes_per_line, qformat)
                qpixmap = QtGui.QPixmap.fromImage(qimg)
                self.central_widget.setPixmap(qpixmap)
                self.central_widget.setText("")
            except Exception as e:
                self.central_widget.setText(f"Error: {e}")

        # Schedule the UI update on the main thread using a single-shot timer
        QtCore.QTimer.singleShot(0, apply)

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

