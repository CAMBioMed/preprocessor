import logging
import signal
import sys
from dataclasses import dataclass
from typing import cast, Callable

import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSettings, QByteArray, QTimer, Signal, Slot
from PySide6.QtGui import QAction, QIcon, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QDockWidget,
    QWidget,
    QFileDialog,
    QLabel,
    QGridLayout,
)
from cv2.typing import MatLike

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.quadrat_detection import QuadratDetectionParams
from preprocessor.gui.ui_loader import UILoader
from preprocessor._version import __version__
from preprocessor.gui.worker import Worker, WorkerManager

from qimage2ndarray import array2qimage

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    properties_dock: QDockWidget
    """The dock widget showing properties."""
    central_widget: QImageEditor
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
        open_action.triggered.connect(self.on_file_open)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)

        exit_action = QAction("&Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.setStatusTip("Show the About dialog")
        about_action.triggered.connect(self.on_help_about)
        help_menu.addAction(about_action)

    def create_toolbar(self) -> None:
        """Create the main window toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        # toolbar.setMovable(False)

        def toolbar_button_clicked(s: str) -> None:
            print("click", s)

        button_action = QAction(QIcon("src/preprocessor/icons/fugue16/folder-open-image.png"), "&Open", self)
        button_action.setStatusTip("Open an image")
        button_action.triggered.connect(self.on_file_open)
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
        self.central_widget = QImageEditor()
        # self.central_widget.setScaledContents(True)
        self.central_widget.setStyleSheet("background-color: purple;")
        self.setCentralWidget(self.central_widget)

    def create_properties_dock(self) -> None:
        """Create a dock widget."""
        self.properties_dock = cast(QDockWidget, UILoader.load("properties_dock"))
        self.properties_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties_dock)

        # Update the image and numeric label whenever a slider value changes
        def _on_sliderCannyThreshold1_change(v: int) -> None:
            self.properties_dock.spinboxCannyThreshold1.setValue(v)
            # Start the timer to debounce rapid slider changes
            # If the timer is already running, it will be restarted
            self._debounce_timer.start()

        def _on_sliderCannyThreshold2_change(v: int) -> None:
            self.properties_dock.spinboxCannyThreshold2.setValue(v)
            # Start the timer to debounce rapid slider changes
            # If the timer is already running, it will be restarted
            self._debounce_timer.start()

        def _on_parameter_change() -> None:
            # Start the timer to debounce rapid parameter changes
            # If the timer is already running, it will be restarted
            self._debounce_timer.start()

        self.properties_dock.checkboxDownscaleEnabled.stateChanged.connect(_on_parameter_change)
        self.properties_dock.spinboxDownscaleMaxSize.valueChanged.connect(_on_parameter_change)
        self.properties_dock.checkboxBlurEnabled.stateChanged.connect(_on_parameter_change)
        self.properties_dock.spinboxBlurKernelSize.valueChanged.connect(_on_parameter_change)
        # TODO: Add new thresholding handlers
        # TODO: Change value in spinbox when slider changes and vice versa
        self.properties_dock.checkboxCannyEnabled.stateChanged.connect(_on_parameter_change)
        self.properties_dock.sliderCannyThreshold1.valueChanged.connect(_on_sliderCannyThreshold1_change)
        self.properties_dock.sliderCannyThreshold2.valueChanged.connect(_on_sliderCannyThreshold2_change)
        self.properties_dock.spinboxCannyApertureSize.valueChanged.connect(_on_parameter_change)

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

    def on_file_open(self) -> None:
        path = QFileDialog.getOpenFileName(self, "Open")[0]
        if path:
            self._display_image(str(path))

    def on_help_about(self) -> None:
        show_about_dialog(self)

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

        # Obtain current parameters
        params = QuadratDetectionParams(
            downscale_enabled = bool(self.properties_dock.checkboxDownscaleEnabled.isChecked()),
            downscale_max_size = int(self.properties_dock.spinboxDownscaleMaxSize.value()),
            blur_enabled = bool(self.properties_dock.checkboxBlurEnabled.isChecked()),
            blur_kernel_size = int(self.properties_dock.spinboxBlurKernelSize.value()),
            # TODO: Add new thresholding parameters
            canny_enabled = bool(self.properties_dock.checkboxCannyEnabled.isChecked()),
            canny_threshold1 = int(self.properties_dock.sliderCannyThreshold1.value()),
            canny_threshold2 = int(self.properties_dock.sliderCannyThreshold2.value()),
            canny_aperture_size = int(self.properties_dock.spinboxCannyApertureSize.value()),
        )

        @Slot(object)
        def on_result(result: MatLike) -> None:
            self._on_process_image_finished(result, token)

        @Slot(float)
        def on_progress(p: float) -> None:
            self.central_widget.message = f"Processing... {int(p * 100)}% ({self._worker_manager.threadpool.maxThreadCount()})"

        @Slot()
        def act(progress_callback: Signal) -> MatLike | None:
            return self._process_image(image_path, params, progress_callback)

        logger.debug(f"Refcount on_result pre: {sys.getrefcount(on_result)}")
        logger.debug(f"Refcount on_progress pre: {sys.getrefcount(on_progress)}")
        logger.debug(f"Refcount act pre: {sys.getrefcount(act)}")

        worker = Worker(act)
        worker.signals.result.connect(on_result)
        worker.signals.progress.connect(on_progress)

        logger.debug(f"Refcount on_result post: {sys.getrefcount(on_result)}")
        logger.debug(f"Refcount on_progress post: {sys.getrefcount(on_progress)}")
        logger.debug(f"Refcount act post: {sys.getrefcount(act)}")

        try:
            # Clear pixmap and show small text so users know processing is happening
            self.central_widget.pixmap = None
            self.central_widget.message = "Processing..."
        except Exception:
            pass
        logger.debug(f"Refcount worker pre: {sys.getrefcount(worker)}")
        self._worker_manager.start(worker)
        logger.debug(f"Refcount worker post: {sys.getrefcount(worker)}")

    def _process_image(
        self, image_path: str, params: QuadratDetectionParams, progress_callback: Signal
    ) -> MatLike | None:
        """Process the image and return it."""
        import faulthandler

        faulthandler.enable(all_threads=True)

        if not image_path:
            return None

        logger.debug(f"Reading image {image_path}...")
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        progress_callback.emit(0.1)
        logger.debug(f"Read image {image_path}")
        if img is None:
            return None

        h, w = img.shape[:2]

        # Downscale image for preview processing to speed up worker
        try:
            if params.downscale_enabled and params.downscale_max_size and (h > params.downscale_max_size or w > params.downscale_max_size):
                scale = float(params.downscale_max_size) / float(max(h, w))
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                logger.debug(f"Downscaling image to {new_w}x{new_h} pixels...")
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                progress_callback.emit(0.4)
                logger.debug(f"Downscaled image to {new_w}x{new_h} pixels")
        except Exception:
            # if resizing fails for any reason, continue with original image
            pass

        logger.debug("Graying image...")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        progress_callback.emit(0.6)
        logger.debug("Grayed image.")

        if (params.blur_enabled):
            logger.debug("Blurring image...")
            img = cv2.GaussianBlur(img, (params.blur_kernel_size, params.blur_kernel_size), 0)
            progress_callback.emit(0.8)
            logger.debug("Blurred image")

        if (params.canny_enabled):
            threshold1 = params.canny_threshold1
            threshold2 = params.canny_threshold2

            # WARNING: This seems to work better on the scaled down preview
            # than on the full image. Thus, generating the final image
            # full-scale will produce different results!
            logger.debug(f"Cannying image to {threshold1}, {threshold2}...")
            img = cv2.Canny(img, threshold1, threshold2, apertureSize=params.canny_aperture_size)
            progress_callback.emit(1.0)
            logger.debug("Cannied image.")

        return img

    def _on_process_image_finished(self, result: MatLike | None, token: int) -> None:
        """Handle worker finished processing the image."""
        logger.debug("Finishing processing...")
        # Only update the display if this is the latest request
        if token != self._latest_token:
            logger.debug("Skipped: not latest")
            return
        # Only update the display if there is a result
        if result is None:
            logger.debug("Skipped: no result")
            return

        def apply() -> None:
            try:
                logger.debug("Converting image...")
                qimg = array2qimage(result)
                # h, w = result.shape[:2]
                # bytes_per_line = result.strides[0]
                # self._image_ref = result
                # qformat = QtGui.QImage.Format.Format_Grayscale8
                # qimg = QtGui.QImage(self._image_ref.data, w, h, bytes_per_line, qformat)
                logger.debug("Converted image")

                logger.debug("Displaying image...")
                qpixmap = QtGui.QPixmap.fromImage(qimg)
                self.central_widget.pixmap = qpixmap
                self.central_widget.message = ""
                logger.debug("Displayed image.")
            except Exception as e:
                self.central_widget.message = f"Error: {e}"

        # Schedule the UI update on the main thread using a single-shot timer
        logger.debug("Scheduling display on UI...")
        QtCore.QTimer.singleShot(0, apply)
        logger.debug("Scheduled display on UI")

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()

signal_timer: QTimer

def setup_sigint_handler(interval: int = 200) -> None:
    """Process any pending SIGINT signals."""

    # Based on: https://stackoverflow.com/a/4939113/146622
    # The Qt application main event loop doesn't run on the Python interpreter, so it doesn't process signals.
    # Setup timer to periodically run the Python interpreter to check for (SIGINT) signals from outside.

    global signal_timer  # Prevent garbage collection

    signal.signal(signal.SIGINT, sigint_handler)
    signal_timer = QTimer()
    signal_timer.start(interval)
    signal_timer.timeout.connect(lambda: None)  # Let the interpreter run each time.

def show_application() -> None:
    """Show the main application window."""
    # Disable allocation limit
    QtGui.QImageReader.setAllocationLimit(0)

    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    window = MainWindow()
    window.show()
    setup_sigint_handler()
    exit_code = app.exec_()
    sys.exit(exit_code)
