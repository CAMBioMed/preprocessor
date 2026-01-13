from PySide6.QtCore import QObject, Signal

from preprocessor.model.list_model import QListModel
from preprocessor.model.photo_model import PhotoModel


class ProjectModel(QObject):
    """
    The model for the entire current project.

    This includes the project-specific settings.
    """

    on_changed: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        _photos = QListModel[PhotoModel](parent = self)

    _photos: QListModel[PhotoModel]

    @property
    def photos(self) -> QListModel[PhotoModel]:
        """The list of photos in the project."""
        return self._photos

