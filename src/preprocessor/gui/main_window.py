import logging
import signal
import sys
from typing import cast, Any

import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSettings, QByteArray, QTimer, Slot, Signal
from PySide6.QtGui import QAction, QIcon, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QWidget,
    QFileDialog,
)
from cv2.typing import MatLike

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.main_window_model import MainWindowModel
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.processing.detect_quadrat import detect_quadrat, QuadratDetectionResult
from preprocessor.processing.fix_perspective import fix_perspective
from preprocessor.processing.load_image import load_image
from preprocessor.processing.params import QuadratDetectionParams
from preprocessor._version import __version__
from preprocessor.gui.worker import Worker, WorkerManager

from qimage2ndarray import array2qimage

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    model: MainWindowModel

    properties_dock: PropertiesDockWidget
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

        self.model = MainWindowModel()
        # FIXME: How to get the PropertiesDockModel into the widget?
        self._connect_signals()

        self.read_settings()

    def _connect_signals(self) -> None:
        # TODO
        pass

    def create_debounce_timer(self) -> None:
        debounce_interval_ms = 150  # milliseconds
        self._debounce_timer = QtCore.QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(debounce_interval_ms)
        self._debounce_timer.timeout.connect(lambda: self._schedule_processing(self._current_image_path))

    def _on_parameter_change(self) -> None:
        # Start the timer to debounce rapid parameter changes
        # If the timer is already running, it will be restarted
        self._debounce_timer.start()

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

    view_original_button: QAction
    view_processed_button: QAction
    view_final_button: QAction
    view_debug_button: QAction

    def create_toolbar(self) -> None:
        """Create the main window toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(toolbar)
        # toolbar.setMovable(False)

        def toolbar_button_clicked(s: str) -> None:
            print("click", s)

        # open_button_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        open_button_icon = QIcon("src/preprocessor/icons/fugue16/folder-open-image.png")
        open_button = QAction(open_button_icon, "&Open", self)
        open_button.setStatusTip("Open an image")
        open_button.triggered.connect(self.on_file_open)
        open_button.setCheckable(False)
        toolbar.addAction(open_button)

        toolbar.addSeparator()

        view_group = QtGui.QActionGroup(self)

        view_original_button_icon = QIcon("src/preprocessor/icons/fugue16/image-medium.png")
        self.view_original_button = QAction(view_original_button_icon, "&View Original", view_group)
        self.view_original_button.setStatusTip("View the original image")
        self.view_original_button.triggered.connect(self._on_parameter_change)
        self.view_original_button.setCheckable(True)
        toolbar.addAction(self.view_original_button)

        view_processed_button_icon = QIcon("src/preprocessor/icons/fugue16/image-saturation.png")
        self.view_processed_button = QAction(view_processed_button_icon, "&View Processed", view_group)
        self.view_processed_button.setStatusTip("View the processed image")
        self.view_processed_button.triggered.connect(self._on_parameter_change)
        self.view_processed_button.setCheckable(True)
        # self.view_processed_button.setChecked(True)
        toolbar.addAction(self.view_processed_button)

        view_debug_button_icon = QIcon("src/preprocessor/icons/fugue16/images-flickr.png")
        self.view_debug_button = QAction(view_debug_button_icon, "&View Debug", view_group)
        self.view_debug_button.setStatusTip("View the debug image")
        self.view_debug_button.triggered.connect(self._on_parameter_change)
        self.view_debug_button.setCheckable(True)
        self.view_debug_button.setChecked(True)
        toolbar.addAction(self.view_debug_button)

        view_final_button_icon = QIcon("src/preprocessor/icons/fugue16/image-saturation.png")
        self.view_final_button = QAction(view_final_button_icon, "&View final", view_group)
        self.view_final_button.setStatusTip("View the final image")
        self.view_final_button.triggered.connect(self._on_parameter_change)
        self.view_final_button.setCheckable(True)
        toolbar.addAction(self.view_final_button)

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
        # self.properties_dock = cast(QDockWidget, UILoader.load("properties_dock"))
        self.properties_dock = PropertiesDockWidget()
        self.properties_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties_dock)

        self.properties_dock.model.on_changed.connect(self._on_parameter_change)

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

    def _schedule_processing(self, image_path: str | None) -> None:
        """Schedule a worker to process the image."""
        # Increment token to mark a new request
        self._latest_token += 1
        token = self._latest_token

        # Obtain current parameters
        params = self.properties_dock.model.params

        @Slot(object)
        def on_result(result: QuadratDetectionResult) -> None:
            self._on_process_image_finished(result, token)

        @Slot(float)
        def on_progress(p: float) -> None:
            self.central_widget.message = f"Processing... {int(p * 100)}%"

        @Slot()
        def act(progress_callback: Signal) -> QuadratDetectionResult:
            return self._process_image(image_path, params, progress_callback)

        # logger.debug(f"Refcount on_result pre: {sys.getrefcount(on_result)}")
        # logger.debug(f"Refcount on_progress pre: {sys.getrefcount(on_progress)}")
        # logger.debug(f"Refcount act pre: {sys.getrefcount(act)}")

        worker = Worker(act)
        worker.signals.result.connect(on_result)
        worker.signals.progress.connect(on_progress)

        # logger.debug(f"Refcount on_result post: {sys.getrefcount(on_result)}")
        # logger.debug(f"Refcount on_progress post: {sys.getrefcount(on_progress)}")
        # logger.debug(f"Refcount act post: {sys.getrefcount(act)}")

        try:
            # Clear pixmap and show small text so users know processing is happening
            self.central_widget.pixmap = None
            self.central_widget.message = "Processing..."
        except Exception:
            pass
        # logger.debug(f"Refcount worker pre: {sys.getrefcount(worker)}")
        self._worker_manager.start(worker)
        # logger.debug(f"Refcount worker post: {sys.getrefcount(worker)}")

    def _process_image(
        self, image_path: str | None, params: QuadratDetectionParams, _progress_callback: Signal
    ) -> QuadratDetectionResult:
        """Process the image and return it."""
        if not image_path:
            return QuadratDetectionResult(None, None, None, None)

        img = load_image(image_path)
        if img is None:
            return QuadratDetectionResult(None, None, None, None)

        result = detect_quadrat(img, params)
        if params.fix_perspective.enabled and result.corners is not None and len(result.corners) == 4:
            final_img = fix_perspective(
                img,
                result.corners,
                params.fix_perspective.target_width,
                params.fix_perspective.target_height,
            )
            return QuadratDetectionResult(
                original=result.original,
                processed=result.processed,
                final=final_img,
                debug=result.debug,
            )
        else:
            return result

    def _overlay_image(self, base: MatLike, overlay: MatLike) -> MatLike:
        """Overlay one image on top of another with transparency.

        Args:
            base: The base image (H x W x 3).
            overlay: The overlay image with alpha channel (H x W x 4).
        """
        # Extract RGB channels and alpha channel from overlay image
        overlay_rgb = overlay[:, :, :3]
        overlay_alpha = overlay[:, :, 3]
        # Create mask by thresholding alpha channel
        _, base_mask = cv2.threshold(overlay_alpha, 0, 255, cv2.THRESH_BINARY_INV)
        # # Invert mask to create background mask
        # base_mask = cv2.bitwise_not(mask)
        # Apply background mask to background image
        base_masked = cv2.bitwise_and(base, base, mask=base_mask)
        # Combine masked background image and overlay image
        return cv2.bitwise_or(base_masked, overlay_rgb)

    def _on_process_image_finished(self, result: QuadratDetectionResult, token: int) -> None:
        """Handle worker finished processing the image."""
        # logger.debug("Finishing processing...")
        # Only update the display if this is the latest request
        if token != self._latest_token:
            logger.debug("Finishing processing, skipped: not latest")
            return
        # Only update the display if there is a result
        if result is None or result.processed is None:
            logger.debug("Finishing processing, skipped: no result")
            return

        def apply() -> None:
            try:
                # logger.debug("Combining images...")

                display_img: MatLike | None
                if self.view_original_button.isChecked():
                    display_img = result.original
                elif self.view_processed_button.isChecked():
                    display_img = result.processed
                elif self.view_debug_button.isChecked():
                    display_img = result.debug
                elif self.view_final_button.isChecked():
                    display_img = result.final
                else:
                    display_img = None  # will be handled below
                #
                # if (
                #     display_img is not None
                #     and self.view_debug_button.isChecked()
                #     and result.debug is not None
                # ):
                #     debug_img = result.debug
                #     # Overlay debug image on display image
                #     if self.view_processed_button.isChecked():
                #         bgr_img = cv2.cvtColor(display_img, cv2.COLOR_GRAY2BGR)
                #     elif self.view_final_button.isChecked():
                #         bgr_img = debug_img
                #     else:
                #         bgr_img = display_img
                #     display_img = self._overlay_image(bgr_img, debug_img)

                # logger.debug("Converting image...")
                qimg = array2qimage(display_img)
                # h, w = result.shape[:2]
                # bytes_per_line = result.strides[0]
                # self._image_ref = result
                # qformat = QtGui.QImage.Format.Format_Grayscale8
                # qimg = QtGui.QImage(self._image_ref.data, w, h, bytes_per_line, qformat)
                # logger.debug("Converted image")

                # logger.debug("Displaying image...")
                qpixmap = QtGui.QPixmap.fromImage(qimg)
                self.central_widget.pixmap = qpixmap
                self.central_widget.message = ""
                # logger.debug("Displayed image.")
            except Exception as e:
                logger.error("Error displaying image", exc_info=e)
                self.central_widget.message = f"Error: {e}"

        # Schedule the UI update on the main thread using a single-shot timer
        # logger.debug("Scheduling display on UI...")
        QtCore.QTimer.singleShot(0, apply)
        logger.debug("Scheduled display on UI")


def sigint_handler(*_args: Any) -> None:
    """Handle the SIGINT signal."""
    sys.stderr.write("\r")
    QApplication.quit()


signal_timer: QTimer


def setup_sigint_handler(interval: int = 200) -> None:
    """Process any pending SIGINT signals."""
    # Based on: https://stackoverflow.com/a/4939113/146622
    # The Qt application main event loop doesn't run on the Python interpreter, so it doesn't process signals.
    # Setup timer to periodically run the Python interpreter to check for (SIGINT) signals from outside.

    global signal_timer  # Prevent garbage collection # noqa: PLW0603

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
