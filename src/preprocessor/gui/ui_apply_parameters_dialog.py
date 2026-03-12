# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'apply_parameters_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ApplyParametersDialog(object):
    def setupUi(self, ApplyParametersDialog):
        if not ApplyParametersDialog.objectName():
            ApplyParametersDialog.setObjectName(u"ApplyParametersDialog")
        ApplyParametersDialog.resize(435, 238)
        self.horizontalLayout = QHBoxLayout(ApplyParametersDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblSummary = QLabel(ApplyParametersDialog)
        self.lblSummary.setObjectName(u"lblSummary")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSummary.sizePolicy().hasHeightForWidth())
        self.lblSummary.setSizePolicy(sizePolicy)
        self.lblSummary.setWordWrap(True)

        self.verticalLayout.addWidget(self.lblSummary)

        self.scrollArea = QScrollArea(ApplyParametersDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 287, 168))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.lblParameters = QLabel(self.scrollAreaWidgetContents)
        self.lblParameters.setObjectName(u"lblParameters")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblParameters)

        self.chkColorCorrection = QCheckBox(self.scrollAreaWidgetContents)
        self.chkColorCorrection.setObjectName(u"chkColorCorrection")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chkColorCorrection)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(3, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)

        self.chkLensCorrection = QCheckBox(self.scrollAreaWidgetContents)
        self.chkLensCorrection.setObjectName(u"chkLensCorrection")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chkLensCorrection)

        self.chkCrop = QCheckBox(self.scrollAreaWidgetContents)
        self.chkCrop.setObjectName(u"chkCrop")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chkCrop)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.btnButtons = QDialogButtonBox(ApplyParametersDialog)
        self.btnButtons.setObjectName(u"btnButtons")
        self.btnButtons.setMinimumSize(QSize(100, 0))
        self.btnButtons.setOrientation(Qt.Orientation.Vertical)
        self.btnButtons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.btnButtons.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.btnButtons)


        self.retranslateUi(ApplyParametersDialog)
        self.btnButtons.accepted.connect(ApplyParametersDialog.accept)
        self.btnButtons.rejected.connect(ApplyParametersDialog.reject)

        QMetaObject.connectSlotsByName(ApplyParametersDialog)
    # setupUi

    def retranslateUi(self, ApplyParametersDialog):
        ApplyParametersDialog.setWindowTitle(QCoreApplication.translate("ApplyParametersDialog", u"Apply", None))
        self.lblSummary.setText(QCoreApplication.translate("ApplyParametersDialog", u"Select the parameters to copy from the opened photo to the selected photos.", None))
        self.lblParameters.setText(QCoreApplication.translate("ApplyParametersDialog", u"Parameters:", None))
        self.chkColorCorrection.setText(QCoreApplication.translate("ApplyParametersDialog", u"Color correction", None))
        self.chkLensCorrection.setText(QCoreApplication.translate("ApplyParametersDialog", u"Lens correction", None))
        self.chkCrop.setText(QCoreApplication.translate("ApplyParametersDialog", u"Crop", None))
    # retranslateUi

