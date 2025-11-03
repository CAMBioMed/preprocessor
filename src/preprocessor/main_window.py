import sys
from pathlib import Path

import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import *
from cv2.typing import MatLike

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
        self.label = QLabel('Hello PySide6!')
        add_widget_with_label(main_layout, self.label, 'QLabel:')

        # QPushButton
        self.button = QPushButton('Click Me')
        self.button.clicked.connect(self.on_button_clicked)
        add_widget_with_label(main_layout, self.button, 'QPushButton:')

        # QLineEdit
        self.line_edit = QLineEdit()
        add_widget_with_label(main_layout, self.line_edit, 'QLineEdit:')

        # QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Option 1', 'Option 2', 'Option 3'])
        add_widget_with_label(main_layout, self.combo_box, 'QComboBox:')

        # QCheckBox
        self.check_box = QCheckBox('Check Me')
        add_widget_with_label(main_layout, self.check_box, 'QCheckBox:')

        # QRadioButton
        self.radio_button = QRadioButton('Radio Button')
        add_widget_with_label(main_layout, self.radio_button, 'QRadioButton:')

        # QTextEdit
        self.text_edit = QTextEdit()
        add_widget_with_label(main_layout, self.text_edit, 'QTextEdit:')

        # QSlider
        self.slider = QSlider()
        add_widget_with_label(main_layout, self.slider, 'QSlider:')

        # QSpinBox
        self.spin_box = QSpinBox()
        add_widget_with_label(main_layout, self.spin_box, 'QSpinBox:')

        # QProgressBar
        self.progress_bar = QProgressBar()
        add_widget_with_label(main_layout, self.progress_bar, 'QProgressBar:')

        # Image display label
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 300)
        self.image_label.setScaledContents(True)
        add_widget_with_label(main_layout, self.image_label, 'Image:')

        # Track the current image path (defaults to module-level image_file)
        self.current_image_path = str(image_file)

        # Sliders
        self.slider1 = QSlider()
        self.slider1.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(500)
        self.slider1.setTickInterval(10)
        self.slider1.setValue(100)
        add_widget_with_label(main_layout, self.slider1, 'Threshold 1:')

        self.slider2 = QSlider()
        self.slider2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(500)
        self.slider2.setTickInterval(10)
        self.slider2.setValue(150)
        add_widget_with_label(main_layout, self.slider2, 'Threshold 2:')

        # Update the image whenever a slider value changes
        self.slider1.valueChanged.connect(lambda _val: self.on_slider_changed())
        self.slider2.valueChanged.connect(lambda _val: self.on_slider_changed())

        # QTableWidget
        self.table_widget = QTableWidget(5, 3)
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f"Cell {i + 1},{j + 1}")
                self.table_widget.setItem(i, j, item)
        add_widget_with_label(main_layout, self.table_widget, 'QTableWidget:')

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
            text = "<center>" \
                   "<h1>Example</h1>" \
                   "&#8291;" \
                   "<img src=icon.svg>" \
                   "</center>" \
                   "<p>Version 31.4.159.265358<br/>" \
                   "Copyright &copy; Company Inc.</p>"
            QMessageBox.about(self, "About Example", text)

        about_action.triggered.connect(show_about_dialog)

        # Show the default image at startup (if available)
        try:
            if hasattr(self, 'current_image_path') and self.current_image_path:
                self.display_image(self.current_image_path)
        except Exception:
            pass

    def on_button_clicked(self):
        self.label.setText('Button Clicked!')

    def on_slider_changed(self) -> None:
        """Called when either slider changes; re-run show_image on the currently-displayed image."""
        try:
            if hasattr(self, 'current_image_path') and self.current_image_path:
                self.display_image(self.current_image_path)
        except Exception:
            # don't allow slider updates to crash the UI
            pass

    def display_image(self, image_path: str) -> None:
        """
        Load the image via show_image, convert to QImage/QPixmap and set on the QLabel.
        Keeps a reference to the NumPy array in self._image_ref to prevent GC.
        """
        img = self.show_image(image_path)
        if img is None:
            return
        h, w = img.shape[:2]
        bytes_per_line = img.strides[0]
        # keep a reference so QImage doesn't point to freed memory
        self._image_ref = img
        qimg = QtGui.QImage(self._image_ref.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pix)

    def show_image(self, image_path: str) -> MatLike:
        # guard: if the path is falsy or the file can't be read, return None
        if not image_path:
            return None
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            return None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        threshold1 = int(self.slider1.value()) if hasattr(self, 'slider1') else 100
        threshold2 = int(self.slider2.value()) if hasattr(self, 'slider2') else 150
        edges = cv2.Canny(blurred, threshold1, threshold2)
        return edges
