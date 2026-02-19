import sys
import traceback
from types import TracebackType
from typing import Any
import signal

import click
import PySide6

from preprocessor.gui.launch_dialog import LaunchDialog
from preprocessor.gui.main_window import MainWindow
from preprocessor.model.application_model import ApplicationModel
from ._version import __version__  # type: ignore
from PySide6 import QtGui
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox, QDialog,
)

import logging


@click.group()
def cli() -> None:
    pass


@cli.command()
def version() -> None:
    click.echo(f"CAMBioMed Preprocessor {__version__}")
    # use getattr to avoid mypy errors when stubs don't expose __version__
    pyside_ver = getattr(PySide6, "__version__", "unknown")
    qtcore_ver = getattr(getattr(PySide6, "QtCore", None), "__version__", "unknown")
    click.echo(f"  PySide6: {pyside_ver}")
    click.echo(f"  PySide6 QtCore: {qtcore_ver}")


@cli.command()
def gui() -> None:
    """Show the main application window."""
    try:
        setup_logging()
        sys.excepthook = _excepthook

        # Disable allocation limit
        QtGui.QImageReader.setAllocationLimit(0)

        QCoreApplication.setOrganizationName("CAMBioMed")
        QCoreApplication.setOrganizationDomain("cambiomed-biodiversa.com")
        QCoreApplication.setApplicationName("Preprocessor")

        app = QApplication(sys.argv)
        app.setApplicationName("CAMBioMed Preprocessor")
        app.setApplicationVersion(__version__)

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
    cli()


def main_gui() -> None:
    gui()


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
        msg_box.setWindowTitle("CAMBioMed Preprocessor Fatal Error")
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
