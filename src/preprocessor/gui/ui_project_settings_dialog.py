# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_settings_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
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
        self.tabMetadata = QWidget()
        self.tabMetadata.setObjectName(u"tabMetadata")
        self.formLayout_2 = QFormLayout(self.tabMetadata)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lblGroup = QLabel(self.tabMetadata)
        self.lblGroup.setObjectName(u"lblGroup")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblGroup)

        self.txtGroup = QLineEdit(self.tabMetadata)
        self.txtGroup.setObjectName(u"txtGroup")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txtGroup)

        self.lblSeason = QLabel(self.tabMetadata)
        self.lblSeason.setObjectName(u"lblSeason")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblSeason)

        self.txtSeason = QLineEdit(self.tabMetadata)
        self.txtSeason.setObjectName(u"txtSeason")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txtSeason)

        self.lblArea = QLabel(self.tabMetadata)
        self.lblArea.setObjectName(u"lblArea")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblArea)

        self.txtArea = QLineEdit(self.tabMetadata)
        self.txtArea.setObjectName(u"txtArea")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtArea)

        self.lblSite = QLabel(self.tabMetadata)
        self.lblSite.setObjectName(u"lblSite")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblSite)

        self.txtSite = QLineEdit(self.tabMetadata)
        self.txtSite.setObjectName(u"txtSite")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.txtSite)

        self.lblDepth = QLabel(self.tabMetadata)
        self.lblDepth.setObjectName(u"lblDepth")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblDepth)

        self.txtDepth = QLineEdit(self.tabMetadata)
        self.txtDepth.setObjectName(u"txtDepth")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.txtDepth)

        self.lblTransect = QLabel(self.tabMetadata)
        self.lblTransect.setObjectName(u"lblTransect")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblTransect)

        self.txtTransect = QLineEdit(self.tabMetadata)
        self.txtTransect.setObjectName(u"txtTransect")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.txtTransect)

        self.tabs.addTab(self.tabMetadata, "")

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
        self.lblGroup.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Group:", None))
        self.lblSeason.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Season:", None))
        self.lblArea.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Area:", None))
        self.lblSite.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Site:", None))
        self.lblDepth.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Depth:", None))
        self.lblTransect.setText(QCoreApplication.translate("ProjectSettingsDialog", u"Transect:", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabMetadata), QCoreApplication.translate("ProjectSettingsDialog", u"Metadata", None))
    # retranslateUi

