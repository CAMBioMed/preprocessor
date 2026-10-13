# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hsv_threshold.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSlider, QSpinBox, QWidget)

class Ui_HSVThreshold(object):
    def setupUi(self, HSVThreshold):
        if not HSVThreshold.objectName():
            HSVThreshold.setObjectName(u"HSVThreshold")
        HSVThreshold.resize(400, 190)
        self.layout = QFormLayout(HSVThreshold)
        self.layout.setObjectName(u"layout")
        self.labelHueMin = QLabel(HSVThreshold)
        self.labelHueMin.setObjectName(u"labelHueMin")

        self.layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelHueMin)

        self.layoutHueMin = QHBoxLayout()
        self.layoutHueMin.setObjectName(u"layoutHueMin")
        self.sliderHueMin = QSlider(HSVThreshold)
        self.sliderHueMin.setObjectName(u"sliderHueMin")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliderHueMin.sizePolicy().hasHeightForWidth())
        self.sliderHueMin.setSizePolicy(sizePolicy)
        self.sliderHueMin.setMaximum(255)
        self.sliderHueMin.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHueMin.addWidget(self.sliderHueMin)

        self.spinboxHueMin = QSpinBox(HSVThreshold)
        self.spinboxHueMin.setObjectName(u"spinboxHueMin")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinboxHueMin.sizePolicy().hasHeightForWidth())
        self.spinboxHueMin.setSizePolicy(sizePolicy1)
        self.spinboxHueMin.setMaximum(255)

        self.layoutHueMin.addWidget(self.spinboxHueMin)


        self.layout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.layoutHueMin)

        self.labelHueMax = QLabel(HSVThreshold)
        self.labelHueMax.setObjectName(u"labelHueMax")

        self.layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelHueMax)

        self.layoutHueMax = QHBoxLayout()
        self.layoutHueMax.setObjectName(u"layoutHueMax")
        self.sliderHueMax = QSlider(HSVThreshold)
        self.sliderHueMax.setObjectName(u"sliderHueMax")
        sizePolicy.setHeightForWidth(self.sliderHueMax.sizePolicy().hasHeightForWidth())
        self.sliderHueMax.setSizePolicy(sizePolicy)
        self.sliderHueMax.setMaximum(255)
        self.sliderHueMax.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHueMax.addWidget(self.sliderHueMax)

        self.spinboxHueMax = QSpinBox(HSVThreshold)
        self.spinboxHueMax.setObjectName(u"spinboxHueMax")
        sizePolicy1.setHeightForWidth(self.spinboxHueMax.sizePolicy().hasHeightForWidth())
        self.spinboxHueMax.setSizePolicy(sizePolicy1)
        self.spinboxHueMax.setMaximum(255)

        self.layoutHueMax.addWidget(self.spinboxHueMax)


        self.layout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layoutHueMax)

        self.labelSaturationMin = QLabel(HSVThreshold)
        self.labelSaturationMin.setObjectName(u"labelSaturationMin")

        self.layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelSaturationMin)

        self.layoutSaturationMin = QHBoxLayout()
        self.layoutSaturationMin.setObjectName(u"layoutSaturationMin")
        self.sliderSaturationMin = QSlider(HSVThreshold)
        self.sliderSaturationMin.setObjectName(u"sliderSaturationMin")
        sizePolicy.setHeightForWidth(self.sliderSaturationMin.sizePolicy().hasHeightForWidth())
        self.sliderSaturationMin.setSizePolicy(sizePolicy)
        self.sliderSaturationMin.setMaximum(255)
        self.sliderSaturationMin.setOrientation(Qt.Orientation.Horizontal)

        self.layoutSaturationMin.addWidget(self.sliderSaturationMin)

        self.spinboxSaturationMin = QSpinBox(HSVThreshold)
        self.spinboxSaturationMin.setObjectName(u"spinboxSaturationMin")
        sizePolicy1.setHeightForWidth(self.spinboxSaturationMin.sizePolicy().hasHeightForWidth())
        self.spinboxSaturationMin.setSizePolicy(sizePolicy1)
        self.spinboxSaturationMin.setMaximum(255)

        self.layoutSaturationMin.addWidget(self.spinboxSaturationMin)


        self.layout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutSaturationMin)

        self.labelSaturationMax = QLabel(HSVThreshold)
        self.labelSaturationMax.setObjectName(u"labelSaturationMax")

        self.layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelSaturationMax)

        self.layoutSaturationMax = QHBoxLayout()
        self.layoutSaturationMax.setObjectName(u"layoutSaturationMax")
        self.sliderSaturationMax = QSlider(HSVThreshold)
        self.sliderSaturationMax.setObjectName(u"sliderSaturationMax")
        sizePolicy.setHeightForWidth(self.sliderSaturationMax.sizePolicy().hasHeightForWidth())
        self.sliderSaturationMax.setSizePolicy(sizePolicy)
        self.sliderSaturationMax.setMaximum(255)
        self.sliderSaturationMax.setOrientation(Qt.Orientation.Horizontal)

        self.layoutSaturationMax.addWidget(self.sliderSaturationMax)

        self.spinboxSaturationMax = QSpinBox(HSVThreshold)
        self.spinboxSaturationMax.setObjectName(u"spinboxSaturationMax")
        sizePolicy1.setHeightForWidth(self.spinboxSaturationMax.sizePolicy().hasHeightForWidth())
        self.spinboxSaturationMax.setSizePolicy(sizePolicy1)
        self.spinboxSaturationMax.setMaximum(255)

        self.layoutSaturationMax.addWidget(self.spinboxSaturationMax)


        self.layout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.layoutSaturationMax)

        self.labelValueMin = QLabel(HSVThreshold)
        self.labelValueMin.setObjectName(u"labelValueMin")

        self.layout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelValueMin)

        self.layoutValueMin = QHBoxLayout()
        self.layoutValueMin.setObjectName(u"layoutValueMin")
        self.sliderValueMin = QSlider(HSVThreshold)
        self.sliderValueMin.setObjectName(u"sliderValueMin")
        sizePolicy.setHeightForWidth(self.sliderValueMin.sizePolicy().hasHeightForWidth())
        self.sliderValueMin.setSizePolicy(sizePolicy)
        self.sliderValueMin.setMaximum(255)
        self.sliderValueMin.setOrientation(Qt.Orientation.Horizontal)

        self.layoutValueMin.addWidget(self.sliderValueMin)

        self.spinboxValueMin = QSpinBox(HSVThreshold)
        self.spinboxValueMin.setObjectName(u"spinboxValueMin")
        sizePolicy1.setHeightForWidth(self.spinboxValueMin.sizePolicy().hasHeightForWidth())
        self.spinboxValueMin.setSizePolicy(sizePolicy1)
        self.spinboxValueMin.setMaximum(255)

        self.layoutValueMin.addWidget(self.spinboxValueMin)


        self.layout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.layoutValueMin)

        self.labelValueMax = QLabel(HSVThreshold)
        self.labelValueMax.setObjectName(u"labelValueMax")

        self.layout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelValueMax)

        self.layoutValueMax = QHBoxLayout()
        self.layoutValueMax.setObjectName(u"layoutValueMax")
        self.sliderValueMax = QSlider(HSVThreshold)
        self.sliderValueMax.setObjectName(u"sliderValueMax")
        sizePolicy.setHeightForWidth(self.sliderValueMax.sizePolicy().hasHeightForWidth())
        self.sliderValueMax.setSizePolicy(sizePolicy)
        self.sliderValueMax.setMaximum(255)
        self.sliderValueMax.setOrientation(Qt.Orientation.Horizontal)

        self.layoutValueMax.addWidget(self.sliderValueMax)

        self.spinboxValueMax = QSpinBox(HSVThreshold)
        self.spinboxValueMax.setObjectName(u"spinboxValueMax")
        sizePolicy1.setHeightForWidth(self.spinboxValueMax.sizePolicy().hasHeightForWidth())
        self.spinboxValueMax.setSizePolicy(sizePolicy1)
        self.spinboxValueMax.setMaximum(255)

        self.layoutValueMax.addWidget(self.spinboxValueMax)


        self.layout.setLayout(5, QFormLayout.ItemRole.FieldRole, self.layoutValueMax)


        self.retranslateUi(HSVThreshold)

        QMetaObject.connectSlotsByName(HSVThreshold)
    # setupUi

    def retranslateUi(self, HSVThreshold):
        HSVThreshold.setWindowTitle(QCoreApplication.translate("HSVThreshold", u"Form", None))
        self.labelHueMin.setText(QCoreApplication.translate("HSVThreshold", u"Hue (min)", None))
        self.labelHueMax.setText(QCoreApplication.translate("HSVThreshold", u"Hue (max)", None))
        self.labelSaturationMin.setText(QCoreApplication.translate("HSVThreshold", u"Saturation (min)", None))
        self.labelSaturationMax.setText(QCoreApplication.translate("HSVThreshold", u"Saturation (max)", None))
        self.labelValueMin.setText(QCoreApplication.translate("HSVThreshold", u"Value (min)", None))
        self.labelValueMax.setText(QCoreApplication.translate("HSVThreshold", u"Value (max)", None))
    # retranslateUi

