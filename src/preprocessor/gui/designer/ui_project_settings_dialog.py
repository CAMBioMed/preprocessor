# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_settings_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_ProjectSettingsDialog(object):
    def setupUi(self, ProjectSettingsDialog):
        if not ProjectSettingsDialog.objectName():
            ProjectSettingsDialog.setObjectName(u"ProjectSettingsDialog")
        ProjectSettingsDialog.resize(649, 470)
        self.verticalLayout = QVBoxLayout(ProjectSettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabs = QTabWidget(ProjectSettingsDialog)
        self.tabs.setObjectName(u"tabs")
        self.tabSettings = QWidget()
        self.tabSettings.setObjectName(u"tabSettings")
        self.formLayout_2 = QFormLayout(self.tabSettings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.labelExplanation = QLabel(self.tabSettings)
        self.labelExplanation.setObjectName(u"labelExplanation")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.labelExplanation)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout_2.setItem(1, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)

        self.labelEmpty = QLabel(self.tabSettings)
        self.labelEmpty.setObjectName(u"labelEmpty")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelEmpty)

        self.tabs.addTab(self.tabSettings, "")

        self.verticalLayout.addWidget(self.tabs)

        self.btnsDialog = QDialogButtonBox(ProjectSettingsDialog)
        self.btnsDialog.setObjectName(u"btnsDialog")
        self.btnsDialog.setOrientation(Qt.Orientation.Horizontal)
        self.btnsDialog.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.btnsDialog)


        self.retranslateUi(ProjectSettingsDialog)
        self.btnsDialog.accepted.connect(ProjectSettingsDialog.accept)
        self.btnsDialog.rejected.connect(ProjectSettingsDialog.reject)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ProjectSettingsDialog)
    # setupUi

    def retranslateUi(self, ProjectSettingsDialog):
        ProjectSettingsDialog.setWindowTitle(QCoreApplication.translate("ProjectSettingsDialog", u"Dialog", None))
        self.labelExplanation.setText(QCoreApplication.translate("ProjectSettingsDialog", u"(no settings available)", None))
        self.labelEmpty.setText("")
        self.tabs.setTabText(self.tabs.indexOf(self.tabSettings), QCoreApplication.translate("ProjectSettingsDialog", u"Settings", None))
    # retranslateUi

