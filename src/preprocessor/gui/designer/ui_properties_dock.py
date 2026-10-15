# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_dock.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDial,
    QDockWidget, QDoubleSpinBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QWidget)

class Ui_PropertiesDock(object):
    def setupUi(self, PropertiesDock):
        if not PropertiesDock.objectName():
            PropertiesDock.setObjectName(u"PropertiesDock")
        PropertiesDock.resize(494, 506)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.layoutPropertiesDock = QGridLayout(self.dockWidgetContents)
        self.layoutPropertiesDock.setObjectName(u"layoutPropertiesDock")
        self.layoutPropertiesDock.setContentsMargins(0, 0, 0, 0)
        self.scrollareaPropertiesDock = QScrollArea(self.dockWidgetContents)
        self.scrollareaPropertiesDock.setObjectName(u"scrollareaPropertiesDock")
        self.scrollareaPropertiesDock.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 477, 1415))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.layoutScrollAreaPropertiesDock = QGridLayout(self.scrollAreaWidgetContents)
        self.layoutScrollAreaPropertiesDock.setObjectName(u"layoutScrollAreaPropertiesDock")
        self.group2Threshold = QGroupBox(self.scrollAreaWidgetContents)
        self.group2Threshold.setObjectName(u"group2Threshold")
        self.formLayout = QFormLayout(self.group2Threshold)
        self.formLayout.setObjectName(u"formLayout")
        self.labelThresholdingMethod = QLabel(self.group2Threshold)
        self.labelThresholdingMethod.setObjectName(u"labelThresholdingMethod")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelThresholdingMethod)

        self.comboboxThresholdingMethod = QComboBox(self.group2Threshold)
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.setObjectName(u"comboboxThresholdingMethod")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboboxThresholdingMethod)

        self.labelThresholdingThreshold = QLabel(self.group2Threshold)
        self.labelThresholdingThreshold.setObjectName(u"labelThresholdingThreshold")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelThresholdingThreshold)

        self.labelThresholdingMaximum = QLabel(self.group2Threshold)
        self.labelThresholdingMaximum.setObjectName(u"labelThresholdingMaximum")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelThresholdingMaximum)

        self.labelThresholdingBlockSize = QLabel(self.group2Threshold)
        self.labelThresholdingBlockSize.setObjectName(u"labelThresholdingBlockSize")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelThresholdingBlockSize)

        self.labelThresholdingC = QLabel(self.group2Threshold)
        self.labelThresholdingC.setObjectName(u"labelThresholdingC")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelThresholdingC)

        self.labelThresholdingOtsu = QLabel(self.group2Threshold)
        self.labelThresholdingOtsu.setObjectName(u"labelThresholdingOtsu")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelThresholdingOtsu)

        self.checkboxThresholdingOtsu = QCheckBox(self.group2Threshold)
        self.checkboxThresholdingOtsu.setObjectName(u"checkboxThresholdingOtsu")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.checkboxThresholdingOtsu)

        self.layoutThresholdingThreshold = QHBoxLayout()
        self.layoutThresholdingThreshold.setObjectName(u"layoutThresholdingThreshold")
        self.sliderThresholdingThreshold = QSlider(self.group2Threshold)
        self.sliderThresholdingThreshold.setObjectName(u"sliderThresholdingThreshold")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sliderThresholdingThreshold.sizePolicy().hasHeightForWidth())
        self.sliderThresholdingThreshold.setSizePolicy(sizePolicy1)
        self.sliderThresholdingThreshold.setMaximum(255)
        self.sliderThresholdingThreshold.setValue(127)
        self.sliderThresholdingThreshold.setOrientation(Qt.Orientation.Horizontal)

        self.layoutThresholdingThreshold.addWidget(self.sliderThresholdingThreshold)

        self.spinboxThresholdingThreshold = QSpinBox(self.group2Threshold)
        self.spinboxThresholdingThreshold.setObjectName(u"spinboxThresholdingThreshold")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinboxThresholdingThreshold.sizePolicy().hasHeightForWidth())
        self.spinboxThresholdingThreshold.setSizePolicy(sizePolicy2)
        self.spinboxThresholdingThreshold.setMaximum(255)
        self.spinboxThresholdingThreshold.setValue(127)

        self.layoutThresholdingThreshold.addWidget(self.spinboxThresholdingThreshold)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutThresholdingThreshold)

        self.layoutThresholdingMaximum = QHBoxLayout()
        self.layoutThresholdingMaximum.setObjectName(u"layoutThresholdingMaximum")
        self.sliderThresholdingMaximum = QSlider(self.group2Threshold)
        self.sliderThresholdingMaximum.setObjectName(u"sliderThresholdingMaximum")
        sizePolicy1.setHeightForWidth(self.sliderThresholdingMaximum.sizePolicy().hasHeightForWidth())
        self.sliderThresholdingMaximum.setSizePolicy(sizePolicy1)
        self.sliderThresholdingMaximum.setMaximum(255)
        self.sliderThresholdingMaximum.setValue(255)
        self.sliderThresholdingMaximum.setOrientation(Qt.Orientation.Horizontal)

        self.layoutThresholdingMaximum.addWidget(self.sliderThresholdingMaximum)

        self.spinboxThresholdingMaximum = QSpinBox(self.group2Threshold)
        self.spinboxThresholdingMaximum.setObjectName(u"spinboxThresholdingMaximum")
        sizePolicy2.setHeightForWidth(self.spinboxThresholdingMaximum.sizePolicy().hasHeightForWidth())
        self.spinboxThresholdingMaximum.setSizePolicy(sizePolicy2)
        self.spinboxThresholdingMaximum.setMaximum(255)
        self.spinboxThresholdingMaximum.setValue(255)

        self.layoutThresholdingMaximum.addWidget(self.spinboxThresholdingMaximum)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.layoutThresholdingMaximum)

        self.sliderThresholdingBlockSize = QSlider(self.group2Threshold)
        self.sliderThresholdingBlockSize.setObjectName(u"sliderThresholdingBlockSize")
        self.sliderThresholdingBlockSize.setMinimum(1)
        self.sliderThresholdingBlockSize.setSingleStep(2)
        self.sliderThresholdingBlockSize.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.sliderThresholdingBlockSize)

        self.spinboxThresholdingC = QDoubleSpinBox(self.group2Threshold)
        self.spinboxThresholdingC.setObjectName(u"spinboxThresholdingC")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spinboxThresholdingC)

        self.labelThresholdingInverse = QLabel(self.group2Threshold)
        self.labelThresholdingInverse.setObjectName(u"labelThresholdingInverse")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelThresholdingInverse)

        self.checkboxThresholdingInverse = QCheckBox(self.group2Threshold)
        self.checkboxThresholdingInverse.setObjectName(u"checkboxThresholdingInverse")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.checkboxThresholdingInverse)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group2Threshold, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutScrollAreaPropertiesDock.addItem(self.verticalSpacer, 7, 0, 1, 1)

        self.group4FindContour = QGroupBox(self.scrollAreaWidgetContents)
        self.group4FindContour.setObjectName(u"group4FindContour")
        self.formLayout_2 = QFormLayout(self.group4FindContour)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.labelFindContourEnabled = QLabel(self.group4FindContour)
        self.labelFindContourEnabled.setObjectName(u"labelFindContourEnabled")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelFindContourEnabled)

        self.labelFindContourMethod = QLabel(self.group4FindContour)
        self.labelFindContourMethod.setObjectName(u"labelFindContourMethod")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelFindContourMethod)

        self.comboboxFindContourMethod = QComboBox(self.group4FindContour)
        self.comboboxFindContourMethod.addItem("")
        self.comboboxFindContourMethod.addItem("")
        self.comboboxFindContourMethod.addItem("")
        self.comboboxFindContourMethod.addItem("")
        self.comboboxFindContourMethod.setObjectName(u"comboboxFindContourMethod")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboboxFindContourMethod)

        self.checkboxFindContourEnabled = QCheckBox(self.group4FindContour)
        self.checkboxFindContourEnabled.setObjectName(u"checkboxFindContourEnabled")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxFindContourEnabled)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group4FindContour, 5, 0, 1, 1)

        self.groupHough = QGroupBox(self.scrollAreaWidgetContents)
        self.groupHough.setObjectName(u"groupHough")
        self.formLayout_3 = QFormLayout(self.groupHough)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.labelHoughEnabled = QLabel(self.groupHough)
        self.labelHoughEnabled.setObjectName(u"labelHoughEnabled")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelHoughEnabled)

        self.labelHoughProbabilistic = QLabel(self.groupHough)
        self.labelHoughProbabilistic.setObjectName(u"labelHoughProbabilistic")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelHoughProbabilistic)

        self.labelHoughRho = QLabel(self.groupHough)
        self.labelHoughRho.setObjectName(u"labelHoughRho")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelHoughRho)

        self.labelHoughTheta = QLabel(self.groupHough)
        self.labelHoughTheta.setObjectName(u"labelHoughTheta")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelHoughTheta)

        self.labelHoughThreshold = QLabel(self.groupHough)
        self.labelHoughThreshold.setObjectName(u"labelHoughThreshold")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelHoughThreshold)

        self.labelHoughSrn = QLabel(self.groupHough)
        self.labelHoughSrn.setObjectName(u"labelHoughSrn")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelHoughSrn)

        self.labelHoughStn = QLabel(self.groupHough)
        self.labelHoughStn.setObjectName(u"labelHoughStn")

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelHoughStn)

        self.labelHoughMinTheta = QLabel(self.groupHough)
        self.labelHoughMinTheta.setObjectName(u"labelHoughMinTheta")

        self.formLayout_3.setWidget(7, QFormLayout.ItemRole.LabelRole, self.labelHoughMinTheta)

        self.labelHoughMaxTheta = QLabel(self.groupHough)
        self.labelHoughMaxTheta.setObjectName(u"labelHoughMaxTheta")

        self.formLayout_3.setWidget(8, QFormLayout.ItemRole.LabelRole, self.labelHoughMaxTheta)

        self.checkboxHoughEnabled = QCheckBox(self.groupHough)
        self.checkboxHoughEnabled.setObjectName(u"checkboxHoughEnabled")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxHoughEnabled)

        self.checkboxHoughProbabilistic = QCheckBox(self.groupHough)
        self.checkboxHoughProbabilistic.setObjectName(u"checkboxHoughProbabilistic")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.checkboxHoughProbabilistic)

        self.layoutHoughRho = QHBoxLayout()
        self.layoutHoughRho.setObjectName(u"layoutHoughRho")
        self.sliderHoughRho = QSlider(self.groupHough)
        self.sliderHoughRho.setObjectName(u"sliderHoughRho")
        sizePolicy1.setHeightForWidth(self.sliderHoughRho.sizePolicy().hasHeightForWidth())
        self.sliderHoughRho.setSizePolicy(sizePolicy1)
        self.sliderHoughRho.setMinimum(1)
        self.sliderHoughRho.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHoughRho.addWidget(self.sliderHoughRho)

        self.spinboxHoughRho = QSpinBox(self.groupHough)
        self.spinboxHoughRho.setObjectName(u"spinboxHoughRho")
        sizePolicy2.setHeightForWidth(self.spinboxHoughRho.sizePolicy().hasHeightForWidth())
        self.spinboxHoughRho.setSizePolicy(sizePolicy2)
        self.spinboxHoughRho.setMinimum(1)

        self.layoutHoughRho.addWidget(self.spinboxHoughRho)


        self.formLayout_3.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutHoughRho)

        self.layoutHoughTheta = QHBoxLayout()
        self.layoutHoughTheta.setObjectName(u"layoutHoughTheta")
        self.dialHoughTheta = QDial(self.groupHough)
        self.dialHoughTheta.setObjectName(u"dialHoughTheta")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(4)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.dialHoughTheta.sizePolicy().hasHeightForWidth())
        self.dialHoughTheta.setSizePolicy(sizePolicy3)
        self.dialHoughTheta.setMinimum(1)
        self.dialHoughTheta.setMaximum(360)
        self.dialHoughTheta.setOrientation(Qt.Orientation.Horizontal)
        self.dialHoughTheta.setNotchTarget(37.000000000000000)
        self.dialHoughTheta.setNotchesVisible(True)

        self.layoutHoughTheta.addWidget(self.dialHoughTheta)

        self.spinboxHoughTheta = QSpinBox(self.groupHough)
        self.spinboxHoughTheta.setObjectName(u"spinboxHoughTheta")
        sizePolicy2.setHeightForWidth(self.spinboxHoughTheta.sizePolicy().hasHeightForWidth())
        self.spinboxHoughTheta.setSizePolicy(sizePolicy2)
        self.spinboxHoughTheta.setMinimum(1)
        self.spinboxHoughTheta.setMaximum(360)

        self.layoutHoughTheta.addWidget(self.spinboxHoughTheta)


        self.formLayout_3.setLayout(3, QFormLayout.ItemRole.FieldRole, self.layoutHoughTheta)

        self.layoutHoughThreshold = QHBoxLayout()
        self.layoutHoughThreshold.setObjectName(u"layoutHoughThreshold")
        self.sliderHoughThreshold = QSlider(self.groupHough)
        self.sliderHoughThreshold.setObjectName(u"sliderHoughThreshold")
        sizePolicy1.setHeightForWidth(self.sliderHoughThreshold.sizePolicy().hasHeightForWidth())
        self.sliderHoughThreshold.setSizePolicy(sizePolicy1)
        self.sliderHoughThreshold.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHoughThreshold.addWidget(self.sliderHoughThreshold)

        self.spinboxHoughThreshold = QSpinBox(self.groupHough)
        self.spinboxHoughThreshold.setObjectName(u"spinboxHoughThreshold")
        sizePolicy2.setHeightForWidth(self.spinboxHoughThreshold.sizePolicy().hasHeightForWidth())
        self.spinboxHoughThreshold.setSizePolicy(sizePolicy2)

        self.layoutHoughThreshold.addWidget(self.spinboxHoughThreshold)


        self.formLayout_3.setLayout(4, QFormLayout.ItemRole.FieldRole, self.layoutHoughThreshold)

        self.layoutHoughMinTheta = QHBoxLayout()
        self.layoutHoughMinTheta.setObjectName(u"layoutHoughMinTheta")
        self.dialHoughMinTheta = QDial(self.groupHough)
        self.dialHoughMinTheta.setObjectName(u"dialHoughMinTheta")
        sizePolicy3.setHeightForWidth(self.dialHoughMinTheta.sizePolicy().hasHeightForWidth())
        self.dialHoughMinTheta.setSizePolicy(sizePolicy3)
        self.dialHoughMinTheta.setMaximum(359)
        self.dialHoughMinTheta.setNotchTarget(37.000000000000000)
        self.dialHoughMinTheta.setNotchesVisible(True)

        self.layoutHoughMinTheta.addWidget(self.dialHoughMinTheta)

        self.spinboxHoughMinTheta = QSpinBox(self.groupHough)
        self.spinboxHoughMinTheta.setObjectName(u"spinboxHoughMinTheta")
        sizePolicy2.setHeightForWidth(self.spinboxHoughMinTheta.sizePolicy().hasHeightForWidth())
        self.spinboxHoughMinTheta.setSizePolicy(sizePolicy2)
        self.spinboxHoughMinTheta.setMaximum(359)

        self.layoutHoughMinTheta.addWidget(self.spinboxHoughMinTheta)


        self.formLayout_3.setLayout(7, QFormLayout.ItemRole.FieldRole, self.layoutHoughMinTheta)

        self.layoutHoughMaxTheta = QHBoxLayout()
        self.layoutHoughMaxTheta.setObjectName(u"layoutHoughMaxTheta")
        self.dialHoughMaxTheta = QDial(self.groupHough)
        self.dialHoughMaxTheta.setObjectName(u"dialHoughMaxTheta")
        sizePolicy3.setHeightForWidth(self.dialHoughMaxTheta.sizePolicy().hasHeightForWidth())
        self.dialHoughMaxTheta.setSizePolicy(sizePolicy3)
        self.dialHoughMaxTheta.setMaximum(359)
        self.dialHoughMaxTheta.setNotchTarget(37.000000000000000)
        self.dialHoughMaxTheta.setNotchesVisible(True)

        self.layoutHoughMaxTheta.addWidget(self.dialHoughMaxTheta)

        self.spinboxHoughMaxTheta = QSpinBox(self.groupHough)
        self.spinboxHoughMaxTheta.setObjectName(u"spinboxHoughMaxTheta")
        sizePolicy2.setHeightForWidth(self.spinboxHoughMaxTheta.sizePolicy().hasHeightForWidth())
        self.spinboxHoughMaxTheta.setSizePolicy(sizePolicy2)
        self.spinboxHoughMaxTheta.setMaximum(359)

        self.layoutHoughMaxTheta.addWidget(self.spinboxHoughMaxTheta)


        self.formLayout_3.setLayout(8, QFormLayout.ItemRole.FieldRole, self.layoutHoughMaxTheta)

        self.layoutHoughSrn = QHBoxLayout()
        self.layoutHoughSrn.setObjectName(u"layoutHoughSrn")
        self.widgetHoughSrn = QWidget(self.groupHough)
        self.widgetHoughSrn.setObjectName(u"widgetHoughSrn")
        sizePolicy3.setHeightForWidth(self.widgetHoughSrn.sizePolicy().hasHeightForWidth())
        self.widgetHoughSrn.setSizePolicy(sizePolicy3)

        self.layoutHoughSrn.addWidget(self.widgetHoughSrn)

        self.spinboxHoughSrn = QDoubleSpinBox(self.groupHough)
        self.spinboxHoughSrn.setObjectName(u"spinboxHoughSrn")

        self.layoutHoughSrn.addWidget(self.spinboxHoughSrn)


        self.formLayout_3.setLayout(5, QFormLayout.ItemRole.FieldRole, self.layoutHoughSrn)

        self.layoutHoughStn = QHBoxLayout()
        self.layoutHoughStn.setObjectName(u"layoutHoughStn")
        self.widgetHoughStn = QWidget(self.groupHough)
        self.widgetHoughStn.setObjectName(u"widgetHoughStn")
        sizePolicy3.setHeightForWidth(self.widgetHoughStn.sizePolicy().hasHeightForWidth())
        self.widgetHoughStn.setSizePolicy(sizePolicy3)

        self.layoutHoughStn.addWidget(self.widgetHoughStn)

        self.spinboxHoughStn = QDoubleSpinBox(self.groupHough)
        self.spinboxHoughStn.setObjectName(u"spinboxHoughStn")

        self.layoutHoughStn.addWidget(self.spinboxHoughStn)


        self.formLayout_3.setLayout(6, QFormLayout.ItemRole.FieldRole, self.layoutHoughStn)

        self.labelHoughMinLineLength = QLabel(self.groupHough)
        self.labelHoughMinLineLength.setObjectName(u"labelHoughMinLineLength")
        self.labelHoughMinLineLength.setFrameShape(QFrame.Shape.NoFrame)

        self.formLayout_3.setWidget(9, QFormLayout.ItemRole.LabelRole, self.labelHoughMinLineLength)

        self.labelHoughMaxLineGap = QLabel(self.groupHough)
        self.labelHoughMaxLineGap.setObjectName(u"labelHoughMaxLineGap")

        self.formLayout_3.setWidget(10, QFormLayout.ItemRole.LabelRole, self.labelHoughMaxLineGap)

        self.layoutHoughMinLineLength = QHBoxLayout()
        self.layoutHoughMinLineLength.setObjectName(u"layoutHoughMinLineLength")
        self.sliderHoughMinLineLength = QSlider(self.groupHough)
        self.sliderHoughMinLineLength.setObjectName(u"sliderHoughMinLineLength")
        sizePolicy1.setHeightForWidth(self.sliderHoughMinLineLength.sizePolicy().hasHeightForWidth())
        self.sliderHoughMinLineLength.setSizePolicy(sizePolicy1)
        self.sliderHoughMinLineLength.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHoughMinLineLength.addWidget(self.sliderHoughMinLineLength)

        self.spinboxHoughMinLineLength = QSpinBox(self.groupHough)
        self.spinboxHoughMinLineLength.setObjectName(u"spinboxHoughMinLineLength")
        sizePolicy2.setHeightForWidth(self.spinboxHoughMinLineLength.sizePolicy().hasHeightForWidth())
        self.spinboxHoughMinLineLength.setSizePolicy(sizePolicy2)

        self.layoutHoughMinLineLength.addWidget(self.spinboxHoughMinLineLength)


        self.formLayout_3.setLayout(9, QFormLayout.ItemRole.FieldRole, self.layoutHoughMinLineLength)

        self.layoutHoughMaxLineGap = QHBoxLayout()
        self.layoutHoughMaxLineGap.setObjectName(u"layoutHoughMaxLineGap")
        self.sliderHoughMaxLineGap = QSlider(self.groupHough)
        self.sliderHoughMaxLineGap.setObjectName(u"sliderHoughMaxLineGap")
        sizePolicy1.setHeightForWidth(self.sliderHoughMaxLineGap.sizePolicy().hasHeightForWidth())
        self.sliderHoughMaxLineGap.setSizePolicy(sizePolicy1)
        self.sliderHoughMaxLineGap.setOrientation(Qt.Orientation.Horizontal)

        self.layoutHoughMaxLineGap.addWidget(self.sliderHoughMaxLineGap)

        self.spinboxHoughMaxLineGap = QSpinBox(self.groupHough)
        self.spinboxHoughMaxLineGap.setObjectName(u"spinboxHoughMaxLineGap")
        sizePolicy2.setHeightForWidth(self.spinboxHoughMaxLineGap.sizePolicy().hasHeightForWidth())
        self.spinboxHoughMaxLineGap.setSizePolicy(sizePolicy2)

        self.layoutHoughMaxLineGap.addWidget(self.spinboxHoughMaxLineGap)


        self.formLayout_3.setLayout(10, QFormLayout.ItemRole.FieldRole, self.layoutHoughMaxLineGap)


        self.layoutScrollAreaPropertiesDock.addWidget(self.groupHough, 4, 0, 1, 1)

        self.group1Blur = QGroupBox(self.scrollAreaWidgetContents)
        self.group1Blur.setObjectName(u"group1Blur")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.group1Blur.sizePolicy().hasHeightForWidth())
        self.group1Blur.setSizePolicy(sizePolicy4)
        self.layoutBlur = QFormLayout(self.group1Blur)
        self.layoutBlur.setObjectName(u"layoutBlur")
        self.labelBlurEnabled = QLabel(self.group1Blur)
        self.labelBlurEnabled.setObjectName(u"labelBlurEnabled")

        self.layoutBlur.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelBlurEnabled)

        self.labelBlurKernelSize = QLabel(self.group1Blur)
        self.labelBlurKernelSize.setObjectName(u"labelBlurKernelSize")

        self.layoutBlur.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelBlurKernelSize)

        self.spinboxBlurKernelSize = QSpinBox(self.group1Blur)
        self.spinboxBlurKernelSize.setObjectName(u"spinboxBlurKernelSize")
        self.spinboxBlurKernelSize.setMinimum(1)
        self.spinboxBlurKernelSize.setSingleStep(2)
        self.spinboxBlurKernelSize.setValue(5)

        self.layoutBlur.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinboxBlurKernelSize)

        self.checkboxBlurEnabled = QCheckBox(self.group1Blur)
        self.checkboxBlurEnabled.setObjectName(u"checkboxBlurEnabled")
        self.checkboxBlurEnabled.setChecked(True)

        self.layoutBlur.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxBlurEnabled)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group1Blur, 1, 0, 1, 1)

        self.group3Canny = QGroupBox(self.scrollAreaWidgetContents)
        self.group3Canny.setObjectName(u"group3Canny")
        sizePolicy4.setHeightForWidth(self.group3Canny.sizePolicy().hasHeightForWidth())
        self.group3Canny.setSizePolicy(sizePolicy4)
        self.layoutCanny = QFormLayout(self.group3Canny)
        self.layoutCanny.setObjectName(u"layoutCanny")
        self.labelCannyEnabled = QLabel(self.group3Canny)
        self.labelCannyEnabled.setObjectName(u"labelCannyEnabled")

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCannyEnabled)

        self.checkboxCannyEnabled = QCheckBox(self.group3Canny)
        self.checkboxCannyEnabled.setObjectName(u"checkboxCannyEnabled")
        self.checkboxCannyEnabled.setChecked(True)

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxCannyEnabled)

        self.labelCannyThreshold1 = QLabel(self.group3Canny)
        self.labelCannyThreshold1.setObjectName(u"labelCannyThreshold1")

        self.layoutCanny.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold1)

        self.labelCannyThreshold2 = QLabel(self.group3Canny)
        self.labelCannyThreshold2.setObjectName(u"labelCannyThreshold2")

        self.layoutCanny.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold2)

        self.labelCannyApertureSize = QLabel(self.group3Canny)
        self.labelCannyApertureSize.setObjectName(u"labelCannyApertureSize")

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCannyApertureSize)

        self.layoutCannyThreshold1 = QHBoxLayout()
        self.layoutCannyThreshold1.setObjectName(u"layoutCannyThreshold1")
        self.sliderCannyThreshold1 = QSlider(self.group3Canny)
        self.sliderCannyThreshold1.setObjectName(u"sliderCannyThreshold1")
        sizePolicy1.setHeightForWidth(self.sliderCannyThreshold1.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold1.setSizePolicy(sizePolicy1)
        self.sliderCannyThreshold1.setMaximum(255)
        self.sliderCannyThreshold1.setValue(50)
        self.sliderCannyThreshold1.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold1.addWidget(self.sliderCannyThreshold1)

        self.spinboxCannyThreshold1 = QSpinBox(self.group3Canny)
        self.spinboxCannyThreshold1.setObjectName(u"spinboxCannyThreshold1")
        sizePolicy2.setHeightForWidth(self.spinboxCannyThreshold1.sizePolicy().hasHeightForWidth())
        self.spinboxCannyThreshold1.setSizePolicy(sizePolicy2)
        self.spinboxCannyThreshold1.setMaximum(255)
        self.spinboxCannyThreshold1.setValue(50)

        self.layoutCannyThreshold1.addWidget(self.spinboxCannyThreshold1)


        self.layoutCanny.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layoutCannyThreshold1)

        self.layoutCannyThreshold2 = QHBoxLayout()
        self.layoutCannyThreshold2.setObjectName(u"layoutCannyThreshold2")
        self.sliderCannyThreshold2 = QSlider(self.group3Canny)
        self.sliderCannyThreshold2.setObjectName(u"sliderCannyThreshold2")
        sizePolicy1.setHeightForWidth(self.sliderCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold2.setSizePolicy(sizePolicy1)
        self.sliderCannyThreshold2.setMaximum(255)
        self.sliderCannyThreshold2.setValue(150)
        self.sliderCannyThreshold2.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold2.addWidget(self.sliderCannyThreshold2)

        self.spinboxCannyThreshold2 = QSpinBox(self.group3Canny)
        self.spinboxCannyThreshold2.setObjectName(u"spinboxCannyThreshold2")
        sizePolicy2.setHeightForWidth(self.spinboxCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.spinboxCannyThreshold2.setSizePolicy(sizePolicy2)
        self.spinboxCannyThreshold2.setMaximum(255)
        self.spinboxCannyThreshold2.setValue(150)

        self.layoutCannyThreshold2.addWidget(self.spinboxCannyThreshold2)


        self.layoutCanny.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutCannyThreshold2)

        self.spinboxCannyApertureSize = QSpinBox(self.group3Canny)
        self.spinboxCannyApertureSize.setObjectName(u"spinboxCannyApertureSize")
        self.spinboxCannyApertureSize.setMinimum(3)
        self.spinboxCannyApertureSize.setMaximum(7)
        self.spinboxCannyApertureSize.setSingleStep(2)

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spinboxCannyApertureSize)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group3Canny, 3, 0, 1, 1)

        self.group0Downscale = QGroupBox(self.scrollAreaWidgetContents)
        self.group0Downscale.setObjectName(u"group0Downscale")
        sizePolicy4.setHeightForWidth(self.group0Downscale.sizePolicy().hasHeightForWidth())
        self.group0Downscale.setSizePolicy(sizePolicy4)
        self.layoutDownscale = QFormLayout(self.group0Downscale)
        self.layoutDownscale.setObjectName(u"layoutDownscale")
        self.labelDownscaleMaxSize = QLabel(self.group0Downscale)
        self.labelDownscaleMaxSize.setObjectName(u"labelDownscaleMaxSize")

        self.layoutDownscale.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelDownscaleMaxSize)

        self.spinboxDownscaleMaxSize = QSpinBox(self.group0Downscale)
        self.spinboxDownscaleMaxSize.setObjectName(u"spinboxDownscaleMaxSize")
        self.spinboxDownscaleMaxSize.setMaximum(3000)
        self.spinboxDownscaleMaxSize.setValue(800)

        self.layoutDownscale.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinboxDownscaleMaxSize)

        self.labelDownscaleEnabled = QLabel(self.group0Downscale)
        self.labelDownscaleEnabled.setObjectName(u"labelDownscaleEnabled")

        self.layoutDownscale.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDownscaleEnabled)

        self.checkboxDownscaleEnabled = QCheckBox(self.group0Downscale)
        self.checkboxDownscaleEnabled.setObjectName(u"checkboxDownscaleEnabled")
        self.checkboxDownscaleEnabled.setChecked(True)

        self.layoutDownscale.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxDownscaleEnabled)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group0Downscale, 0, 0, 1, 1)

        self.groupFixPerspective = QGroupBox(self.scrollAreaWidgetContents)
        self.groupFixPerspective.setObjectName(u"groupFixPerspective")
        self.formLayout_4 = QFormLayout(self.groupFixPerspective)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.labelFixPerspectiveEnabled = QLabel(self.groupFixPerspective)
        self.labelFixPerspectiveEnabled.setObjectName(u"labelFixPerspectiveEnabled")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelFixPerspectiveEnabled)

        self.checkboxFixPerspectiveEnabled = QCheckBox(self.groupFixPerspective)
        self.checkboxFixPerspectiveEnabled.setObjectName(u"checkboxFixPerspectiveEnabled")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxFixPerspectiveEnabled)

        self.labelFixPerspectiveWidth = QLabel(self.groupFixPerspective)
        self.labelFixPerspectiveWidth.setObjectName(u"labelFixPerspectiveWidth")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelFixPerspectiveWidth)

        self.layoutFixPerspectiveWidth = QHBoxLayout()
        self.layoutFixPerspectiveWidth.setObjectName(u"layoutFixPerspectiveWidth")
        self.widgetFixPerspectiveWidth = QWidget(self.groupFixPerspective)
        self.widgetFixPerspectiveWidth.setObjectName(u"widgetFixPerspectiveWidth")
        sizePolicy3.setHeightForWidth(self.widgetFixPerspectiveWidth.sizePolicy().hasHeightForWidth())
        self.widgetFixPerspectiveWidth.setSizePolicy(sizePolicy3)

        self.layoutFixPerspectiveWidth.addWidget(self.widgetFixPerspectiveWidth)

        self.spinboxFixPerspectiveWidth = QSpinBox(self.groupFixPerspective)
        self.spinboxFixPerspectiveWidth.setObjectName(u"spinboxFixPerspectiveWidth")
        sizePolicy2.setHeightForWidth(self.spinboxFixPerspectiveWidth.sizePolicy().hasHeightForWidth())
        self.spinboxFixPerspectiveWidth.setSizePolicy(sizePolicy2)
        self.spinboxFixPerspectiveWidth.setMinimum(100)
        self.spinboxFixPerspectiveWidth.setMaximum(10240)
        self.spinboxFixPerspectiveWidth.setSingleStep(10)

        self.layoutFixPerspectiveWidth.addWidget(self.spinboxFixPerspectiveWidth)


        self.formLayout_4.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layoutFixPerspectiveWidth)

        self.labelFixPerspectiveHeight = QLabel(self.groupFixPerspective)
        self.labelFixPerspectiveHeight.setObjectName(u"labelFixPerspectiveHeight")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelFixPerspectiveHeight)

        self.layoutFixPerspectiveHeight = QHBoxLayout()
        self.layoutFixPerspectiveHeight.setObjectName(u"layoutFixPerspectiveHeight")
        self.widgetFixPerspectiveHeight = QWidget(self.groupFixPerspective)
        self.widgetFixPerspectiveHeight.setObjectName(u"widgetFixPerspectiveHeight")
        sizePolicy3.setHeightForWidth(self.widgetFixPerspectiveHeight.sizePolicy().hasHeightForWidth())
        self.widgetFixPerspectiveHeight.setSizePolicy(sizePolicy3)

        self.layoutFixPerspectiveHeight.addWidget(self.widgetFixPerspectiveHeight)

        self.spinboxFixPerspectiveHeight = QSpinBox(self.groupFixPerspective)
        self.spinboxFixPerspectiveHeight.setObjectName(u"spinboxFixPerspectiveHeight")
        sizePolicy2.setHeightForWidth(self.spinboxFixPerspectiveHeight.sizePolicy().hasHeightForWidth())
        self.spinboxFixPerspectiveHeight.setSizePolicy(sizePolicy2)
        self.spinboxFixPerspectiveHeight.setMinimum(100)
        self.spinboxFixPerspectiveHeight.setMaximum(10240)
        self.spinboxFixPerspectiveHeight.setSingleStep(10)

        self.layoutFixPerspectiveHeight.addWidget(self.spinboxFixPerspectiveHeight)


        self.formLayout_4.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutFixPerspectiveHeight)


        self.layoutScrollAreaPropertiesDock.addWidget(self.groupFixPerspective, 6, 0, 1, 1)

        self.scrollareaPropertiesDock.setWidget(self.scrollAreaWidgetContents)

        self.layoutPropertiesDock.addWidget(self.scrollareaPropertiesDock, 0, 0, 1, 1)

        PropertiesDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(PropertiesDock)

        QMetaObject.connectSlotsByName(PropertiesDock)
    # setupUi

    def retranslateUi(self, PropertiesDock):
        PropertiesDock.setWindowTitle(QCoreApplication.translate("PropertiesDock", u"Properties", None))
        self.group2Threshold.setTitle(QCoreApplication.translate("PropertiesDock", u"Thresholding", None))
        self.labelThresholdingMethod.setText(QCoreApplication.translate("PropertiesDock", u"Method", None))
        self.comboboxThresholdingMethod.setItemText(0, QCoreApplication.translate("PropertiesDock", u"None", None))
        self.comboboxThresholdingMethod.setItemText(1, QCoreApplication.translate("PropertiesDock", u"Binary", None))
        self.comboboxThresholdingMethod.setItemText(2, QCoreApplication.translate("PropertiesDock", u"Truncate", None))
        self.comboboxThresholdingMethod.setItemText(3, QCoreApplication.translate("PropertiesDock", u"To Zero", None))
        self.comboboxThresholdingMethod.setItemText(4, QCoreApplication.translate("PropertiesDock", u"Mean", None))
        self.comboboxThresholdingMethod.setItemText(5, QCoreApplication.translate("PropertiesDock", u"Gaussian", None))

        self.labelThresholdingThreshold.setText(QCoreApplication.translate("PropertiesDock", u"Threshold", None))
        self.labelThresholdingMaximum.setText(QCoreApplication.translate("PropertiesDock", u"Maximum", None))
        self.labelThresholdingBlockSize.setText(QCoreApplication.translate("PropertiesDock", u"Block size", None))
        self.labelThresholdingC.setText(QCoreApplication.translate("PropertiesDock", u"C", None))
        self.labelThresholdingOtsu.setText(QCoreApplication.translate("PropertiesDock", u"Otsu", None))
        self.checkboxThresholdingOtsu.setText("")
        self.labelThresholdingInverse.setText(QCoreApplication.translate("PropertiesDock", u"Inverse", None))
        self.checkboxThresholdingInverse.setText("")
        self.group4FindContour.setTitle(QCoreApplication.translate("PropertiesDock", u"Find Contour", None))
        self.labelFindContourEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.labelFindContourMethod.setText(QCoreApplication.translate("PropertiesDock", u"Method", None))
        self.comboboxFindContourMethod.setItemText(0, QCoreApplication.translate("PropertiesDock", u"None", None))
        self.comboboxFindContourMethod.setItemText(1, QCoreApplication.translate("PropertiesDock", u"Simple", None))
        self.comboboxFindContourMethod.setItemText(2, QCoreApplication.translate("PropertiesDock", u"Teh-Chin L1", None))
        self.comboboxFindContourMethod.setItemText(3, QCoreApplication.translate("PropertiesDock", u"Teh-Chin KCOS", None))

        self.checkboxFindContourEnabled.setText("")
        self.groupHough.setTitle(QCoreApplication.translate("PropertiesDock", u"Hough", None))
        self.labelHoughEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.labelHoughProbabilistic.setText(QCoreApplication.translate("PropertiesDock", u"Probabilistic", None))
        self.labelHoughRho.setText(QCoreApplication.translate("PropertiesDock", u"Rho", None))
        self.labelHoughTheta.setText(QCoreApplication.translate("PropertiesDock", u"Theta", None))
        self.labelHoughThreshold.setText(QCoreApplication.translate("PropertiesDock", u"Threshold", None))
        self.labelHoughSrn.setText(QCoreApplication.translate("PropertiesDock", u"Srn", None))
        self.labelHoughStn.setText(QCoreApplication.translate("PropertiesDock", u"Stn", None))
        self.labelHoughMinTheta.setText(QCoreApplication.translate("PropertiesDock", u"Min Theta", None))
        self.labelHoughMaxTheta.setText(QCoreApplication.translate("PropertiesDock", u"Max Theta", None))
        self.checkboxHoughEnabled.setText("")
        self.checkboxHoughProbabilistic.setText("")
        self.labelHoughMinLineLength.setText(QCoreApplication.translate("PropertiesDock", u"Min Line Length", None))
        self.labelHoughMaxLineGap.setText(QCoreApplication.translate("PropertiesDock", u"Max Line Gap", None))
        self.group1Blur.setTitle(QCoreApplication.translate("PropertiesDock", u"Gaussian Blur", None))
        self.labelBlurEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.labelBlurKernelSize.setText(QCoreApplication.translate("PropertiesDock", u"Kernel size", None))
        self.spinboxBlurKernelSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.checkboxBlurEnabled.setText("")
        self.group3Canny.setTitle(QCoreApplication.translate("PropertiesDock", u"Canny", None))
        self.labelCannyEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.checkboxCannyEnabled.setText("")
        self.labelCannyThreshold1.setText(QCoreApplication.translate("PropertiesDock", u"Threshold 1", None))
        self.labelCannyThreshold2.setText(QCoreApplication.translate("PropertiesDock", u"Threshold 2", None))
        self.labelCannyApertureSize.setText(QCoreApplication.translate("PropertiesDock", u"Aperture size", None))
        self.spinboxCannyApertureSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.group0Downscale.setTitle(QCoreApplication.translate("PropertiesDock", u"Downscale", None))
        self.labelDownscaleMaxSize.setText(QCoreApplication.translate("PropertiesDock", u"Max Size", None))
        self.spinboxDownscaleMaxSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.labelDownscaleEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.checkboxDownscaleEnabled.setText("")
        self.groupFixPerspective.setTitle(QCoreApplication.translate("PropertiesDock", u"Fix Perspective", None))
        self.labelFixPerspectiveEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.checkboxFixPerspectiveEnabled.setText("")
        self.labelFixPerspectiveWidth.setText(QCoreApplication.translate("PropertiesDock", u"Width", None))
        self.spinboxFixPerspectiveWidth.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.labelFixPerspectiveHeight.setText(QCoreApplication.translate("PropertiesDock", u"Height", None))
        self.spinboxFixPerspectiveHeight.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
    # retranslateUi

