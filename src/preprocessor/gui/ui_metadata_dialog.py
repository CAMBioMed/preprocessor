# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'metadata_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateTimeEdit, QDialog,
    QDoubleSpinBox, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MetadataDialog(object):
    def setupUi(self, MetadataDialog):
        if not MetadataDialog.objectName():
            MetadataDialog.setObjectName(u"MetadataDialog")
        MetadataDialog.resize(773, 860)
        self.verticalLayout = QVBoxLayout(MetadataDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layMain = QHBoxLayout()
        self.layMain.setObjectName(u"layMain")
        self.scrollArea = QScrollArea(MetadataDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 633, 832))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblSelection = QLabel(self.scrollAreaWidgetContents)
        self.lblSelection.setObjectName(u"lblSelection")
        sizePolicy1.setHeightForWidth(self.lblSelection.sizePolicy().hasHeightForWidth())
        self.lblSelection.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.lblSelection)

        self.btnCopyFromCurrentPhoto = QPushButton(self.scrollAreaWidgetContents)
        self.btnCopyFromCurrentPhoto.setObjectName(u"btnCopyFromCurrentPhoto")

        self.horizontalLayout.addWidget(self.btnCopyFromCurrentPhoto)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.lblDate = QLabel(self.scrollAreaWidgetContents)
        self.lblDate.setObjectName(u"lblDate")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblDate)

        self.lay01Date = QHBoxLayout()
        self.lay01Date.setObjectName(u"lay01Date")
        self.chkDate = QCheckBox(self.scrollAreaWidgetContents)
        self.chkDate.setObjectName(u"chkDate")

        self.lay01Date.addWidget(self.chkDate)

        self.dteDate = QDateTimeEdit(self.scrollAreaWidgetContents)
        self.dteDate.setObjectName(u"dteDate")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dteDate.sizePolicy().hasHeightForWidth())
        self.dteDate.setSizePolicy(sizePolicy2)
        self.dteDate.setCalendarPopup(True)

        self.lay01Date.addWidget(self.dteDate)

        self.dteDateCommonValue = QDateTimeEdit(self.scrollAreaWidgetContents)
        self.dteDateCommonValue.setObjectName(u"dteDateCommonValue")
        self.dteDateCommonValue.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.dteDateCommonValue.sizePolicy().hasHeightForWidth())
        self.dteDateCommonValue.setSizePolicy(sizePolicy2)
        self.dteDateCommonValue.setCalendarPopup(True)

        self.lay01Date.addWidget(self.dteDateCommonValue)

        self.txtDateVarious = QLineEdit(self.scrollAreaWidgetContents)
        self.txtDateVarious.setObjectName(u"txtDateVarious")
        self.txtDateVarious.setEnabled(True)
        self.txtDateVarious.setReadOnly(True)

        self.lay01Date.addWidget(self.txtDateVarious)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.lay01Date)

        self.lblPartner = QLabel(self.scrollAreaWidgetContents)
        self.lblPartner.setObjectName(u"lblPartner")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblPartner)

        self.lay02Partner = QHBoxLayout()
        self.lay02Partner.setObjectName(u"lay02Partner")
        self.chkPartner = QCheckBox(self.scrollAreaWidgetContents)
        self.chkPartner.setObjectName(u"chkPartner")

        self.lay02Partner.addWidget(self.chkPartner)

        self.txtPartner = QLineEdit(self.scrollAreaWidgetContents)
        self.txtPartner.setObjectName(u"txtPartner")

        self.lay02Partner.addWidget(self.txtPartner)

        self.txtPartnerCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtPartnerCommonValue.setObjectName(u"txtPartnerCommonValue")
        self.txtPartnerCommonValue.setReadOnly(True)

        self.lay02Partner.addWidget(self.txtPartnerCommonValue)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.lay02Partner)

        self.lblArea = QLabel(self.scrollAreaWidgetContents)
        self.lblArea.setObjectName(u"lblArea")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblArea)

        self.lay03Area = QHBoxLayout()
        self.lay03Area.setObjectName(u"lay03Area")
        self.chkArea = QCheckBox(self.scrollAreaWidgetContents)
        self.chkArea.setObjectName(u"chkArea")

        self.lay03Area.addWidget(self.chkArea)

        self.txtArea = QLineEdit(self.scrollAreaWidgetContents)
        self.txtArea.setObjectName(u"txtArea")

        self.lay03Area.addWidget(self.txtArea)

        self.txtAreaCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtAreaCommonValue.setObjectName(u"txtAreaCommonValue")
        self.txtAreaCommonValue.setReadOnly(True)

        self.lay03Area.addWidget(self.txtAreaCommonValue)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.lay03Area)

        self.lblSite = QLabel(self.scrollAreaWidgetContents)
        self.lblSite.setObjectName(u"lblSite")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblSite)

        self.lay04Site = QHBoxLayout()
        self.lay04Site.setObjectName(u"lay04Site")
        self.chkSite = QCheckBox(self.scrollAreaWidgetContents)
        self.chkSite.setObjectName(u"chkSite")

        self.lay04Site.addWidget(self.chkSite)

        self.txtSite = QLineEdit(self.scrollAreaWidgetContents)
        self.txtSite.setObjectName(u"txtSite")

        self.lay04Site.addWidget(self.txtSite)

        self.txtSiteCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtSiteCommonValue.setObjectName(u"txtSiteCommonValue")
        self.txtSiteCommonValue.setReadOnly(True)

        self.lay04Site.addWidget(self.txtSiteCommonValue)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.lay04Site)

        self.lblSeason = QLabel(self.scrollAreaWidgetContents)
        self.lblSeason.setObjectName(u"lblSeason")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblSeason)

        self.lay05Season = QHBoxLayout()
        self.lay05Season.setObjectName(u"lay05Season")
        self.chkSeason = QCheckBox(self.scrollAreaWidgetContents)
        self.chkSeason.setObjectName(u"chkSeason")

        self.lay05Season.addWidget(self.chkSeason)

        self.txtSeason = QLineEdit(self.scrollAreaWidgetContents)
        self.txtSeason.setObjectName(u"txtSeason")

        self.lay05Season.addWidget(self.txtSeason)

        self.txtSeasonCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtSeasonCommonValue.setObjectName(u"txtSeasonCommonValue")
        self.txtSeasonCommonValue.setReadOnly(True)

        self.lay05Season.addWidget(self.txtSeasonCommonValue)


        self.formLayout.setLayout(5, QFormLayout.ItemRole.FieldRole, self.lay05Season)

        self.lblTransect = QLabel(self.scrollAreaWidgetContents)
        self.lblTransect.setObjectName(u"lblTransect")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lblTransect)

        self.lay06Transect = QHBoxLayout()
        self.lay06Transect.setObjectName(u"lay06Transect")
        self.chkTransect = QCheckBox(self.scrollAreaWidgetContents)
        self.chkTransect.setObjectName(u"chkTransect")

        self.lay06Transect.addWidget(self.chkTransect)

        self.txtTransect = QLineEdit(self.scrollAreaWidgetContents)
        self.txtTransect.setObjectName(u"txtTransect")

        self.lay06Transect.addWidget(self.txtTransect)

        self.txtTransectCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtTransectCommonValue.setObjectName(u"txtTransectCommonValue")
        self.txtTransectCommonValue.setReadOnly(True)

        self.lay06Transect.addWidget(self.txtTransectCommonValue)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.FieldRole, self.lay06Transect)

        self.lay07Height = QHBoxLayout()
        self.lay07Height.setObjectName(u"lay07Height")
        self.chkHeight = QCheckBox(self.scrollAreaWidgetContents)
        self.chkHeight.setObjectName(u"chkHeight")

        self.lay07Height.addWidget(self.chkHeight)

        self.txtHeight = QLineEdit(self.scrollAreaWidgetContents)
        self.txtHeight.setObjectName(u"txtHeight")

        self.lay07Height.addWidget(self.txtHeight)

        self.txtHeightCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtHeightCommonValue.setObjectName(u"txtHeightCommonValue")
        self.txtHeightCommonValue.setReadOnly(True)

        self.lay07Height.addWidget(self.txtHeightCommonValue)


        self.formLayout.setLayout(8, QFormLayout.ItemRole.FieldRole, self.lay07Height)

        self.lblLatitude = QLabel(self.scrollAreaWidgetContents)
        self.lblLatitude.setObjectName(u"lblLatitude")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.lblLatitude)

        self.lay08Latitude = QHBoxLayout()
        self.lay08Latitude.setObjectName(u"lay08Latitude")
        self.chkLatitude = QCheckBox(self.scrollAreaWidgetContents)
        self.chkLatitude.setObjectName(u"chkLatitude")

        self.lay08Latitude.addWidget(self.chkLatitude)

        self.numLatitude = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.numLatitude.setObjectName(u"numLatitude")
        sizePolicy2.setHeightForWidth(self.numLatitude.sizePolicy().hasHeightForWidth())
        self.numLatitude.setSizePolicy(sizePolicy2)
        self.numLatitude.setDecimals(6)
        self.numLatitude.setMinimum(-90.000000000000000)
        self.numLatitude.setMaximum(90.000000000000000)

        self.lay08Latitude.addWidget(self.numLatitude)

        self.numLatitudeCommonValue = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.numLatitudeCommonValue.setObjectName(u"numLatitudeCommonValue")
        sizePolicy2.setHeightForWidth(self.numLatitudeCommonValue.sizePolicy().hasHeightForWidth())
        self.numLatitudeCommonValue.setSizePolicy(sizePolicy2)
        self.numLatitudeCommonValue.setReadOnly(True)
        self.numLatitudeCommonValue.setDecimals(6)
        self.numLatitudeCommonValue.setMinimum(-90.000000000000000)
        self.numLatitudeCommonValue.setMaximum(90.000000000000000)

        self.lay08Latitude.addWidget(self.numLatitudeCommonValue)

        self.txtLatitudeVarious = QLineEdit(self.scrollAreaWidgetContents)
        self.txtLatitudeVarious.setObjectName(u"txtLatitudeVarious")
        self.txtLatitudeVarious.setEnabled(True)
        self.txtLatitudeVarious.setReadOnly(True)

        self.lay08Latitude.addWidget(self.txtLatitudeVarious)


        self.formLayout.setLayout(9, QFormLayout.ItemRole.FieldRole, self.lay08Latitude)

        self.lblLongitude = QLabel(self.scrollAreaWidgetContents)
        self.lblLongitude.setObjectName(u"lblLongitude")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.lblLongitude)

        self.lay09Longitude = QHBoxLayout()
        self.lay09Longitude.setObjectName(u"lay09Longitude")
        self.chkLongitude = QCheckBox(self.scrollAreaWidgetContents)
        self.chkLongitude.setObjectName(u"chkLongitude")

        self.lay09Longitude.addWidget(self.chkLongitude)

        self.numLongitude = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.numLongitude.setObjectName(u"numLongitude")
        sizePolicy2.setHeightForWidth(self.numLongitude.sizePolicy().hasHeightForWidth())
        self.numLongitude.setSizePolicy(sizePolicy2)
        self.numLongitude.setDecimals(6)
        self.numLongitude.setMinimum(-180.000000000000000)
        self.numLongitude.setMaximum(180.000000000000000)

        self.lay09Longitude.addWidget(self.numLongitude)

        self.numLongitudeCommonValue = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.numLongitudeCommonValue.setObjectName(u"numLongitudeCommonValue")
        sizePolicy2.setHeightForWidth(self.numLongitudeCommonValue.sizePolicy().hasHeightForWidth())
        self.numLongitudeCommonValue.setSizePolicy(sizePolicy2)
        self.numLongitudeCommonValue.setReadOnly(True)
        self.numLongitudeCommonValue.setDecimals(6)
        self.numLongitudeCommonValue.setMinimum(-180.000000000000000)
        self.numLongitudeCommonValue.setMaximum(180.000000000000000)

        self.lay09Longitude.addWidget(self.numLongitudeCommonValue)

        self.txtLongitudeVarious = QLineEdit(self.scrollAreaWidgetContents)
        self.txtLongitudeVarious.setObjectName(u"txtLongitudeVarious")
        self.txtLongitudeVarious.setEnabled(True)
        self.txtLongitudeVarious.setReadOnly(True)

        self.lay09Longitude.addWidget(self.txtLongitudeVarious)


        self.formLayout.setLayout(10, QFormLayout.ItemRole.FieldRole, self.lay09Longitude)

        self.lblDepth = QLabel(self.scrollAreaWidgetContents)
        self.lblDepth.setObjectName(u"lblDepth")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.lblDepth)

        self.lay10Depth = QHBoxLayout()
        self.lay10Depth.setObjectName(u"lay10Depth")
        self.chkDepth = QCheckBox(self.scrollAreaWidgetContents)
        self.chkDepth.setObjectName(u"chkDepth")

        self.lay10Depth.addWidget(self.chkDepth)

        self.txtDepth = QLineEdit(self.scrollAreaWidgetContents)
        self.txtDepth.setObjectName(u"txtDepth")

        self.lay10Depth.addWidget(self.txtDepth)

        self.txtDepthCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtDepthCommonValue.setObjectName(u"txtDepthCommonValue")
        self.txtDepthCommonValue.setEnabled(True)
        self.txtDepthCommonValue.setReadOnly(True)

        self.lay10Depth.addWidget(self.txtDepthCommonValue)


        self.formLayout.setLayout(11, QFormLayout.ItemRole.FieldRole, self.lay10Depth)

        self.lblCamera = QLabel(self.scrollAreaWidgetContents)
        self.lblCamera.setObjectName(u"lblCamera")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.lblCamera)

        self.lay11Camera = QHBoxLayout()
        self.lay11Camera.setObjectName(u"lay11Camera")
        self.chkCamera = QCheckBox(self.scrollAreaWidgetContents)
        self.chkCamera.setObjectName(u"chkCamera")

        self.lay11Camera.addWidget(self.chkCamera)

        self.txtCamera = QLineEdit(self.scrollAreaWidgetContents)
        self.txtCamera.setObjectName(u"txtCamera")

        self.lay11Camera.addWidget(self.txtCamera)

        self.txtCameraCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtCameraCommonValue.setObjectName(u"txtCameraCommonValue")
        self.txtCameraCommonValue.setEnabled(True)
        self.txtCameraCommonValue.setReadOnly(True)

        self.lay11Camera.addWidget(self.txtCameraCommonValue)


        self.formLayout.setLayout(12, QFormLayout.ItemRole.FieldRole, self.lay11Camera)

        self.lblPhotographer = QLabel(self.scrollAreaWidgetContents)
        self.lblPhotographer.setObjectName(u"lblPhotographer")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.lblPhotographer)

        self.lay12Photographer = QHBoxLayout()
        self.lay12Photographer.setObjectName(u"lay12Photographer")
        self.chkPhotographer = QCheckBox(self.scrollAreaWidgetContents)
        self.chkPhotographer.setObjectName(u"chkPhotographer")

        self.lay12Photographer.addWidget(self.chkPhotographer)

        self.txtPhotographer = QLineEdit(self.scrollAreaWidgetContents)
        self.txtPhotographer.setObjectName(u"txtPhotographer")

        self.lay12Photographer.addWidget(self.txtPhotographer)

        self.txtPhotographerCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtPhotographerCommonValue.setObjectName(u"txtPhotographerCommonValue")
        self.txtPhotographerCommonValue.setEnabled(True)
        self.txtPhotographerCommonValue.setReadOnly(True)

        self.lay12Photographer.addWidget(self.txtPhotographerCommonValue)


        self.formLayout.setLayout(13, QFormLayout.ItemRole.FieldRole, self.lay12Photographer)

        self.lblWaterQuality = QLabel(self.scrollAreaWidgetContents)
        self.lblWaterQuality.setObjectName(u"lblWaterQuality")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.lblWaterQuality)

        self.lay13WaterQuality = QHBoxLayout()
        self.lay13WaterQuality.setObjectName(u"lay13WaterQuality")
        self.chkWaterQuality = QCheckBox(self.scrollAreaWidgetContents)
        self.chkWaterQuality.setObjectName(u"chkWaterQuality")

        self.lay13WaterQuality.addWidget(self.chkWaterQuality)

        self.txtWaterQuality = QLineEdit(self.scrollAreaWidgetContents)
        self.txtWaterQuality.setObjectName(u"txtWaterQuality")

        self.lay13WaterQuality.addWidget(self.txtWaterQuality)

        self.txtWaterQualityCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtWaterQualityCommonValue.setObjectName(u"txtWaterQualityCommonValue")
        self.txtWaterQualityCommonValue.setEnabled(True)
        self.txtWaterQualityCommonValue.setReadOnly(True)

        self.lay13WaterQuality.addWidget(self.txtWaterQualityCommonValue)


        self.formLayout.setLayout(14, QFormLayout.ItemRole.FieldRole, self.lay13WaterQuality)

        self.lblStrobes = QLabel(self.scrollAreaWidgetContents)
        self.lblStrobes.setObjectName(u"lblStrobes")

        self.formLayout.setWidget(15, QFormLayout.ItemRole.LabelRole, self.lblStrobes)

        self.lay14Strobes = QHBoxLayout()
        self.lay14Strobes.setObjectName(u"lay14Strobes")
        self.chkStrobes = QCheckBox(self.scrollAreaWidgetContents)
        self.chkStrobes.setObjectName(u"chkStrobes")

        self.lay14Strobes.addWidget(self.chkStrobes)

        self.txtStrobes = QLineEdit(self.scrollAreaWidgetContents)
        self.txtStrobes.setObjectName(u"txtStrobes")

        self.lay14Strobes.addWidget(self.txtStrobes)

        self.txtStrobesCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtStrobesCommonValue.setObjectName(u"txtStrobesCommonValue")
        self.txtStrobesCommonValue.setEnabled(True)
        self.txtStrobesCommonValue.setReadOnly(True)

        self.lay14Strobes.addWidget(self.txtStrobesCommonValue)


        self.formLayout.setLayout(15, QFormLayout.ItemRole.FieldRole, self.lay14Strobes)

        self.lblFraming = QLabel(self.scrollAreaWidgetContents)
        self.lblFraming.setObjectName(u"lblFraming")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.LabelRole, self.lblFraming)

        self.lay15Framing = QHBoxLayout()
        self.lay15Framing.setObjectName(u"lay15Framing")
        self.chkFraming = QCheckBox(self.scrollAreaWidgetContents)
        self.chkFraming.setObjectName(u"chkFraming")

        self.lay15Framing.addWidget(self.chkFraming)

        self.txtFraming = QLineEdit(self.scrollAreaWidgetContents)
        self.txtFraming.setObjectName(u"txtFraming")

        self.lay15Framing.addWidget(self.txtFraming)

        self.txtFramingCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtFramingCommonValue.setObjectName(u"txtFramingCommonValue")
        self.txtFramingCommonValue.setEnabled(True)
        self.txtFramingCommonValue.setReadOnly(True)

        self.lay15Framing.addWidget(self.txtFramingCommonValue)


        self.formLayout.setLayout(16, QFormLayout.ItemRole.FieldRole, self.lay15Framing)

        self.lblWhiteBalanceCard = QLabel(self.scrollAreaWidgetContents)
        self.lblWhiteBalanceCard.setObjectName(u"lblWhiteBalanceCard")

        self.formLayout.setWidget(17, QFormLayout.ItemRole.LabelRole, self.lblWhiteBalanceCard)

        self.lay16WhiteBalanceCard = QHBoxLayout()
        self.lay16WhiteBalanceCard.setObjectName(u"lay16WhiteBalanceCard")
        self.chkWhiteBalanceCard = QCheckBox(self.scrollAreaWidgetContents)
        self.chkWhiteBalanceCard.setObjectName(u"chkWhiteBalanceCard")

        self.lay16WhiteBalanceCard.addWidget(self.chkWhiteBalanceCard)

        self.txtWhiteBalanceCard = QLineEdit(self.scrollAreaWidgetContents)
        self.txtWhiteBalanceCard.setObjectName(u"txtWhiteBalanceCard")

        self.lay16WhiteBalanceCard.addWidget(self.txtWhiteBalanceCard)

        self.txtWhiteBalanceCardCommonValue = QLineEdit(self.scrollAreaWidgetContents)
        self.txtWhiteBalanceCardCommonValue.setObjectName(u"txtWhiteBalanceCardCommonValue")
        self.txtWhiteBalanceCardCommonValue.setEnabled(True)
        self.txtWhiteBalanceCardCommonValue.setReadOnly(True)

        self.lay16WhiteBalanceCard.addWidget(self.txtWhiteBalanceCardCommonValue)


        self.formLayout.setLayout(17, QFormLayout.ItemRole.FieldRole, self.lay16WhiteBalanceCard)

        self.lblComments = QLabel(self.scrollAreaWidgetContents)
        self.lblComments.setObjectName(u"lblComments")

        self.formLayout.setWidget(18, QFormLayout.ItemRole.LabelRole, self.lblComments)

        self.lay17Comments = QHBoxLayout()
        self.lay17Comments.setObjectName(u"lay17Comments")
        self.chkComments = QCheckBox(self.scrollAreaWidgetContents)
        self.chkComments.setObjectName(u"chkComments")

        self.lay17Comments.addWidget(self.chkComments)

        self.txtComments = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.txtComments.setObjectName(u"txtComments")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.txtComments.sizePolicy().hasHeightForWidth())
        self.txtComments.setSizePolicy(sizePolicy3)

        self.lay17Comments.addWidget(self.txtComments)

        self.txtCommentsCommonValue = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.txtCommentsCommonValue.setObjectName(u"txtCommentsCommonValue")
        self.txtCommentsCommonValue.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtCommentsCommonValue.sizePolicy().hasHeightForWidth())
        self.txtCommentsCommonValue.setSizePolicy(sizePolicy3)
        self.txtCommentsCommonValue.setReadOnly(True)

        self.lay17Comments.addWidget(self.txtCommentsCommonValue)


        self.formLayout.setLayout(18, QFormLayout.ItemRole.FieldRole, self.lay17Comments)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy4)
        self.line.setMinimumSize(QSize(0, 6))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.line)

        self.lblHeight = QLabel(self.scrollAreaWidgetContents)
        self.lblHeight.setObjectName(u"lblHeight")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.lblHeight)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layMain.addWidget(self.scrollArea)

        self.layButtons = QVBoxLayout()
        self.layButtons.setObjectName(u"layButtons")
        self.btnApply = QPushButton(MetadataDialog)
        self.btnApply.setObjectName(u"btnApply")
        self.btnApply.setMinimumSize(QSize(100, 0))

        self.layButtons.addWidget(self.btnApply)

        self.btnCancel = QPushButton(MetadataDialog)
        self.btnCancel.setObjectName(u"btnCancel")

        self.layButtons.addWidget(self.btnCancel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layButtons.addItem(self.verticalSpacer)


        self.layMain.addLayout(self.layButtons)


        self.verticalLayout.addLayout(self.layMain)


        self.retranslateUi(MetadataDialog)

        self.btnApply.setDefault(True)


        QMetaObject.connectSlotsByName(MetadataDialog)
    # setupUi

    def retranslateUi(self, MetadataDialog):
        MetadataDialog.setWindowTitle(QCoreApplication.translate("MetadataDialog", u"Set Metadata", None))
        self.lblSelection.setText(QCoreApplication.translate("MetadataDialog", u"0/0 photos selected", None))
        self.btnCopyFromCurrentPhoto.setText(QCoreApplication.translate("MetadataDialog", u"Copy from current photo", None))
        self.lblDate.setText(QCoreApplication.translate("MetadataDialog", u"Date:", None))
        self.chkDate.setText("")
        self.dteDate.setDisplayFormat(QCoreApplication.translate("MetadataDialog", u"yyyy-MM-dd HH:mm", None))
        self.dteDateCommonValue.setDisplayFormat(QCoreApplication.translate("MetadataDialog", u"yyyy-MM-dd HH:mm", None))
        self.txtDateVarious.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblPartner.setText(QCoreApplication.translate("MetadataDialog", u"Partner:", None))
        self.chkPartner.setText("")
        self.txtPartnerCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblArea.setText(QCoreApplication.translate("MetadataDialog", u"Area:", None))
        self.chkArea.setText("")
        self.txtAreaCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblSite.setText(QCoreApplication.translate("MetadataDialog", u"Site:", None))
        self.chkSite.setText("")
        self.txtSiteCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblSeason.setText(QCoreApplication.translate("MetadataDialog", u"Season:", None))
        self.chkSeason.setText("")
        self.txtSeasonCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblTransect.setText(QCoreApplication.translate("MetadataDialog", u"Transect:", None))
        self.chkTransect.setText("")
        self.txtTransectCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.chkHeight.setText("")
        self.txtHeightCommonValue.setText("")
        self.txtHeightCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblLatitude.setText(QCoreApplication.translate("MetadataDialog", u"Latitude:", None))
        self.chkLatitude.setText("")
        self.txtLatitudeVarious.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblLongitude.setText(QCoreApplication.translate("MetadataDialog", u"Longitude:", None))
        self.chkLongitude.setText("")
        self.txtLongitudeVarious.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblDepth.setText(QCoreApplication.translate("MetadataDialog", u"Depth:", None))
        self.chkDepth.setText("")
        self.txtDepthCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblCamera.setText(QCoreApplication.translate("MetadataDialog", u"Camera:", None))
        self.chkCamera.setText("")
        self.txtCameraCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblPhotographer.setText(QCoreApplication.translate("MetadataDialog", u"Photographer:", None))
        self.chkPhotographer.setText("")
        self.txtPhotographerCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblWaterQuality.setText(QCoreApplication.translate("MetadataDialog", u"Water quality:", None))
        self.chkWaterQuality.setText("")
        self.txtWaterQualityCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblStrobes.setText(QCoreApplication.translate("MetadataDialog", u"Strobes:", None))
        self.chkStrobes.setText("")
        self.txtStrobesCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblFraming.setText(QCoreApplication.translate("MetadataDialog", u"Framing:", None))
        self.chkFraming.setText("")
        self.txtFramingCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblWhiteBalanceCard.setText(QCoreApplication.translate("MetadataDialog", u"White balance card:", None))
        self.chkWhiteBalanceCard.setText("")
        self.txtWhiteBalanceCardCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblComments.setText(QCoreApplication.translate("MetadataDialog", u"Comments:", None))
        self.chkComments.setText("")
        self.txtCommentsCommonValue.setPlaceholderText(QCoreApplication.translate("MetadataDialog", u"(various)", None))
        self.lblHeight.setText(QCoreApplication.translate("MetadataDialog", u"Height:", None))
        self.btnApply.setText(QCoreApplication.translate("MetadataDialog", u"Apply", None))
        self.btnCancel.setText(QCoreApplication.translate("MetadataDialog", u"Cancel", None))
    # retranslateUi

