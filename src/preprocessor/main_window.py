import contextlib
import sys
from pathlib import Path

import cv2
from PySide6 import QtCore, QtGui

# Add Qt concurrency helpers
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


# Worker signal object to send results back to the main thread
class _WorkerSignals(QObject):
    finished = Signal(object, int)  # (result_image_or_None, token)


class _ImageWorker(QRunnable):
    """QRunnable that processes an image (read, grayscale, blur, Canny) in a worker thread.
    Emits finished(result, token) when done.
    """

    def __init__(self, image_path: str, threshold1: int, threshold2: int, token: int, preview_max_side: int = 800):
        super().__init__()
        self.image_path = image_path
        self.threshold1 = int(threshold1)
        self.threshold2 = int(threshold2)
        self.token = int(token)
        self.preview_max_side = int(preview_max_side)
        self.signals = _WorkerSignals()

    def run(self) -> None:
        # Do the image processing here (same algorithm as before) and emit the result
        result = None
        try:
            if not self.image_path:
                result = None
            else:
                img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
                if img is None:
                    result = None
                else:
                    # Downscale image for preview processing to speed up worker
                    try:
                        if self.preview_max_side and (
                            img.shape[0] > self.preview_max_side or img.shape[1] > self.preview_max_side
                        ):
                            h, w = img.shape[:2]
                            scale = float(self.preview_max_side) / float(max(h, w))
                            new_w = max(1, int(w * scale))
                            new_h = max(1, int(h * scale))
                            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    except Exception:
                        # if resizing fails for any reason, continue with original image
                        pass
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                    # WARNING: This seems to work better on the scaled down preview
                    # than on the full image. Thus, generating the final image
                    # full-scale will produce different results!
                    edges = cv2.Canny(blurred, self.threshold1, self.threshold2)
                    result = edges
        except Exception:
            # avoid allowing worker exceptions to escape
            result = None
        # Emit the result and the token so the main thread can ignore stale results
        with contextlib.suppress(Exception):
            self.signals.finished.emit(result, self.token)


image_file = Path(__file__).resolve().parent / "images" / "Kea5_3a.JPG"


