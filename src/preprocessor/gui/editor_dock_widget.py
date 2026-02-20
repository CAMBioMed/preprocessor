from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.ui_editor_dock import Ui_EditorDock

class EditorDockWidget(QDockWidget):
    ui: Ui_EditorDock

    on_autodetect_quadrat_clicked: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_EditorDock()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.ui.btnCropping_QuadratAutodetect.clicked.connect(self.on_autodetect_quadrat_clicked.emit)