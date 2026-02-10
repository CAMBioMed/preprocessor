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
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        ExportDialog.resize(597, 438)
        self.verticalLayout = QVBoxLayout(ExportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frmMain = QScrollArea(ExportDialog)
        self.frmMain.setObjectName(u"frmMain")
        self.frmMain.setFrameShape(QFrame.Shape.NoFrame)
        self.frmMain.setWidgetResizable(True)
        self.layMain = QWidget()
        self.layMain.setObjectName(u"layMain")
        self.layMain.setGeometry(QRect(0, 0, 573, 122))
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

        self.lblTargetWidth = QLabel(self.layMain)
        self.lblTargetWidth.setObjectName(u"lblTargetWidth")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblTargetWidth)

        self.layTargetWidth = QHBoxLayout()
        self.layTargetWidth.setObjectName(u"layTargetWidth")
        self.numTargetWidth = QSpinBox(self.layMain)
        self.numTargetWidth.setObjectName(u"numTargetWidth")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numTargetWidth.sizePolicy().hasHeightForWidth())
        self.numTargetWidth.setSizePolicy(sizePolicy)
        self.numTargetWidth.setMinimum(128)
        self.numTargetWidth.setMaximum(10240)

        self.layTargetWidth.addWidget(self.numTargetWidth)

        self.lblTargetWidth_Value = QLabel(self.layMain)
        self.lblTargetWidth_Value.setObjectName(u"lblTargetWidth_Value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(6)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblTargetWidth_Value.sizePolicy().hasHeightForWidth())
        self.lblTargetWidth_Value.setSizePolicy(sizePolicy1)

        self.layTargetWidth.addWidget(self.lblTargetWidth_Value)


        self.formLayout_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layTargetWidth)

        self.layTargetHeight = QHBoxLayout()
        self.layTargetHeight.setObjectName(u"layTargetHeight")
        self.numTargetHeight = QSpinBox(self.layMain)
        self.numTargetHeight.setObjectName(u"numTargetHeight")
        sizePolicy.setHeightForWidth(self.numTargetHeight.sizePolicy().hasHeightForWidth())
        self.numTargetHeight.setSizePolicy(sizePolicy)
        self.numTargetHeight.setMinimum(128)
        self.numTargetHeight.setMaximum(10240)

        self.layTargetHeight.addWidget(self.numTargetHeight)

        self.lblTargetHeight_Value = QLabel(self.layMain)
        self.lblTargetHeight_Value.setObjectName(u"lblTargetHeight_Value")
        sizePolicy1.setHeightForWidth(self.lblTargetHeight_Value.sizePolicy().hasHeightForWidth())
        self.lblTargetHeight_Value.setSizePolicy(sizePolicy1)

        self.layTargetHeight.addWidget(self.lblTargetHeight_Value)


        self.formLayout_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layTargetHeight)

        self.lblTargetHeight = QLabel(self.layMain)
        self.lblTargetHeight.setObjectName(u"lblTargetHeight")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblTargetHeight)

        self.frmMain.setWidget(self.layMain)

        self.verticalLayout.addWidget(self.frmMain)

        self.frmProgress = QFrame(ExportDialog)
        self.frmProgress.setObjectName(u"frmProgress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frmProgress.sizePolicy().hasHeightForWidth())
        self.frmProgress.setSizePolicy(sizePolicy2)
        self.frmProgress.setFrameShape(QFrame.Shape.NoFrame)
        self.frmProgress.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frmProgress)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.lblProgress = QLabel(self.frmProgress)
        self.lblProgress.setObjectName(u"lblProgress")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblProgress)

        self.layProgress = QHBoxLayout()
        self.layProgress.setObjectName(u"layProgress")
        self.prbProgress = QProgressBar(self.frmProgress)
        self.prbProgress.setObjectName(u"prbProgress")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(5)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.prbProgress.sizePolicy().hasHeightForWidth())
        self.prbProgress.setSizePolicy(sizePolicy3)
        self.prbProgress.setValue(0)

        self.layProgress.addWidget(self.prbProgress)

        self.lblProgress_Status = QLabel(self.frmProgress)
        self.lblProgress_Status.setObjectName(u"lblProgress_Status")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lblProgress_Status.sizePolicy().hasHeightForWidth())
        self.lblProgress_Status.setSizePolicy(sizePolicy4)
        self.lblProgress_Status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layProgress.addWidget(self.lblProgress_Status)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layProgress)

        self.lblMessages = QLabel(self.frmProgress)
        self.lblMessages.setObjectName(u"lblMessages")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblMessages)

        self.lstMessages = QListWidget(self.frmProgress)
        self.lstMessages.setObjectName(u"lstMessages")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lstMessages.sizePolicy().hasHeightForWidth())
        self.lstMessages.setSizePolicy(sizePolicy5)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lstMessages)


        self.verticalLayout.addWidget(self.frmProgress)

        self.btnsDialog = QDialogButtonBox(ExportDialog)
        self.btnsDialog.setObjectName(u"btnsDialog")
        self.btnsDialog.setOrientation(Qt.Orientation.Horizontal)
        self.btnsDialog.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.SaveAll)
        self.btnsDialog.setCenterButtons(False)

        self.verticalLayout.addWidget(self.btnsDialog)


        self.retranslateUi(ExportDialog)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Export", None))
        self.lblOutputDirectory.setText(QCoreApplication.translate("ExportDialog", u"Output directory:", None))
        self.btnOutputDir.setText(QCoreApplication.translate("ExportDialog", u"Browse", None))
        self.lblTargetWidth.setText(QCoreApplication.translate("ExportDialog", u"Target width:", None))
        self.lblTargetWidth_Value.setText(QCoreApplication.translate("ExportDialog", u"0 px", None))
        self.lblTargetHeight_Value.setText(QCoreApplication.translate("ExportDialog", u"0 px", None))
        self.lblTargetHeight.setText(QCoreApplication.translate("ExportDialog", u"Target height:", None))
        self.lblProgress.setText(QCoreApplication.translate("ExportDialog", u"Progress:", None))
        self.lblProgress_Status.setText(QCoreApplication.translate("ExportDialog", u"Ready", None))
        self.lblMessages.setText(QCoreApplication.translate("ExportDialog", u"Messages:", None))
    # retranslateUi

