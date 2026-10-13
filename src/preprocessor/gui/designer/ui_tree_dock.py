# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tree_dock.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QHeaderView,
    QSizePolicy, QTreeView, QWidget)

class Ui_TreeDock(object):
    def setupUi(self, TreeDock):
        if not TreeDock.objectName():
            TreeDock.setObjectName(u"TreeDock")
        TreeDock.resize(400, 300)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.treeView = QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setHeaderHidden(True)

        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)

        TreeDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(TreeDock)

        QMetaObject.connectSlotsByName(TreeDock)
    # setupUi

    def retranslateUi(self, TreeDock):
        TreeDock.setWindowTitle(QCoreApplication.translate("TreeDock", u"Directories", None))
    # retranslateUi

