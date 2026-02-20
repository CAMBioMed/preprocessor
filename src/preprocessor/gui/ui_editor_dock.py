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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFormLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QWidget)

class Ui_EditorDock(object):
    def setupUi(self, EditorDock):
        if not EditorDock.objectName():
            EditorDock.setObjectName(u"EditorDock")
        EditorDock.resize(400, 300)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 276))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.grpCropping = QGroupBox(self.scrollAreaWidgetContents)
        self.grpCropping.setObjectName(u"grpCropping")
        self.formLayout = QFormLayout(self.grpCropping)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.lblCropping_QuadratAutodetect = QLabel(self.grpCropping)
        self.lblCropping_QuadratAutodetect.setObjectName(u"lblCropping_QuadratAutodetect")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblCropping_QuadratAutodetect)

        self.btnCropping_QuadratAutodetect = QPushButton(self.grpCropping)
        self.btnCropping_QuadratAutodetect.setObjectName(u"btnCropping_QuadratAutodetect")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.btnCropping_QuadratAutodetect)


        self.gridLayout_2.addWidget(self.grpCropping, 1, 0, 1, 1)

        self.grpLensCorrection = QGroupBox(self.scrollAreaWidgetContents)
        self.grpLensCorrection.setObjectName(u"grpLensCorrection")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
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
        self.sldLensCorrection_Distortion.setMinimum(-50)
        self.sldLensCorrection_Distortion.setMaximum(50)
        self.sldLensCorrection_Distortion.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.sldLensCorrection_Distortion)


        self.gridLayout_2.addWidget(self.grpLensCorrection, 2, 0, 1, 1)

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
    # retranslateUi

