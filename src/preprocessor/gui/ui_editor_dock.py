# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor_dock.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDockWidget, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QWidget)

class Ui_EditorDock(object):
    def setupUi(self, EditorDock):
        if not EditorDock.objectName():
            EditorDock.setObjectName(u"EditorDock")
        EditorDock.resize(447, 1023)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.dockWidgetContents)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 445, 999))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.grpCropping = QGroupBox(self.scrollAreaWidgetContents)
        self.grpCropping.setObjectName(u"grpCropping")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.grpCropping.sizePolicy().hasHeightForWidth())
        self.grpCropping.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.grpCropping)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.lblCropping_QuadratAutodetect = QLabel(self.grpCropping)
        self.lblCropping_QuadratAutodetect.setObjectName(u"lblCropping_QuadratAutodetect")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblCropping_QuadratAutodetect)

        self.btnCropping_QuadratAutodetect = QPushButton(self.grpCropping)
        self.btnCropping_QuadratAutodetect.setObjectName(u"btnCropping_QuadratAutodetect")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.btnCropping_QuadratAutodetect)


        self.gridLayout_2.addWidget(self.grpCropping, 3, 0, 1, 1)

        self.grpLensCorrection = QGroupBox(self.scrollAreaWidgetContents)
        self.grpLensCorrection.setObjectName(u"grpLensCorrection")
        sizePolicy1.setHeightForWidth(self.grpLensCorrection.sizePolicy().hasHeightForWidth())
        self.grpLensCorrection.setSizePolicy(sizePolicy1)
        self.formLayout_2 = QFormLayout(self.grpLensCorrection)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.lblLensCorrection_Distortion = QLabel(self.grpLensCorrection)
        self.lblLensCorrection_Distortion.setObjectName(u"lblLensCorrection_Distortion")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblLensCorrection_Distortion)

        self.sldLensCorrection_Distortion = QSlider(self.grpLensCorrection)
        self.sldLensCorrection_Distortion.setObjectName(u"sldLensCorrection_Distortion")
        self.sldLensCorrection_Distortion.setMinimum(-100)
        self.sldLensCorrection_Distortion.setMaximum(100)
        self.sldLensCorrection_Distortion.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.sldLensCorrection_Distortion)


        self.gridLayout_2.addWidget(self.grpLensCorrection, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.grpMetadata = QGroupBox(self.scrollAreaWidgetContents)
        self.grpMetadata.setObjectName(u"grpMetadata")
        sizePolicy1.setHeightForWidth(self.grpMetadata.sizePolicy().hasHeightForWidth())
        self.grpMetadata.setSizePolicy(sizePolicy1)
        self.formLayout_3 = QFormLayout(self.grpMetadata)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.lblMetadataDate = QLabel(self.grpMetadata)
        self.lblMetadataDate.setObjectName(u"lblMetadataDate")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblMetadataDate)

        self.dteMetadataDate = QDateTimeEdit(self.grpMetadata)
        self.dteMetadataDate.setObjectName(u"dteMetadataDate")
        self.dteMetadataDate.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dteMetadataDate)

        self.lblMetadataPartner = QLabel(self.grpMetadata)
        self.lblMetadataPartner.setObjectName(u"lblMetadataPartner")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblMetadataPartner)

        self.txtMetadataPartner = QLineEdit(self.grpMetadata)
        self.txtMetadataPartner.setObjectName(u"txtMetadataPartner")
        self.txtMetadataPartner.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txtMetadataPartner)

        self.lblMetadataArea = QLabel(self.grpMetadata)
        self.lblMetadataArea.setObjectName(u"lblMetadataArea")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblMetadataArea)

        self.lblMetadataSite = QLabel(self.grpMetadata)
        self.lblMetadataSite.setObjectName(u"lblMetadataSite")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblMetadataSite)

        self.lblMetadataSeason = QLabel(self.grpMetadata)
        self.lblMetadataSeason.setObjectName(u"lblMetadataSeason")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblMetadataSeason)

        self.lblMetadataTransect = QLabel(self.grpMetadata)
        self.lblMetadataTransect.setObjectName(u"lblMetadataTransect")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblMetadataTransect)

        self.line = QFrame(self.grpMetadata)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setMinimumSize(QSize(0, 6))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.FieldRole, self.line)

        self.lblMetadataHeight = QLabel(self.grpMetadata)
        self.lblMetadataHeight.setObjectName(u"lblMetadataHeight")

        self.formLayout_3.setWidget(7, QFormLayout.ItemRole.LabelRole, self.lblMetadataHeight)

        self.lblMetadataLatitude = QLabel(self.grpMetadata)
        self.lblMetadataLatitude.setObjectName(u"lblMetadataLatitude")

        self.formLayout_3.setWidget(8, QFormLayout.ItemRole.LabelRole, self.lblMetadataLatitude)

        self.lblMetadataLongitude = QLabel(self.grpMetadata)
        self.lblMetadataLongitude.setObjectName(u"lblMetadataLongitude")

        self.formLayout_3.setWidget(9, QFormLayout.ItemRole.LabelRole, self.lblMetadataLongitude)

        self.lblMetadataDepth = QLabel(self.grpMetadata)
        self.lblMetadataDepth.setObjectName(u"lblMetadataDepth")

        self.formLayout_3.setWidget(10, QFormLayout.ItemRole.LabelRole, self.lblMetadataDepth)

        self.lblMetadataCamera = QLabel(self.grpMetadata)
        self.lblMetadataCamera.setObjectName(u"lblMetadataCamera")

        self.formLayout_3.setWidget(11, QFormLayout.ItemRole.LabelRole, self.lblMetadataCamera)

        self.lblMetadataPhotographer = QLabel(self.grpMetadata)
        self.lblMetadataPhotographer.setObjectName(u"lblMetadataPhotographer")

        self.formLayout_3.setWidget(12, QFormLayout.ItemRole.LabelRole, self.lblMetadataPhotographer)

        self.lblMetadataWaterQuality = QLabel(self.grpMetadata)
        self.lblMetadataWaterQuality.setObjectName(u"lblMetadataWaterQuality")

        self.formLayout_3.setWidget(13, QFormLayout.ItemRole.LabelRole, self.lblMetadataWaterQuality)

        self.lblMetadataStrobes = QLabel(self.grpMetadata)
        self.lblMetadataStrobes.setObjectName(u"lblMetadataStrobes")

        self.formLayout_3.setWidget(14, QFormLayout.ItemRole.LabelRole, self.lblMetadataStrobes)

        self.lblMetadataFraming = QLabel(self.grpMetadata)
        self.lblMetadataFraming.setObjectName(u"lblMetadataFraming")

        self.formLayout_3.setWidget(15, QFormLayout.ItemRole.LabelRole, self.lblMetadataFraming)

        self.lblMetadataWhiteBalanceCard = QLabel(self.grpMetadata)
        self.lblMetadataWhiteBalanceCard.setObjectName(u"lblMetadataWhiteBalanceCard")

        self.formLayout_3.setWidget(16, QFormLayout.ItemRole.LabelRole, self.lblMetadataWhiteBalanceCard)

        self.lblMetadataComments = QLabel(self.grpMetadata)
        self.lblMetadataComments.setObjectName(u"lblMetadataComments")

        self.formLayout_3.setWidget(17, QFormLayout.ItemRole.LabelRole, self.lblMetadataComments)

        self.btnMetadataEdit = QPushButton(self.grpMetadata)
        self.btnMetadataEdit.setObjectName(u"btnMetadataEdit")

        self.formLayout_3.setWidget(18, QFormLayout.ItemRole.FieldRole, self.btnMetadataEdit)

        self.txtMetadataArea = QLineEdit(self.grpMetadata)
        self.txtMetadataArea.setObjectName(u"txtMetadataArea")
        self.txtMetadataArea.setReadOnly(True)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtMetadataArea)

        self.txtMetadataSite = QLineEdit(self.grpMetadata)
        self.txtMetadataSite.setObjectName(u"txtMetadataSite")
        self.txtMetadataSite.setReadOnly(True)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.txtMetadataSite)

        self.txtMetadataSeason = QLineEdit(self.grpMetadata)
        self.txtMetadataSeason.setObjectName(u"txtMetadataSeason")
        self.txtMetadataSeason.setReadOnly(True)

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.txtMetadataSeason)

        self.txtMetadataTransect = QLineEdit(self.grpMetadata)
        self.txtMetadataTransect.setObjectName(u"txtMetadataTransect")
        self.txtMetadataTransect.setReadOnly(True)

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.FieldRole, self.txtMetadataTransect)

        self.txtMetadataHeight = QLineEdit(self.grpMetadata)
        self.txtMetadataHeight.setObjectName(u"txtMetadataHeight")
        self.txtMetadataHeight.setReadOnly(True)

        self.formLayout_3.setWidget(7, QFormLayout.ItemRole.FieldRole, self.txtMetadataHeight)

        self.txtMetadataLatitude = QLineEdit(self.grpMetadata)
        self.txtMetadataLatitude.setObjectName(u"txtMetadataLatitude")
        self.txtMetadataLatitude.setReadOnly(True)

        self.formLayout_3.setWidget(8, QFormLayout.ItemRole.FieldRole, self.txtMetadataLatitude)

        self.txtMetadataLongitude = QLineEdit(self.grpMetadata)
        self.txtMetadataLongitude.setObjectName(u"txtMetadataLongitude")
        self.txtMetadataLongitude.setReadOnly(True)

        self.formLayout_3.setWidget(9, QFormLayout.ItemRole.FieldRole, self.txtMetadataLongitude)

        self.txtMetadataDepth = QLineEdit(self.grpMetadata)
        self.txtMetadataDepth.setObjectName(u"txtMetadataDepth")
        self.txtMetadataDepth.setReadOnly(True)

        self.formLayout_3.setWidget(10, QFormLayout.ItemRole.FieldRole, self.txtMetadataDepth)

        self.txtMetadataCamera = QLineEdit(self.grpMetadata)
        self.txtMetadataCamera.setObjectName(u"txtMetadataCamera")
        self.txtMetadataCamera.setReadOnly(True)

        self.formLayout_3.setWidget(11, QFormLayout.ItemRole.FieldRole, self.txtMetadataCamera)

        self.txtMetadataPhotographer = QLineEdit(self.grpMetadata)
        self.txtMetadataPhotographer.setObjectName(u"txtMetadataPhotographer")
        self.txtMetadataPhotographer.setReadOnly(True)

        self.formLayout_3.setWidget(12, QFormLayout.ItemRole.FieldRole, self.txtMetadataPhotographer)

        self.txtMetadataWaterQuality = QLineEdit(self.grpMetadata)
        self.txtMetadataWaterQuality.setObjectName(u"txtMetadataWaterQuality")
        self.txtMetadataWaterQuality.setReadOnly(True)

        self.formLayout_3.setWidget(13, QFormLayout.ItemRole.FieldRole, self.txtMetadataWaterQuality)

        self.txtMetadataStrobes = QLineEdit(self.grpMetadata)
        self.txtMetadataStrobes.setObjectName(u"txtMetadataStrobes")
        self.txtMetadataStrobes.setReadOnly(True)

        self.formLayout_3.setWidget(14, QFormLayout.ItemRole.FieldRole, self.txtMetadataStrobes)

        self.txtMetadataFraming = QLineEdit(self.grpMetadata)
        self.txtMetadataFraming.setObjectName(u"txtMetadataFraming")
        self.txtMetadataFraming.setReadOnly(True)

        self.formLayout_3.setWidget(15, QFormLayout.ItemRole.FieldRole, self.txtMetadataFraming)

        self.txtMetadataWhiteBalanceCard = QLineEdit(self.grpMetadata)
        self.txtMetadataWhiteBalanceCard.setObjectName(u"txtMetadataWhiteBalanceCard")
        self.txtMetadataWhiteBalanceCard.setReadOnly(True)

        self.formLayout_3.setWidget(16, QFormLayout.ItemRole.FieldRole, self.txtMetadataWhiteBalanceCard)

        self.txtComments = QPlainTextEdit(self.grpMetadata)
        self.txtComments.setObjectName(u"txtComments")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.txtComments.sizePolicy().hasHeightForWidth())
        self.txtComments.setSizePolicy(sizePolicy3)
        self.txtComments.setMaximumSize(QSize(16777215, 100))
        self.txtComments.setReadOnly(True)

        self.formLayout_3.setWidget(17, QFormLayout.ItemRole.FieldRole, self.txtComments)


        self.gridLayout_2.addWidget(self.grpMetadata, 4, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        EditorDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(EditorDock)

        QMetaObject.connectSlotsByName(EditorDock)
    # setupUi

    def retranslateUi(self, EditorDock):
        EditorDock.setWindowTitle(QCoreApplication.translate("EditorDock", u"Edit", None))
        self.grpCropping.setTitle(QCoreApplication.translate("EditorDock", u"Cropping", None))
        self.lblCropping_QuadratAutodetect.setText(QCoreApplication.translate("EditorDock", u"Quadrat:", None))
        self.btnCropping_QuadratAutodetect.setText(QCoreApplication.translate("EditorDock", u"Autodetect", None))
        self.grpLensCorrection.setTitle(QCoreApplication.translate("EditorDock", u"Lens correction", None))
        self.lblLensCorrection_Distortion.setText(QCoreApplication.translate("EditorDock", u"Distortion:", None))
        self.grpMetadata.setTitle(QCoreApplication.translate("EditorDock", u"Metadata", None))
        self.lblMetadataDate.setText(QCoreApplication.translate("EditorDock", u"Date:", None))
        self.lblMetadataPartner.setText(QCoreApplication.translate("EditorDock", u"Partner:", None))
        self.lblMetadataArea.setText(QCoreApplication.translate("EditorDock", u"Area:", None))
        self.lblMetadataSite.setText(QCoreApplication.translate("EditorDock", u"Site:", None))
        self.lblMetadataSeason.setText(QCoreApplication.translate("EditorDock", u"Season:", None))
        self.lblMetadataTransect.setText(QCoreApplication.translate("EditorDock", u"Transect:", None))
        self.lblMetadataHeight.setText(QCoreApplication.translate("EditorDock", u"Height:", None))
        self.lblMetadataLatitude.setText(QCoreApplication.translate("EditorDock", u"Latitude:", None))
        self.lblMetadataLongitude.setText(QCoreApplication.translate("EditorDock", u"Longitude:", None))
        self.lblMetadataDepth.setText(QCoreApplication.translate("EditorDock", u"Depth:", None))
        self.lblMetadataCamera.setText(QCoreApplication.translate("EditorDock", u"Camera:", None))
        self.lblMetadataPhotographer.setText(QCoreApplication.translate("EditorDock", u"Photographer:", None))
        self.lblMetadataWaterQuality.setText(QCoreApplication.translate("EditorDock", u"Water quality:", None))
        self.lblMetadataStrobes.setText(QCoreApplication.translate("EditorDock", u"Strobes:", None))
        self.lblMetadataFraming.setText(QCoreApplication.translate("EditorDock", u"Framing:", None))
        self.lblMetadataWhiteBalanceCard.setText(QCoreApplication.translate("EditorDock", u"White balance card:", None))
        self.lblMetadataComments.setText(QCoreApplication.translate("EditorDock", u"Comments:", None))
        self.btnMetadataEdit.setText(QCoreApplication.translate("EditorDock", u"Edit Metadata...", None))
    # retranslateUi

