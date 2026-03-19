import sys
import traceback
from types import TracebackType
from typing import Any
import signal
from pathlib import Path

import PySide6

from preprocessor import app_version, app_organisation, app_domain, app_name, app_formal_name
from preprocessor.gui.launch_dialog import LaunchDialog, open_project
from preprocessor.gui.main_window import MainWindow
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.project_model import ProjectModel
from PySide6 import QtGui
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QDialog,
)

import logging
import click

def setup_excepthook() -> None:
    """Set up the global exception hook to catch uncaught exceptions and show an error message box."""
    sys.excepthook = _excepthook

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