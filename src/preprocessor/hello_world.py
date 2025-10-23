import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

def show_ui():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # Ensure the QML import path includes the module directory
    engine.addImportPath(str(Path(__file__).resolve().parent))
    qml_file = Path(__file__).resolve().parent / "hello_world.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)