def show_ui():
    # Disable allocation limit
    QtGui.QImageReader.setAllocationLimit(0)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAMBioMed Preprocessor")
        self.setGeometry(100, 100, 800, 600)

        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        def toolbar_button_clicked(s):
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

        # Status bar

        self.setStatusBar(QStatusBar(self))

        # Example widgets

        # Function to add widget with label
        def add_widget_with_label(layout, widget, label_text):
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)

        # QLabel
        self.label = QLabel("Hello PySide6!")
        add_widget_with_label(main_layout, self.label, "QLabel:")

        # QPushButton
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_clicked)
        add_widget_with_label(main_layout, self.button, "QPushButton:")

        # QLineEdit
        self.line_edit = QLineEdit()
        add_widget_with_label(main_layout, self.line_edit, "QLineEdit:")

        # QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        add_widget_with_label(main_layout, self.combo_box, "QComboBox:")

        # QCheckBox
        self.check_box = QCheckBox("Check Me")
        add_widget_with_label(main_layout, self.check_box, "QCheckBox:")

        # QRadioButton
        self.radio_button = QRadioButton("Radio Button")
        add_widget_with_label(main_layout, self.radio_button, "QRadioButton:")

        # QTextEdit
        self.text_edit = QTextEdit()
        add_widget_with_label(main_layout, self.text_edit, "QTextEdit:")

        # QSlider
        self.slider = QSlider()
        add_widget_with_label(main_layout, self.slider, "QSlider:")

        # QSpinBox
        self.spin_box = QSpinBox()
        add_widget_with_label(main_layout, self.spin_box, "QSpinBox:")

        # QProgressBar
        self.progress_bar = QProgressBar()
        add_widget_with_label(main_layout, self.progress_bar, "QProgressBar:")

        # Image display label
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 300)
        self.image_label.setScaledContents(True)
        add_widget_with_label(main_layout, self.image_label, "Image:")

        # Track the current image path (defaults to module-level image_file)
        self.current_image_path = str(image_file)

        # Thread pool for background image processing and a token for request ordering
        self.thread_pool = QThreadPool.globalInstance()
        self._latest_token = 0

        # Preview downscale maximum side (pixels) for faster preview processing
        # Set to None or 0 to disable downscaling and process full-resolution images.
        self.preview_max_side = 800

        # Debounce timer for sliders: avoid scheduling a worker on every tiny move
        self._debounce_interval_ms = 150  # milliseconds; adjust if you want a longer/shorter debounce
        self._debounce_timer = QtCore.QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(self._debounce_interval_ms)
        self._debounce_timer.timeout.connect(lambda: self.on_slider_changed())

        # Sliders with numeric value labels
        self.slider1 = QSlider()
        self.slider1.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(500)
        self.slider1.setTickInterval(10)
        self.slider1.setValue(100)
        # value label for slider1
        self.slider1_value_label = QLabel(str(self.slider1.value()))
        # container to hold slider and its numeric label
        slider1_container = QWidget()
        slider1_h = QHBoxLayout(slider1_container)
        slider1_h.setContentsMargins(0, 0, 0, 0)
        slider1_h.addWidget(self.slider1)
        slider1_h.addWidget(self.slider1_value_label)
        add_widget_with_label(main_layout, slider1_container, "Threshold 1:")

        self.slider2 = QSlider()
        self.slider2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(500)
        self.slider2.setTickInterval(10)
        self.slider2.setValue(150)
        # value label for slider2
        self.slider2_value_label = QLabel(str(self.slider2.value()))
        # container to hold slider and its numeric label
        slider2_container = QWidget()
        slider2_h = QHBoxLayout(slider2_container)
        slider2_h.setContentsMargins(0, 0, 0, 0)
        slider2_h.addWidget(self.slider2)
        slider2_h.addWidget(self.slider2_value_label)
        add_widget_with_label(main_layout, slider2_container, "Threshold 2:")

        # Update the image and numeric label whenever a slider value changes
        def _on_slider1_change(v):
            with contextlib.suppress(Exception):
                self.slider1_value_label.setText(str(v))
            # restart debounce timer; actual processing will occur when the timer fires
            try:
                self._debounce_timer.start()
            except Exception:
                # fallback to immediate processing if timer isn't available for any reason
                self.on_slider_changed()

        def _on_slider2_change(v):
            with contextlib.suppress(Exception):
                self.slider2_value_label.setText(str(v))
            # restart debounce timer; actual processing will occur when the timer fires
            try:
                self._debounce_timer.start()
            except Exception:
                # fallback to immediate processing if timer isn't available for any reason
                self.on_slider_changed()

        self.slider1.valueChanged.connect(_on_slider1_change)
        self.slider2.valueChanged.connect(_on_slider2_change)

        # QTableWidget
        self.table_widget = QTableWidget(5, 3)
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f"Cell {i + 1},{j + 1}")
                self.table_widget.setItem(i, j, item)
        add_widget_with_label(main_layout, self.table_widget, "QTableWidget:")

        # menu bar
        menubar = self.menuBar()
        menu_file = menubar.addMenu("&File")
        open_action = QAction("&Open", self)

        def open_file():
            path = QFileDialog.getOpenFileName(self, "Open")[0]
            if path:
                self.text_edit.setPlainText(str(path))
                try:
                    # remember which image is currently displayed so slider changes can re-run processing
                    self.current_image_path = path
                    self.display_image(str(path))
                except Exception:
                    # avoid crashing the UI if image loading fails
                    pass

        open_action.triggered.connect(open_file)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        menu_file.addAction(open_action)

        save_action = QAction("&Save", self)

        def save():
            pass

        save_action.triggered.connect(save)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        menu_file.addAction(save_action)

        save_as_action = QAction("Save &As...", self)

        def save_as():
            pass

        save_as_action.triggered.connect(save_as)
        menu_file.addAction(save_as_action)

        close = QAction("&Close", self)
        close.triggered.connect(self.close)
        menu_file.addAction(close)

        menu_help = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        menu_help.addAction(about_action)

        def show_about_dialog():
            text = """
                <center>
                  <h1>Example</h1>
                  &#8291;
                  <img src=icon.svg>
                </center>
                <p>
                  Version 31.4.159.265358<br/>
                  Copyright &copy; Company Inc.
                </p>
                """
            QMessageBox.about(self, "About Example", text)

        about_action.triggered.connect(show_about_dialog)

        # Show the default image at startup (if available)
        try:
            if hasattr(self, "current_image_path") and self.current_image_path:
                # schedule background processing for the default image
                self.display_image(self.current_image_path)
        except Exception:
            pass

    def on_button_clicked(self):
        self.label.setText("Button Clicked!")

    def on_slider_changed(self) -> None:
        """Called when either slider changes; re-run processing on the currently-displayed image.
        This schedules processing on the thread pool; it won't block the UI.
        """
        try:
            if hasattr(self, "current_image_path") and self.current_image_path:
                # schedule a new processing job for the current image
                self.display_image(self.current_image_path)
        except Exception:
            # don't allow slider updates to crash the UI
            pass

    def _schedule_processing(self, image_path: str) -> None:
        """Create and schedule a worker to process `image_path` with current slider values.
        Uses a token to identify the latest request so stale results are ignored.
        """
        # increment token to mark a new request
        self._latest_token += 1
        token = self._latest_token
        th1 = int(self.slider1.value()) if hasattr(self, "slider1") else 100
        th2 = int(self.slider2.value()) if hasattr(self, "slider2") else 150
        # pass preview_max_side so worker can downscale image for faster preview processing
        worker = _ImageWorker(str(image_path), th1, th2, token, getattr(self, "preview_max_side", 800))
        worker.signals.finished.connect(self._on_worker_finished)
        # optionally show a processing indicator (simple text) while worker runs
        try:
            # clear pixmap and show small text so users know processing is happening
            self.image_label.setPixmap(QtGui.QPixmap())
            self.image_label.setText("Processing...")
        except Exception:
            pass
        self.thread_pool.start(worker)

    def _on_worker_finished(self, result, token: int) -> None:
        """Handle worker completion; apply result only if it matches the latest token."""

        # Schedule the UI update on the main thread using a singleShot
        def apply_result():
            try:
                if token != self._latest_token:
                    # stale result, ignore
                    return
                if result is None:
                    # nothing to show
                    return
                self._set_image_from_array(result)
            except Exception:
                pass

        QtCore.QTimer.singleShot(0, apply_result)

    def _set_image_from_array(self, img) -> None:
        """Convert a grayscale numpy array `img` to QImage/QPixmap and set it on the label.
        Keeps a reference to the NumPy array to avoid GC issues.
        """
        if img is None:
            return
        try:
            h, w = img.shape[:2]
            bytes_per_line = img.strides[0]
            self._image_ref = img
            # choose a safe QImage format via getattr (avoid static-analysis warnings)
            qformat = getattr(QtGui.QImage, "Format_Grayscale8", None)
            if qformat is None:
                for _name in ("Format_Indexed8", "Format_RGB888", "Format_ARGB32", "Format_ARGB32_Premultiplied"):
                    qformat = getattr(QtGui.QImage, _name, None)
                    if qformat is not None:
                        break
            if qformat is None:
                qformat = getattr(QtGui.QImage, "Format_Invalid", 0)
            qimg = QtGui.QImage(self._image_ref.data, w, h, bytes_per_line, qformat)
            pix = QtGui.QPixmap.fromImage(qimg)
            self.image_label.setText("")
            self.image_label.setPixmap(pix)
        except Exception:
            # on failure, don't crash the UI
            pass

    def display_image(self, image_path: str) -> None:
        """Public API: schedule background processing of `image_path` and show result when ready.
        This replaces the previous synchronous behavior.
        """
        # remember which image is currently displayed so slider changes can re-run processing
        self.current_image_path = str(image_path)
        # schedule background processing
        self._schedule_processing(self.current_image_path)
