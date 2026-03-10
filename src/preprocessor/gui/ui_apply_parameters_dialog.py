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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(610, 463)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblSummary = QLabel(Dialog)
        self.lblSummary.setObjectName(u"lblSummary")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSummary.sizePolicy().hasHeightForWidth())
        self.lblSummary.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.lblSummary)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblColorCorrection = QLabel(Dialog)
        self.lblColorCorrection.setObjectName(u"lblColorCorrection")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblColorCorrection)

        self.chkColorCorrection = QCheckBox(Dialog)
        self.chkColorCorrection.setObjectName(u"chkColorCorrection")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chkColorCorrection)

        self.lblLensCorrection = QLabel(Dialog)
        self.lblLensCorrection.setObjectName(u"lblLensCorrection")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblLensCorrection)

        self.chkLensCorrection = QCheckBox(Dialog)
        self.chkLensCorrection.setObjectName(u"chkLensCorrection")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chkLensCorrection)

        self.lblCrop = QLabel(Dialog)
        self.lblCrop.setObjectName(u"lblCrop")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblCrop)

        self.chkCrop = QCheckBox(Dialog)
        self.chkCrop.setObjectName(u"chkCrop")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chkCrop)

        self.lblMetadata = QLabel(Dialog)
        self.lblMetadata.setObjectName(u"lblMetadata")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblMetadata)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.chkMetadataDate = QCheckBox(Dialog)
        self.chkMetadataDate.setObjectName(u"chkMetadataDate")

        self.verticalLayout_2.addWidget(self.chkMetadataDate)

        self.chkMetadataPartner = QCheckBox(Dialog)
        self.chkMetadataPartner.setObjectName(u"chkMetadataPartner")

        self.verticalLayout_2.addWidget(self.chkMetadataPartner)

        self.chkMetadataArea = QCheckBox(Dialog)
        self.chkMetadataArea.setObjectName(u"chkMetadataArea")

        self.verticalLayout_2.addWidget(self.chkMetadataArea)

        self.chkMetadataSite = QCheckBox(Dialog)
        self.chkMetadataSite.setObjectName(u"chkMetadataSite")

        self.verticalLayout_2.addWidget(self.chkMetadataSite)

        self.chkMetadataSeason = QCheckBox(Dialog)
        self.chkMetadataSeason.setObjectName(u"chkMetadataSeason")

        self.verticalLayout_2.addWidget(self.chkMetadataSeason)

        self.checkBox_6 = QCheckBox(Dialog)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout_2.addWidget(self.checkBox_6)

        self.checkBox_7 = QCheckBox(Dialog)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.verticalLayout_2.addWidget(self.checkBox_7)

        self.checkBox_8 = QCheckBox(Dialog)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.verticalLayout_2.addWidget(self.checkBox_8)

        self.checkBox_9 = QCheckBox(Dialog)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.verticalLayout_2.addWidget(self.checkBox_9)

        self.checkBox_10 = QCheckBox(Dialog)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.verticalLayout_2.addWidget(self.checkBox_10)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(4, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)


        self.verticalLayout.addLayout(self.formLayout)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(100, 0))
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lblSummary.setText(QCoreApplication.translate("Dialog", u"Select the parameters to copy to the other photos.", None))
        self.lblColorCorrection.setText(QCoreApplication.translate("Dialog", u"Color correction:", None))
        self.chkColorCorrection.setText("")
        self.lblLensCorrection.setText(QCoreApplication.translate("Dialog", u"Lens correction:", None))
        self.chkLensCorrection.setText("")
        self.lblCrop.setText(QCoreApplication.translate("Dialog", u"Crop:", None))
        self.chkCrop.setText("")
        self.lblMetadata.setText(QCoreApplication.translate("Dialog", u"Metadata:", None))
        self.chkMetadataDate.setText(QCoreApplication.translate("Dialog", u"Date", None))
        self.chkMetadataPartner.setText(QCoreApplication.translate("Dialog", u"Partner", None))
        self.chkMetadataArea.setText(QCoreApplication.translate("Dialog", u"Area", None))
        self.chkMetadataSite.setText(QCoreApplication.translate("Dialog", u"Site", None))
        self.chkMetadataSeason.setText(QCoreApplication.translate("Dialog", u"Season", None))
        self.checkBox_6.setText(QCoreApplication.translate("Dialog", u"Transect", None))
        self.checkBox_7.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_8.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_9.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_10.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
    # retranslateUi

