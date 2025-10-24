import sys

from PySide6 import QtGui
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import *


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
                self.text_edit.setPlainText(open(path).read())

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

    def on_button_clicked(self):
        self.label.setText('Button Clicked!')