import sys
import traceback
from types import TracebackType
from typing import Any
import signal

import PySide6

from preprocessor import app_version, app_organisation, app_domain, app_name, app_formal_name
from preprocessor.gui.launch_dialog import LaunchDialog
from preprocessor.gui.main_window import MainWindow
from preprocessor.model.application_model import ApplicationModel
from PySide6 import QtGui
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QDialog,
)

import logging


def main_gui() -> None:
    """Show the main application window."""
    try:
        setup_logging()
        sys.excepthook = _excepthook

        # Disable allocation limit
        QtGui.QImageReader.setAllocationLimit(0)

        QCoreApplication.setOrganizationName(app_organisation)
        QCoreApplication.setOrganizationDomain(app_domain)
        QCoreApplication.setApplicationName(app_name)

        app = QApplication(sys.argv)
        app.setApplicationName(app_formal_name)
        app.setApplicationVersion(app_version)

        # Setup application model
        model = ApplicationModel()
        model.read_settings()

        _setup_sigint_handler()

        # Show launch dialog
        if LaunchDialog(model).exec() == QDialog.DialogCode.Accepted:
            window = MainWindow(model)
            window.show()
            exit_code = app.exec()
            sys.exit(exit_code)
        else:
            sys.exit(1)
    except Exception as e:
        logging.getLogger("preprocessor").exception("Unhandled exception in main_gui: %s", e)
        raise


def _show_main_window(model: ApplicationModel) -> None:
    window = MainWindow(model)
    window.show()
    _setup_sigint_handler()


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("preprocessor")
    logger.info("Logging is set up.")


def main() -> None:
    setup_logging()

    logger = logging.getLogger(__name__)

    pyside_version = getattr(PySide6, "__version__", "unknown")
    qtcore_version = getattr(getattr(PySide6, "QtCore", None), "__version__", "unknown")

    logger.info(f"Starting {app_formal_name} {app_version}...")
    logger.info("Python: %s", sys.version)
    logger.info("PySide6: %s", pyside_version)
    logger.info("QtCore: %s", qtcore_version)

    main_gui()


def _excepthook(cls: type[BaseException], exception: BaseException, traceback_obj: TracebackType | None) -> None:
    """Handle uncaught exceptions including Qt errors."""
    # Build the error message string
    error_msg = f"{cls.__name__}: {exception}\n\n"
    error_msg += "".join(traceback.format_tb(traceback_obj))

    logger = logging.getLogger("preprocessor")
    logger.exception("Fatal error: %s", error_msg)

    # If Qt is initialized, show a message box
    if QApplication.instance() is not None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f"{app_formal_name} Fatal Error")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("We're sorry, an unexpected fatal error occurred.")
        msg_box.setDetailedText(error_msg)
        msg_box.resize(600, 1000)

        msg_box.addButton(QMessageBox.StandardButton.Abort)

        msg_box.exec()

    sys.__excepthook__(cls, exception, traceback_obj)
    sys.exit(1)


def sigint_handler(*_args: Any) -> None:
    """Handle the SIGINT signal."""
    sys.stderr.write("\r")
    QApplication.quit()


signal_timer: QTimer


def _setup_sigint_handler(interval: int = 200) -> None:
    """Process any pending SIGINT signals."""
    # Based on: https://stackoverflow.com/a/4939113/146622
    # The Qt application main event loop doesn't run on the Python interpreter, so it doesn't process signals.
    # Setup timer to periodically run the Python interpreter to check for (SIGINT) signals from outside.

    global signal_timer  # Prevent garbage collection # noqa: PLW0603

    signal.signal(signal.SIGINT, sigint_handler)
    signal_timer = QTimer()
    signal_timer.start(interval)
    signal_timer.timeout.connect(lambda: None)  # Let the interpreter run each time.


if __name__ == "__main__":
    main()
