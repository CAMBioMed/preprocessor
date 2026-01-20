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
        # store the photos list on the instance
        self._photos = QListModel[PhotoModel](parent = self)

    _photos: QListModel[PhotoModel]

    @property
    def photos(self) -> QListModel[PhotoModel]:
        """The list of photos in the project."""
        return self._photos

    def serialize(self) -> dict:
        """
        Serialize this model into basic Python types suitable for JSON.
        """
        pass

    def deserialize(self, data: dict) -> None:
        """
        Deserialize state from a dict produced by serialize.
        Uses the setters so signals are emitted only on change.
        If a key doesn't occur in the data, it is not set.
        """
        pass
