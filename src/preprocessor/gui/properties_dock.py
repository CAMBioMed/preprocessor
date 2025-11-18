# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_dock.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDockWidget, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QWidget)

class Ui_PropertiesDock(object):
    def setupUi(self, PropertiesDock):
        if not PropertiesDock.objectName():
            PropertiesDock.setObjectName(u"PropertiesDock")
        PropertiesDock.resize(494, 410)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.layoutPropertiesDock = QGridLayout(self.dockWidgetContents)
        self.layoutPropertiesDock.setObjectName(u"layoutPropertiesDock")
        self.scrollareaPropertiesDock = QScrollArea(self.dockWidgetContents)
        self.scrollareaPropertiesDock.setObjectName(u"scrollareaPropertiesDock")
        self.scrollareaPropertiesDock.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 460, 434))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.layoutScrollAreaPropertiesDock = QGridLayout(self.scrollAreaWidgetContents)
        self.layoutScrollAreaPropertiesDock.setObjectName(u"layoutScrollAreaPropertiesDock")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutScrollAreaPropertiesDock.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.group0Downscale = QGroupBox(self.scrollAreaWidgetContents)
        self.group0Downscale.setObjectName(u"group0Downscale")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.group0Downscale.sizePolicy().hasHeightForWidth())
        self.group0Downscale.setSizePolicy(sizePolicy1)
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

        self.group1Blur = QGroupBox(self.scrollAreaWidgetContents)
        self.group1Blur.setObjectName(u"group1Blur")
        sizePolicy1.setHeightForWidth(self.group1Blur.sizePolicy().hasHeightForWidth())
        self.group1Blur.setSizePolicy(sizePolicy1)
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

        self.group2Canny = QGroupBox(self.scrollAreaWidgetContents)
        self.group2Canny.setObjectName(u"group2Canny")
        sizePolicy1.setHeightForWidth(self.group2Canny.sizePolicy().hasHeightForWidth())
        self.group2Canny.setSizePolicy(sizePolicy1)
        self.layoutCanny = QFormLayout(self.group2Canny)
        self.layoutCanny.setObjectName(u"layoutCanny")
        self.labelCannyEnabled = QLabel(self.group2Canny)
        self.labelCannyEnabled.setObjectName(u"labelCannyEnabled")

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCannyEnabled)

        self.checkboxCannyEnabled = QCheckBox(self.group2Canny)
        self.checkboxCannyEnabled.setObjectName(u"checkboxCannyEnabled")
        self.checkboxCannyEnabled.setChecked(True)

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxCannyEnabled)

        self.labelCannyThreshold1 = QLabel(self.group2Canny)
        self.labelCannyThreshold1.setObjectName(u"labelCannyThreshold1")

        self.layoutCanny.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold1)

        self.labelCannyThreshold2 = QLabel(self.group2Canny)
        self.labelCannyThreshold2.setObjectName(u"labelCannyThreshold2")

        self.layoutCanny.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold2)

        self.labelCannyApertureSize = QLabel(self.group2Canny)
        self.labelCannyApertureSize.setObjectName(u"labelCannyApertureSize")

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCannyApertureSize)

        self.layoutCannyThreshold1 = QHBoxLayout()
        self.layoutCannyThreshold1.setObjectName(u"layoutCannyThreshold1")
        self.sliderCannyThreshold1 = QSlider(self.group2Canny)
        self.sliderCannyThreshold1.setObjectName(u"sliderCannyThreshold1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sliderCannyThreshold1.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold1.setSizePolicy(sizePolicy2)
        self.sliderCannyThreshold1.setMaximum(255)
        self.sliderCannyThreshold1.setValue(50)
        self.sliderCannyThreshold1.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold1.addWidget(self.sliderCannyThreshold1)

        self.spinboxCannyThreshold1 = QSpinBox(self.group2Canny)
        self.spinboxCannyThreshold1.setObjectName(u"spinboxCannyThreshold1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.spinboxCannyThreshold1.sizePolicy().hasHeightForWidth())
        self.spinboxCannyThreshold1.setSizePolicy(sizePolicy3)
        self.spinboxCannyThreshold1.setMaximum(255)
        self.spinboxCannyThreshold1.setValue(50)

        self.layoutCannyThreshold1.addWidget(self.spinboxCannyThreshold1)


        self.layoutCanny.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layoutCannyThreshold1)

        self.layoutCannyThreshold2 = QHBoxLayout()
        self.layoutCannyThreshold2.setObjectName(u"layoutCannyThreshold2")
        self.sliderCannyThreshold2 = QSlider(self.group2Canny)
        self.sliderCannyThreshold2.setObjectName(u"sliderCannyThreshold2")
        sizePolicy2.setHeightForWidth(self.sliderCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold2.setSizePolicy(sizePolicy2)
        self.sliderCannyThreshold2.setMaximum(255)
        self.sliderCannyThreshold2.setValue(150)
        self.sliderCannyThreshold2.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold2.addWidget(self.sliderCannyThreshold2)

        self.spinboxCannyThreshold2 = QSpinBox(self.group2Canny)
        self.spinboxCannyThreshold2.setObjectName(u"spinboxCannyThreshold2")
        sizePolicy3.setHeightForWidth(self.spinboxCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.spinboxCannyThreshold2.setSizePolicy(sizePolicy3)
        self.spinboxCannyThreshold2.setMaximum(255)
        self.spinboxCannyThreshold2.setValue(150)

        self.layoutCannyThreshold2.addWidget(self.spinboxCannyThreshold2)


        self.layoutCanny.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutCannyThreshold2)

        self.spinboxCannyApertureSize = QSpinBox(self.group2Canny)
        self.spinboxCannyApertureSize.setObjectName(u"spinboxCannyApertureSize")
        self.spinboxCannyApertureSize.setMinimum(3)
        self.spinboxCannyApertureSize.setMaximum(7)
        self.spinboxCannyApertureSize.setSingleStep(2)

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spinboxCannyApertureSize)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group2Canny, 2, 0, 1, 1)

        self.scrollareaPropertiesDock.setWidget(self.scrollAreaWidgetContents)

        self.layoutPropertiesDock.addWidget(self.scrollareaPropertiesDock, 0, 0, 1, 1)

        PropertiesDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(PropertiesDock)

        QMetaObject.connectSlotsByName(PropertiesDock)
    # setupUi

    def retranslateUi(self, PropertiesDock):
        PropertiesDock.setWindowTitle(QCoreApplication.translate("PropertiesDock", u"Properties", None))
        self.group0Downscale.setTitle(QCoreApplication.translate("PropertiesDock", u"Downscale", None))
        self.labelDownscaleMaxSize.setText(QCoreApplication.translate("PropertiesDock", u"Max Size", None))
        self.spinboxDownscaleMaxSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.labelDownscaleEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.checkboxDownscaleEnabled.setText("")
        self.group1Blur.setTitle(QCoreApplication.translate("PropertiesDock", u"Gaussian Blur", None))
        self.labelBlurEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.labelBlurKernelSize.setText(QCoreApplication.translate("PropertiesDock", u"Kernel size", None))
        self.spinboxBlurKernelSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
        self.checkboxBlurEnabled.setText("")
        self.group2Canny.setTitle(QCoreApplication.translate("PropertiesDock", u"Canny", None))
        self.labelCannyEnabled.setText(QCoreApplication.translate("PropertiesDock", u"Enabled", None))
        self.checkboxCannyEnabled.setText("")
        self.labelCannyThreshold1.setText(QCoreApplication.translate("PropertiesDock", u"Threshold 1", None))
        self.labelCannyThreshold2.setText(QCoreApplication.translate("PropertiesDock", u"Threshold 2", None))
        self.labelCannyApertureSize.setText(QCoreApplication.translate("PropertiesDock", u"Aperture size", None))
        self.spinboxCannyApertureSize.setSuffix(QCoreApplication.translate("PropertiesDock", u" px", None))
    # retranslateUi

