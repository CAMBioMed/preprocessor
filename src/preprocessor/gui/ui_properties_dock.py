
################################################################################
## Form generated from reading UI file 'properties_dock.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
    Qt)
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QScrollArea, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QWidget)

class Ui_PropertiesDock:
    def setupUi(self, PropertiesDock):
        if not PropertiesDock.objectName():
            PropertiesDock.setObjectName("PropertiesDock")
        PropertiesDock.resize(494, 506)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.layoutPropertiesDock = QGridLayout(self.dockWidgetContents)
        self.layoutPropertiesDock.setObjectName("layoutPropertiesDock")
        self.scrollareaPropertiesDock = QScrollArea(self.dockWidgetContents)
        self.scrollareaPropertiesDock.setObjectName("scrollareaPropertiesDock")
        self.scrollareaPropertiesDock.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -196, 460, 662))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.layoutScrollAreaPropertiesDock = QGridLayout(self.scrollAreaWidgetContents)
        self.layoutScrollAreaPropertiesDock.setObjectName("layoutScrollAreaPropertiesDock")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutScrollAreaPropertiesDock.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.group0Downscale = QGroupBox(self.scrollAreaWidgetContents)
        self.group0Downscale.setObjectName("group0Downscale")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.group0Downscale.sizePolicy().hasHeightForWidth())
        self.group0Downscale.setSizePolicy(sizePolicy1)
        self.layoutDownscale = QFormLayout(self.group0Downscale)
        self.layoutDownscale.setObjectName("layoutDownscale")
        self.labelDownscaleMaxSize = QLabel(self.group0Downscale)
        self.labelDownscaleMaxSize.setObjectName("labelDownscaleMaxSize")

        self.layoutDownscale.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelDownscaleMaxSize)

        self.spinboxDownscaleMaxSize = QSpinBox(self.group0Downscale)
        self.spinboxDownscaleMaxSize.setObjectName("spinboxDownscaleMaxSize")
        self.spinboxDownscaleMaxSize.setMaximum(3000)
        self.spinboxDownscaleMaxSize.setValue(800)

        self.layoutDownscale.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinboxDownscaleMaxSize)

        self.labelDownscaleEnabled = QLabel(self.group0Downscale)
        self.labelDownscaleEnabled.setObjectName("labelDownscaleEnabled")

        self.layoutDownscale.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDownscaleEnabled)

        self.checkboxDownscaleEnabled = QCheckBox(self.group0Downscale)
        self.checkboxDownscaleEnabled.setObjectName("checkboxDownscaleEnabled")
        self.checkboxDownscaleEnabled.setChecked(True)

        self.layoutDownscale.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxDownscaleEnabled)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group0Downscale, 0, 0, 1, 1)

        self.group1Blur = QGroupBox(self.scrollAreaWidgetContents)
        self.group1Blur.setObjectName("group1Blur")
        sizePolicy1.setHeightForWidth(self.group1Blur.sizePolicy().hasHeightForWidth())
        self.group1Blur.setSizePolicy(sizePolicy1)
        self.layoutBlur = QFormLayout(self.group1Blur)
        self.layoutBlur.setObjectName("layoutBlur")
        self.labelBlurEnabled = QLabel(self.group1Blur)
        self.labelBlurEnabled.setObjectName("labelBlurEnabled")

        self.layoutBlur.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelBlurEnabled)

        self.labelBlurKernelSize = QLabel(self.group1Blur)
        self.labelBlurKernelSize.setObjectName("labelBlurKernelSize")

        self.layoutBlur.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelBlurKernelSize)

        self.spinboxBlurKernelSize = QSpinBox(self.group1Blur)
        self.spinboxBlurKernelSize.setObjectName("spinboxBlurKernelSize")
        self.spinboxBlurKernelSize.setMinimum(1)
        self.spinboxBlurKernelSize.setSingleStep(2)
        self.spinboxBlurKernelSize.setValue(5)

        self.layoutBlur.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinboxBlurKernelSize)

        self.checkboxBlurEnabled = QCheckBox(self.group1Blur)
        self.checkboxBlurEnabled.setObjectName("checkboxBlurEnabled")
        self.checkboxBlurEnabled.setChecked(True)

        self.layoutBlur.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxBlurEnabled)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group1Blur, 1, 0, 1, 1)

        self.group3Canny = QGroupBox(self.scrollAreaWidgetContents)
        self.group3Canny.setObjectName("group3Canny")
        sizePolicy1.setHeightForWidth(self.group3Canny.sizePolicy().hasHeightForWidth())
        self.group3Canny.setSizePolicy(sizePolicy1)
        self.layoutCanny = QFormLayout(self.group3Canny)
        self.layoutCanny.setObjectName("layoutCanny")
        self.labelCannyEnabled = QLabel(self.group3Canny)
        self.labelCannyEnabled.setObjectName("labelCannyEnabled")

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCannyEnabled)

        self.checkboxCannyEnabled = QCheckBox(self.group3Canny)
        self.checkboxCannyEnabled.setObjectName("checkboxCannyEnabled")
        self.checkboxCannyEnabled.setChecked(True)

        self.layoutCanny.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkboxCannyEnabled)

        self.labelCannyThreshold1 = QLabel(self.group3Canny)
        self.labelCannyThreshold1.setObjectName("labelCannyThreshold1")

        self.layoutCanny.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold1)

        self.labelCannyThreshold2 = QLabel(self.group3Canny)
        self.labelCannyThreshold2.setObjectName("labelCannyThreshold2")

        self.layoutCanny.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCannyThreshold2)

        self.labelCannyApertureSize = QLabel(self.group3Canny)
        self.labelCannyApertureSize.setObjectName("labelCannyApertureSize")

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCannyApertureSize)

        self.layoutCannyThreshold1 = QHBoxLayout()
        self.layoutCannyThreshold1.setObjectName("layoutCannyThreshold1")
        self.sliderCannyThreshold1 = QSlider(self.group3Canny)
        self.sliderCannyThreshold1.setObjectName("sliderCannyThreshold1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sliderCannyThreshold1.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold1.setSizePolicy(sizePolicy2)
        self.sliderCannyThreshold1.setMaximum(255)
        self.sliderCannyThreshold1.setValue(50)
        self.sliderCannyThreshold1.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold1.addWidget(self.sliderCannyThreshold1)

        self.spinboxCannyThreshold1 = QSpinBox(self.group3Canny)
        self.spinboxCannyThreshold1.setObjectName("spinboxCannyThreshold1")
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
        self.layoutCannyThreshold2.setObjectName("layoutCannyThreshold2")
        self.sliderCannyThreshold2 = QSlider(self.group3Canny)
        self.sliderCannyThreshold2.setObjectName("sliderCannyThreshold2")
        sizePolicy2.setHeightForWidth(self.sliderCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.sliderCannyThreshold2.setSizePolicy(sizePolicy2)
        self.sliderCannyThreshold2.setMaximum(255)
        self.sliderCannyThreshold2.setValue(150)
        self.sliderCannyThreshold2.setOrientation(Qt.Orientation.Horizontal)

        self.layoutCannyThreshold2.addWidget(self.sliderCannyThreshold2)

        self.spinboxCannyThreshold2 = QSpinBox(self.group3Canny)
        self.spinboxCannyThreshold2.setObjectName("spinboxCannyThreshold2")
        sizePolicy3.setHeightForWidth(self.spinboxCannyThreshold2.sizePolicy().hasHeightForWidth())
        self.spinboxCannyThreshold2.setSizePolicy(sizePolicy3)
        self.spinboxCannyThreshold2.setMaximum(255)
        self.spinboxCannyThreshold2.setValue(150)

        self.layoutCannyThreshold2.addWidget(self.spinboxCannyThreshold2)


        self.layoutCanny.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutCannyThreshold2)

        self.spinboxCannyApertureSize = QSpinBox(self.group3Canny)
        self.spinboxCannyApertureSize.setObjectName("spinboxCannyApertureSize")
        self.spinboxCannyApertureSize.setMinimum(3)
        self.spinboxCannyApertureSize.setMaximum(7)
        self.spinboxCannyApertureSize.setSingleStep(2)

        self.layoutCanny.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spinboxCannyApertureSize)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group3Canny, 3, 0, 1, 1)

        self.group2Threshold = QGroupBox(self.scrollAreaWidgetContents)
        self.group2Threshold.setObjectName("group2Threshold")
        self.formLayout = QFormLayout(self.group2Threshold)
        self.formLayout.setObjectName("formLayout")
        self.labelThresholdingMethod = QLabel(self.group2Threshold)
        self.labelThresholdingMethod.setObjectName("labelThresholdingMethod")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelThresholdingMethod)

        self.comboboxThresholdingMethod = QComboBox(self.group2Threshold)
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.addItem("")
        self.comboboxThresholdingMethod.setObjectName("comboboxThresholdingMethod")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboboxThresholdingMethod)

        self.labelThresholdingThreshold = QLabel(self.group2Threshold)
        self.labelThresholdingThreshold.setObjectName("labelThresholdingThreshold")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelThresholdingThreshold)

        self.labelThresholdingMaximum = QLabel(self.group2Threshold)
        self.labelThresholdingMaximum.setObjectName("labelThresholdingMaximum")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelThresholdingMaximum)

        self.labelThresholdingBlockSize = QLabel(self.group2Threshold)
        self.labelThresholdingBlockSize.setObjectName("labelThresholdingBlockSize")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelThresholdingBlockSize)

        self.labelThresholdingC = QLabel(self.group2Threshold)
        self.labelThresholdingC.setObjectName("labelThresholdingC")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelThresholdingC)

        self.labelThresholdingOtsu = QLabel(self.group2Threshold)
        self.labelThresholdingOtsu.setObjectName("labelThresholdingOtsu")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelThresholdingOtsu)

        self.checkboxThresholdingOtsu = QCheckBox(self.group2Threshold)
        self.checkboxThresholdingOtsu.setObjectName("checkboxThresholdingOtsu")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.checkboxThresholdingOtsu)

        self.layoutThresholdingThreshold = QHBoxLayout()
        self.layoutThresholdingThreshold.setObjectName("layoutThresholdingThreshold")
        self.sliderThresholdingThreshold = QSlider(self.group2Threshold)
        self.sliderThresholdingThreshold.setObjectName("sliderThresholdingThreshold")
        sizePolicy2.setHeightForWidth(self.sliderThresholdingThreshold.sizePolicy().hasHeightForWidth())
        self.sliderThresholdingThreshold.setSizePolicy(sizePolicy2)
        self.sliderThresholdingThreshold.setMaximum(255)
        self.sliderThresholdingThreshold.setValue(127)
        self.sliderThresholdingThreshold.setOrientation(Qt.Orientation.Horizontal)

        self.layoutThresholdingThreshold.addWidget(self.sliderThresholdingThreshold)

        self.spinboxThresholdingThreshold = QSpinBox(self.group2Threshold)
        self.spinboxThresholdingThreshold.setObjectName("spinboxThresholdingThreshold")
        sizePolicy3.setHeightForWidth(self.spinboxThresholdingThreshold.sizePolicy().hasHeightForWidth())
        self.spinboxThresholdingThreshold.setSizePolicy(sizePolicy3)
        self.spinboxThresholdingThreshold.setMaximum(255)
        self.spinboxThresholdingThreshold.setValue(127)

        self.layoutThresholdingThreshold.addWidget(self.spinboxThresholdingThreshold)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.layoutThresholdingThreshold)

        self.layoutThresholdingMaximum = QHBoxLayout()
        self.layoutThresholdingMaximum.setObjectName("layoutThresholdingMaximum")
        self.sliderThresholdingMaximum = QSlider(self.group2Threshold)
        self.sliderThresholdingMaximum.setObjectName("sliderThresholdingMaximum")
        sizePolicy2.setHeightForWidth(self.sliderThresholdingMaximum.sizePolicy().hasHeightForWidth())
        self.sliderThresholdingMaximum.setSizePolicy(sizePolicy2)
        self.sliderThresholdingMaximum.setMaximum(255)
        self.sliderThresholdingMaximum.setValue(255)
        self.sliderThresholdingMaximum.setOrientation(Qt.Orientation.Horizontal)

        self.layoutThresholdingMaximum.addWidget(self.sliderThresholdingMaximum)

        self.spinboxThresholdingMaximum = QSpinBox(self.group2Threshold)
        self.spinboxThresholdingMaximum.setObjectName("spinboxThresholdingMaximum")
        sizePolicy3.setHeightForWidth(self.spinboxThresholdingMaximum.sizePolicy().hasHeightForWidth())
        self.spinboxThresholdingMaximum.setSizePolicy(sizePolicy3)
        self.spinboxThresholdingMaximum.setMaximum(255)
        self.spinboxThresholdingMaximum.setValue(255)

        self.layoutThresholdingMaximum.addWidget(self.spinboxThresholdingMaximum)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutThresholdingMaximum)

        self.sliderThresholdingBlockSize = QSlider(self.group2Threshold)
        self.sliderThresholdingBlockSize.setObjectName("sliderThresholdingBlockSize")
        self.sliderThresholdingBlockSize.setMinimum(1)
        self.sliderThresholdingBlockSize.setSingleStep(2)
        self.sliderThresholdingBlockSize.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.sliderThresholdingBlockSize)

        self.spinboxThresholdingC = QDoubleSpinBox(self.group2Threshold)
        self.spinboxThresholdingC.setObjectName("spinboxThresholdingC")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spinboxThresholdingC)


        self.layoutScrollAreaPropertiesDock.addWidget(self.group2Threshold, 2, 0, 1, 1)

        self.scrollareaPropertiesDock.setWidget(self.scrollAreaWidgetContents)

        self.layoutPropertiesDock.addWidget(self.scrollareaPropertiesDock, 0, 0, 1, 1)

        PropertiesDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(PropertiesDock)

        QMetaObject.connectSlotsByName(PropertiesDock)
    # setupUi

    def retranslateUi(self, PropertiesDock):
        PropertiesDock.setWindowTitle(QCoreApplication.translate("PropertiesDock", "Properties", None))
        self.group0Downscale.setTitle(QCoreApplication.translate("PropertiesDock", "Downscale", None))
        self.labelDownscaleMaxSize.setText(QCoreApplication.translate("PropertiesDock", "Max Size", None))
        self.spinboxDownscaleMaxSize.setSuffix(QCoreApplication.translate("PropertiesDock", " px", None))
        self.labelDownscaleEnabled.setText(QCoreApplication.translate("PropertiesDock", "Enabled", None))
        self.checkboxDownscaleEnabled.setText("")
        self.group1Blur.setTitle(QCoreApplication.translate("PropertiesDock", "Gaussian Blur", None))
        self.labelBlurEnabled.setText(QCoreApplication.translate("PropertiesDock", "Enabled", None))
        self.labelBlurKernelSize.setText(QCoreApplication.translate("PropertiesDock", "Kernel size", None))
        self.spinboxBlurKernelSize.setSuffix(QCoreApplication.translate("PropertiesDock", " px", None))
        self.checkboxBlurEnabled.setText("")
        self.group3Canny.setTitle(QCoreApplication.translate("PropertiesDock", "Canny", None))
        self.labelCannyEnabled.setText(QCoreApplication.translate("PropertiesDock", "Enabled", None))
        self.checkboxCannyEnabled.setText("")
        self.labelCannyThreshold1.setText(QCoreApplication.translate("PropertiesDock", "Threshold 1", None))
        self.labelCannyThreshold2.setText(QCoreApplication.translate("PropertiesDock", "Threshold 2", None))
        self.labelCannyApertureSize.setText(QCoreApplication.translate("PropertiesDock", "Aperture size", None))
        self.spinboxCannyApertureSize.setSuffix(QCoreApplication.translate("PropertiesDock", " px", None))
        self.group2Threshold.setTitle(QCoreApplication.translate("PropertiesDock", "Thresholding", None))
        self.labelThresholdingMethod.setText(QCoreApplication.translate("PropertiesDock", "Method", None))
        self.comboboxThresholdingMethod.setItemText(0, QCoreApplication.translate("PropertiesDock", "None", None))
        self.comboboxThresholdingMethod.setItemText(1, QCoreApplication.translate("PropertiesDock", "Binary", None))
        self.comboboxThresholdingMethod.setItemText(2, QCoreApplication.translate("PropertiesDock", "Binary Inverse", None))
        self.comboboxThresholdingMethod.setItemText(3, QCoreApplication.translate("PropertiesDock", "Truncate", None))
        self.comboboxThresholdingMethod.setItemText(4, QCoreApplication.translate("PropertiesDock", "To Zero", None))
        self.comboboxThresholdingMethod.setItemText(5, QCoreApplication.translate("PropertiesDock", "To Zero Inverse", None))
        self.comboboxThresholdingMethod.setItemText(6, QCoreApplication.translate("PropertiesDock", "Mean", None))
        self.comboboxThresholdingMethod.setItemText(7, QCoreApplication.translate("PropertiesDock", "Gaussian", None))

        self.labelThresholdingThreshold.setText(QCoreApplication.translate("PropertiesDock", "Threshold", None))
        self.labelThresholdingMaximum.setText(QCoreApplication.translate("PropertiesDock", "Maximum", None))
        self.labelThresholdingBlockSize.setText(QCoreApplication.translate("PropertiesDock", "Block size", None))
        self.labelThresholdingC.setText(QCoreApplication.translate("PropertiesDock", "C", None))
        self.labelThresholdingOtsu.setText(QCoreApplication.translate("PropertiesDock", "Otsu", None))
        self.checkboxThresholdingOtsu.setText("")
    # retranslateUi

