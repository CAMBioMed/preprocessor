# Manually created
from PySide6.QtCore import QSize, QMetaObject, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QToolBar, QDockWidget, QGridLayout, QListView


class Ui_ThumbnailDock(object):
    """Provides thumbnail dock UI."""

    dockWidgetContents: QWidget
    mainLayout: QGridLayout
    toolbar: QToolBar
    addPhotoAction: QAction
    removePhotoAction: QAction
    thumbnailListWidget: QListWidget

    def setupUi(self, parent: QDockWidget) -> None:
        if not parent.objectName():
            parent.setObjectName(u"ThumbnailDock")
        parent.resize(200, 150)

        # Contents
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")

        # Contents layout
        self.mainLayout = QGridLayout(self.dockWidgetContents)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Toolbar
        self.toolbar = QToolBar(self.dockWidgetContents)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setOrientation(Qt.Orientation.Vertical)
        self.mainLayout.addWidget(self.toolbar, 0, 0, 1, 1)

        # Toolbar actions
        self.addPhotoAction = QAction("&Add Photos...", parent)
        self.addPhotoAction.setStatusTip("Add photos to the project.")
        self.toolbar.addAction(self.addPhotoAction)

        self.removePhotoAction = QAction("&Remove Photos", parent)
        self.removePhotoAction.setStatusTip("Remove photos from the project.")
        self.toolbar.addAction(self.removePhotoAction)

        # Thumbnail list
        self.thumbnailListWidget = QListWidget(self.dockWidgetContents)
        self.thumbnailListWidget.setObjectName(u"thumbnailListWidget")
        self.thumbnailListWidget.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumbnailListWidget.setIconSize(QSize(120, 120))
        self.thumbnailListWidget.setSpacing(10)
        self.thumbnailListWidget.setFlow(QListView.Flow.LeftToRight)
        self.thumbnailListWidget.setMovement(QListView.Movement.Static)
        self.thumbnailListWidget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumbnailListWidget.setWrapping(False)
        self.mainLayout.addWidget(self.thumbnailListWidget, 0, 1, 1, 1)

        parent.setWidget(self.dockWidgetContents)

        # QMetaObject.connectSlotsByName(parent)