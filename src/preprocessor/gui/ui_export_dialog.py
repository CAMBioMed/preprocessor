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
    QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        ExportDialog.resize(597, 637)
        self.verticalLayout = QVBoxLayout(ExportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frmMain = QScrollArea(ExportDialog)
        self.frmMain.setObjectName(u"frmMain")
        self.frmMain.setFrameShape(QFrame.Shape.NoFrame)
        self.frmMain.setWidgetResizable(True)
        self.layMain = QWidget()
        self.layMain.setObjectName(u"layMain")
        self.layMain.setGeometry(QRect(0, 0, 573, 320))
        self.formLayout_2 = QFormLayout(self.layMain)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lblFilename = QLabel(self.layMain)
        self.lblFilename.setObjectName(u"lblFilename")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblFilename)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.txtFilename = QLineEdit(self.layMain)
        self.txtFilename.setObjectName(u"txtFilename")
        self.txtFilename.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.txtFilename)

        self.txtFilenameFormatExplanation = QPlainTextEdit(self.layMain)
        self.txtFilenameFormatExplanation.setObjectName(u"txtFilenameFormatExplanation")
        self.txtFilenameFormatExplanation.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.txtFilenameFormatExplanation)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.verticalLayout_2)

        self.lblOutputDirectory = QLabel(self.layMain)
        self.lblOutputDirectory.setObjectName(u"lblOutputDirectory")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblOutputDirectory)

        self.layOutputDir = QHBoxLayout()
        self.layOutputDir.setObjectName(u"layOutputDir")
        self.txtOutputDir = QLineEdit(self.layMain)
        self.txtOutputDir.setObjectName(u"txtOutputDir")

        self.layOutputDir.addWidget(self.txtOutputDir)

        self.btnOutputDir = QPushButton(self.layMain)
        self.btnOutputDir.setObjectName(u"btnOutputDir")

        self.layOutputDir.addWidget(self.btnOutputDir)


        self.formLayout_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layOutputDir)

        self.frmMain.setWidget(self.layMain)

        self.verticalLayout.addWidget(self.frmMain)

        self.line = QFrame(ExportDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.frmProgress = QFrame(ExportDialog)
        self.frmProgress.setObjectName(u"frmProgress")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmProgress.sizePolicy().hasHeightForWidth())
        self.frmProgress.setSizePolicy(sizePolicy)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.prbProgress.sizePolicy().hasHeightForWidth())
        self.prbProgress.setSizePolicy(sizePolicy1)
        self.prbProgress.setValue(0)

        self.layProgress.addWidget(self.prbProgress)

        self.lblProgress_Status = QLabel(self.frmProgress)
        self.lblProgress_Status.setObjectName(u"lblProgress_Status")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblProgress_Status.sizePolicy().hasHeightForWidth())
        self.lblProgress_Status.setSizePolicy(sizePolicy2)
        self.lblProgress_Status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layProgress.addWidget(self.lblProgress_Status)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layProgress)

        self.lblMessages = QLabel(self.frmProgress)
        self.lblMessages.setObjectName(u"lblMessages")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblMessages)

        self.lstMessages = QListWidget(self.frmProgress)
        self.lstMessages.setObjectName(u"lstMessages")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lstMessages.sizePolicy().hasHeightForWidth())
        self.lstMessages.setSizePolicy(sizePolicy3)

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
        self.lblFilename.setText(QCoreApplication.translate("ExportDialog", u"Filename format:", None))
        self.txtFilename.setText(QCoreApplication.translate("ExportDialog", u"{partner}_{area}_{site}_{date:%Y}_{season}_{depth}_{transect}_{date:%m%d}_{i:03d}.{ext}", None))
        self.txtFilenameFormatExplanation.setPlainText(QCoreApplication.translate("ExportDialog", u"Specify the filename format using these format specifiers:\n"
"- {i}: The one-based index of the \n"
"- {date}: The date in the form yyyy-MM-dd\n"
"- {name}: The name part of the filename.\n"
"- {ext}: The extension part of the filename (without the leading dot).\n"
"Or any of these metadata fields:\n"
"- {partner}\n"
"- {area}\n"
"- {site}\n"
"- {season}\n"
"- {transect}\n"
"- {height}\n"
"- {latitude}\n"
"- {longitude}\n"
"- {depth}\n"
"- {camera}\n"
"- {photographer}\n"
"- {water_quality}\n"
"- {strobes}\n"
"- {framing}\n"
"- {white_balance_card}\n"
"- {comments}", None))
        self.lblOutputDirectory.setText(QCoreApplication.translate("ExportDialog", u"Output directory:", None))
        self.btnOutputDir.setText(QCoreApplication.translate("ExportDialog", u"Browse", None))
        self.lblProgress.setText(QCoreApplication.translate("ExportDialog", u"Progress:", None))
        self.lblProgress_Status.setText(QCoreApplication.translate("ExportDialog", u"Ready", None))
        self.lblMessages.setText(QCoreApplication.translate("ExportDialog", u"Messages:", None))
    # retranslateUi

