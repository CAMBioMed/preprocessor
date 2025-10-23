import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

def show_ui():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.load("src/preprocessor/hello_world.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)