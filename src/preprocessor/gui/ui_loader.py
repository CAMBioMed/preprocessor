import os
import pathlib
from typing import cast

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget


class UILoader:
    """A wrapper for Qt's .ui file loader."""

    path = pathlib.Path(os.path.dirname(__file__))
    loader = QUiLoader()

    @classmethod
    def load(cls, name: str) -> QWidget:
        """
        Load up a .ui file and return it.

        :param name: The name of the .ui file to load, relative to this class and without the .ui extension.
        :return: The QWidget created from the UI file.
        """
        ui_path = str(cls.path / f"{name}.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.OpenModeFlag.ReadOnly)

        return cast(QWidget, cls.loader.load(ui_file))
