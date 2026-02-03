# Convery UI files
UI files, produced by Qt Creator, can be converted to Python files using the `pyside6-uic` tool.

```shell
uv run pyside6-uic src/preprocessor/gui/properties_dock.ui -o src/preprocessor/gui/properties_dock.py
```

They can also be loaded directly, for example:

```python
import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

def mainwindow_setup(w):
    w.setWindowTitle("MainWindow Title")

app = QtWidgets.QApplication(sys.argv)

window = loader.load("main.ui", None)
mainwindow_setup(window)
window.show()
app.exec()
```