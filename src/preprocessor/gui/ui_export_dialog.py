# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_dialog.ui'
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
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        ExportDialog.resize(597, 155)
        self.verticalLayout = QVBoxLayout(ExportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frmMain = QScrollArea(ExportDialog)
        self.frmMain.setObjectName(u"frmMain")
        self.frmMain.setFrameShape(QFrame.Shape.NoFrame)
        self.frmMain.setWidgetResizable(True)
        self.layMain = QWidget()
        self.layMain.setObjectName(u"layMain")
        self.layMain.setGeometry(QRect(0, 0, 573, 78))
        self.formLayout_2 = QFormLayout(self.layMain)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lblOutputDirectory = QLabel(self.layMain)
        self.lblOutputDirectory.setObjectName(u"lblOutputDirectory")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblOutputDirectory)

        self.layOutputDir = QHBoxLayout()
        self.layOutputDir.setObjectName(u"layOutputDir")
        self.txtOutputDir = QLineEdit(self.layMain)
        self.txtOutputDir.setObjectName(u"txtOutputDir")

        self.layOutputDir.addWidget(self.txtOutputDir)

        self.btnOutputDir = QPushButton(self.layMain)
        self.btnOutputDir.setObjectName(u"btnOutputDir")

        self.layOutputDir.addWidget(self.btnOutputDir)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.layOutputDir)

        self.frmMain.setWidget(self.layMain)

        self.verticalLayout.addWidget(self.frmMain)

        self.line = QFrame(ExportDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.btnsDialog = QDialogButtonBox(ExportDialog)
        self.btnsDialog.setObjectName(u"btnsDialog")
        self.btnsDialog.setOrientation(Qt.Orientation.Horizontal)
        self.btnsDialog.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.SaveAll)
        self.btnsDialog.setCenterButtons(False)

        self.verticalLayout.addWidget(self.btnsDialog)


        self.retranslateUi(ExportDialog)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Export", None))
        self.lblOutputDirectory.setText(QCoreApplication.translate("ExportDialog", u"Output directory:", None))
        self.btnOutputDir.setText(QCoreApplication.translate("ExportDialog", u"Browse", None))
    # retranslateUi

