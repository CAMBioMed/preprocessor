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
        # Serialize each PhotoModel using its serialize() method
        return {
            "photos": [p.serialize() for p in self.photos],
        }

    def deserialize(self, data: dict) -> None:
        """
        Deserialize state from a dict produced by serialize.
        Uses the setters so signals are emitted only on change.
        If a key doesn't occur in the data, it is not set.
        """
        if "photos" in data:
            photos_raw = data.get("photos", None)
            # If explicit None -> clear list
            if photos_raw is None:
                # remove existing photos
                # clear the QListModel by removing items
                # iterate copy to avoid modification during iteration
                for item in list(self.photos):
                    self.photos.remove(item)
                # Signal that project changed
                self.on_changed.emit()
            else:
                # Expecting iterable of dicts
                # Clear existing photos first
                for item in list(self.photos):
                    self.photos.remove(item)
                # Recreate PhotoModel instances from serialized data
                for pic_data in photos_raw:
                    photo = PhotoModel()
                    # Let the photo deserialize itself (will emit its own signals)
                    photo.deserialize(pic_data)
                    self.photos.append(photo)
                # Signal that project changed
                self.on_changed.emit()
