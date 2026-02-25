# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launch_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_LaunchDialog(object):
    def setupUi(self, LaunchDialog):
        if not LaunchDialog.objectName():
            LaunchDialog.setObjectName(u"LaunchDialog")
        LaunchDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        LaunchDialog.resize(450, 333)
        self.gridLayout = QGridLayout(LaunchDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.grpRecent = QGroupBox(LaunchDialog)
        self.grpRecent.setObjectName(u"grpRecent")
        self.gridLayout_2 = QGridLayout(self.grpRecent)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lstRecent = QListWidget(self.grpRecent)
        self.lstRecent.setObjectName(u"lstRecent")

        self.gridLayout_2.addWidget(self.lstRecent, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.grpRecent, 0, 0, 1, 1)

        self.layButtons = QVBoxLayout()
        self.layButtons.setObjectName(u"layButtons")
        self.btnNewProject = QPushButton(LaunchDialog)
        self.btnNewProject.setObjectName(u"btnNewProject")

        self.layButtons.addWidget(self.btnNewProject)

        self.btnBrowse = QPushButton(LaunchDialog)
        self.btnBrowse.setObjectName(u"btnBrowse")

        self.layButtons.addWidget(self.btnBrowse)

        self.btnOpenSelected = QPushButton(LaunchDialog)
        self.btnOpenSelected.setObjectName(u"btnOpenSelected")

        self.layButtons.addWidget(self.btnOpenSelected)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layButtons.addItem(self.verticalSpacer)

        self.btnExit = QPushButton(LaunchDialog)
        self.btnExit.setObjectName(u"btnExit")

        self.layButtons.addWidget(self.btnExit)


        self.gridLayout.addLayout(self.layButtons, 0, 1, 1, 1)


        self.retranslateUi(LaunchDialog)

        QMetaObject.connectSlotsByName(LaunchDialog)
    # setupUi

    def retranslateUi(self, LaunchDialog):
        self.grpRecent.setTitle(QCoreApplication.translate("LaunchDialog", u"Recent Projects", None))
        self.btnNewProject.setText(QCoreApplication.translate("LaunchDialog", u"New Project...", None))
        self.btnBrowse.setText(QCoreApplication.translate("LaunchDialog", u"Browse Project...", None))
        self.btnOpenSelected.setText(QCoreApplication.translate("LaunchDialog", u"Open Selected", None))
        self.btnExit.setText(QCoreApplication.translate("LaunchDialog", u"Exit", None))
        pass
    # retranslateUi

