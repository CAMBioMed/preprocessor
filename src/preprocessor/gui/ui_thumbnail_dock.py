# Manually created
from PySide6.QtCore import QSize, QMetaObject, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QToolBar, QDockWidget, QGridLayout


class Ui_ThumbnailDock(object):
    dockWidgetContents: QWidget
    mainLayout: QGridLayout
    toolbar: QToolBar
    addPhotoAction: QAction
    removeThumbnailAction: QAction
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
        addPhotoActionIcon = QIcon.fromTheme(QIcon.ThemeIcon.InsertImage)
        self.addPhotoAction = QAction(addPhotoActionIcon, "&Add Photos...", parent)
        self.addPhotoAction.setStatusTip("Add photos to the project.")
        self.toolbar.addAction(self.addPhotoAction)
        self.removeThumbnailAction = self.toolbar.addAction("Remove Thumbnail")

        # Thumbnail list
        self.thumbnailListWidget = QListWidget(self.dockWidgetContents)
        self.thumbnailListWidget.setObjectName(u"thumbnailListWidget")
        self.thumbnailListWidget.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumbnailListWidget.setIconSize(QSize(100, 100))
        self.thumbnailListWidget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumbnailListWidget.setSpacing(10)
        self.mainLayout.addWidget(self.thumbnailListWidget, 0, 1, 1, 1)

        parent.setWidget(self.dockWidgetContents)

        QMetaObject.connectSlotsByName(parent)