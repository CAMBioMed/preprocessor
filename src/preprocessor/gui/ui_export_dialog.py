# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_dialog.ui'
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
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        ExportDialog.resize(597, 317)
        self.verticalLayout = QVBoxLayout(ExportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(ExportDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 573, 223))
        self.formLayout_2 = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lblOutputDirectory = QLabel(self.scrollAreaWidgetContents)
        self.lblOutputDirectory.setObjectName(u"lblOutputDirectory")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblOutputDirectory)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtOutputDir = QLineEdit(self.scrollAreaWidgetContents)
        self.txtOutputDir.setObjectName(u"txtOutputDir")

        self.horizontalLayout_2.addWidget(self.txtOutputDir)

        self.btnOutputDir = QPushButton(self.scrollAreaWidgetContents)
        self.btnOutputDir.setObjectName(u"btnOutputDir")

        self.horizontalLayout_2.addWidget(self.btnOutputDir)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.frame = QFrame(ExportDialog)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.prbProgress = QProgressBar(self.frame)
        self.prbProgress.setObjectName(u"prbProgress")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(6)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.prbProgress.sizePolicy().hasHeightForWidth())
        self.prbProgress.setSizePolicy(sizePolicy1)
        self.prbProgress.setValue(24)

        self.horizontalLayout.addWidget(self.prbProgress)

        self.lblProgress_Status = QLabel(self.frame)
        self.lblProgress_Status.setObjectName(u"lblProgress_Status")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblProgress_Status.sizePolicy().hasHeightForWidth())
        self.lblProgress_Status.setSizePolicy(sizePolicy2)
        self.lblProgress_Status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.lblProgress_Status)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.lblProgress = QLabel(self.frame)
        self.lblProgress.setObjectName(u"lblProgress")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblProgress)


        self.verticalLayout.addWidget(self.frame)

        self.dialogButtons = QDialogButtonBox(ExportDialog)
        self.dialogButtons.setObjectName(u"dialogButtons")
        self.dialogButtons.setOrientation(Qt.Orientation.Horizontal)
        self.dialogButtons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.SaveAll)
        self.dialogButtons.setCenterButtons(False)

        self.verticalLayout.addWidget(self.dialogButtons)


        self.retranslateUi(ExportDialog)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Export", None))
        self.lblOutputDirectory.setText(QCoreApplication.translate("ExportDialog", u"Output directory:", None))
        self.btnOutputDir.setText(QCoreApplication.translate("ExportDialog", u"Browse", None))
        self.lblProgress_Status.setText(QCoreApplication.translate("ExportDialog", u"0/100 (0%)", None))
        self.lblProgress.setText(QCoreApplication.translate("ExportDialog", u"Progress:", None))
    # retranslateUi

