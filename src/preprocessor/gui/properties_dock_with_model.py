from PySide6.QtWidgets import QDockWidget, QWidget

from preprocessor.gui.ui_properties_dock import Ui_PropertiesDock
from preprocessor.gui.properties_dock_model import PropertiesDockModel
from preprocessor.processing.params import ThresholdingMethod, defaultParams, ContourApproximationMethod


class PropertiesDockWidget(QDockWidget):
    # ui: Ui_PropertiesDock
    model: PropertiesDockModel

    def __init__(self, parent: QWidget | None = None) -> None:
        QDockWidget.__init__(self, parent)
        self.ui = Ui_PropertiesDock()
        self.ui.setupUi(self)

        self.model = PropertiesDockModel()
        self._connect_signals()
        self.model.params = defaultParams

    def _connect_signals(self) -> None:
        # NOTE: Surely there is a way to avoid all this boilerplate...

        # Downscale
        self.ui.checkboxDownscaleEnabled.stateChanged.connect(
            lambda value: setattr(self.model, "downscale_enabled", value)
        )
        self.model.on_downscale_enabled_changed.connect(self.ui.checkboxDownscaleEnabled.setChecked)

        self.ui.spinboxDownscaleMaxSize.valueChanged.connect(
            lambda value: setattr(self.model, "downscale_max_size", value)
        )
        self.model.on_downscale_max_size_changed.connect(self.ui.spinboxDownscaleMaxSize.setValue)

        # Blur
        self.ui.checkboxBlurEnabled.stateChanged.connect(lambda value: setattr(self.model, "blur_enabled", value))
        self.model.on_blur_enabled_changed.connect(self.ui.checkboxBlurEnabled.setChecked)

        self.ui.spinboxBlurKernelSize.valueChanged.connect(lambda value: setattr(self.model, "blur_kernel_size", value))
        self.model.on_blur_kernel_size_changed.connect(self.ui.spinboxBlurKernelSize.setValue)

        # Thresholding
        def on_comboboxThresholdingMethod_changed(i: int) -> None:
            method_str = self.ui.comboboxThresholdingMethod.itemText(i)
            method = ThresholdingMethod.from_string(method_str)
            self.model.thresholding_method = method

        self.ui.comboboxThresholdingMethod.currentIndexChanged.connect(on_comboboxThresholdingMethod_changed)

        def on_thresholding_method_changed(method: ThresholdingMethod) -> None:
            self.ui.comboboxThresholdingMethod.setCurrentText(method.value)
            self.ui.checkboxThresholdingInverse.setEnabled(
                method != ThresholdingMethod.NONE and method != ThresholdingMethod.TRUNC
            )
            self.ui.sliderThresholdingThreshold.setEnabled(method != ThresholdingMethod.NONE)
            self.ui.spinboxThresholdingThreshold.setEnabled(method != ThresholdingMethod.NONE)
            self.ui.sliderThresholdingMaximum.setEnabled(
                method == ThresholdingMethod.BINARY
                or method == ThresholdingMethod.MEAN
                or method == ThresholdingMethod.GAUSSIAN
            )
            self.ui.spinboxThresholdingMaximum.setEnabled(
                method == ThresholdingMethod.BINARY
                or method == ThresholdingMethod.MEAN
                or method == ThresholdingMethod.GAUSSIAN
            )
            self.ui.sliderThresholdingBlockSize.setEnabled(
                method == ThresholdingMethod.MEAN or method == ThresholdingMethod.GAUSSIAN
            )
            self.ui.spinboxThresholdingC.setEnabled(
                method == ThresholdingMethod.MEAN or method == ThresholdingMethod.GAUSSIAN
            )
            self.ui.checkboxThresholdingOtsu.setEnabled(
                method != ThresholdingMethod.NONE
                and method != ThresholdingMethod.MEAN
                and method != ThresholdingMethod.GAUSSIAN
            )

        self.model.on_thresholding_method_changed.connect(on_thresholding_method_changed)

        self.ui.checkboxThresholdingInverse.stateChanged.connect(
            lambda value: setattr(self.model, "thresholding_inverse", value)
        )
        self.model.on_thresholding_inverse_changed.connect(self.ui.checkboxThresholdingInverse.setChecked)

        self.ui.sliderThresholdingThreshold.valueChanged.connect(
            lambda value: setattr(self.model, "thresholding_threshold", value)
        )
        self.model.on_thresholding_threshold_changed.connect(self.ui.sliderThresholdingThreshold.setValue)
        self.ui.spinboxThresholdingThreshold.valueChanged.connect(
            lambda value: setattr(self.model, "thresholding_threshold", value)
        )
        self.model.on_thresholding_threshold_changed.connect(self.ui.spinboxThresholdingThreshold.setValue)

        self.ui.sliderThresholdingMaximum.valueChanged.connect(
            lambda value: setattr(self.model, "thresholding_maximum", value)
        )
        self.model.on_thresholding_maximum_changed.connect(self.ui.sliderThresholdingMaximum.setValue)
        self.ui.spinboxThresholdingMaximum.valueChanged.connect(
            lambda value: setattr(self.model, "thresholding_maximum", value)
        )
        self.model.on_thresholding_maximum_changed.connect(self.ui.spinboxThresholdingMaximum.setValue)

        self.ui.sliderThresholdingBlockSize.valueChanged.connect(
            lambda value: setattr(self.model, "thresholding_block_size", value)
        )
        self.model.on_thresholding_block_size_changed.connect(self.ui.sliderThresholdingBlockSize.setValue)

        self.ui.spinboxThresholdingC.valueChanged.connect(lambda value: setattr(self.model, "thresholding_C", value))
        self.model.on_thresholding_C_changed.connect(self.ui.spinboxThresholdingC.setValue)

        self.ui.checkboxThresholdingOtsu.stateChanged.connect(
            lambda value: setattr(self.model, "thresholding_otsu_enabled", value)
        )
        self.model.on_thresholding_otsu_enabled_changed.connect(self.ui.checkboxThresholdingOtsu.setChecked)

        # Canny

        self.ui.checkboxCannyEnabled.stateChanged.connect(lambda value: setattr(self.model, "canny_enabled", value))
        self.model.on_canny_enabled_changed.connect(self.ui.checkboxCannyEnabled.setChecked)

        self.ui.sliderCannyThreshold1.valueChanged.connect(lambda value: setattr(self.model, "canny_threshold1", value))
        self.model.on_canny_threshold1_changed.connect(self.ui.sliderCannyThreshold1.setValue)
        self.ui.spinboxCannyThreshold1.valueChanged.connect(
            lambda value: setattr(self.model, "canny_threshold1", value)
        )
        self.model.on_canny_threshold1_changed.connect(self.ui.spinboxCannyThreshold1.setValue)

        self.ui.sliderCannyThreshold2.valueChanged.connect(lambda value: setattr(self.model, "canny_threshold2", value))
        self.model.on_canny_threshold2_changed.connect(self.ui.sliderCannyThreshold2.setValue)
        self.ui.spinboxCannyThreshold2.valueChanged.connect(
            lambda value: setattr(self.model, "canny_threshold2", value)
        )
        self.model.on_canny_threshold2_changed.connect(self.ui.spinboxCannyThreshold2.setValue)

        self.ui.spinboxCannyApertureSize.valueChanged.connect(
            lambda value: setattr(self.model, "canny_aperture_size", value)
        )
        self.model.on_canny_aperture_size_changed.connect(self.ui.spinboxCannyApertureSize.setValue)

        # Find Contours
        self.ui.checkboxFindContourEnabled.stateChanged.connect(
            lambda value: setattr(self.model, "find_contour_enabled", value)
        )
        self.model.on_find_contour_enabled_changed.connect(self.ui.checkboxFindContourEnabled.setChecked)

        def on_comboboxFindContourMethod_changed(i: int) -> None:
            method_str = self.ui.comboboxFindContourMethod.itemText(i)
            method = ContourApproximationMethod.from_string(method_str)
            self.model.find_contour_method = method

        self.ui.comboboxFindContourMethod.currentIndexChanged.connect(on_comboboxFindContourMethod_changed)
        self.model.on_find_contour_method_changed.connect(
            lambda method: self.ui.comboboxFindContourMethod.setCurrentText(method)
        )

    def _trigger_initial_updates(self) -> None:
        # Downscale
        self.model.on_downscale_enabled_changed.emit(self.model.downscale_enabled)
        self.model.on_downscale_max_size_changed.emit(self.model.downscale_max_size)

        # Blur
        self.model.on_blur_enabled_changed.emit(self.model.blur_enabled)
        self.model.on_blur_kernel_size_changed.emit(self.model.blur_kernel_size)

        # Thresholding
        self.model.on_thresholding_method_changed.emit(self.model.thresholding_method)
        self.model.on_thresholding_inverse_changed.emit(self.model.thresholding_inverse)
        self.model.on_thresholding_threshold_changed.emit(self.model.thresholding_threshold)
        self.model.on_thresholding_maximum_changed.emit(self.model.thresholding_maximum)
        self.model.on_thresholding_block_size_changed.emit(self.model.thresholding_block_size)
        self.model.on_thresholding_C_changed.emit(self.model.thresholding_C)
        self.model.on_thresholding_otsu_enabled_changed.emit(self.model.thresholding_otsu_enabled)

        # Canny
        self.model.on_canny_enabled_changed.emit(self.model.canny_enabled)
        self.model.on_canny_threshold1_changed.emit(self.model.canny_threshold1)
        self.model.on_canny_threshold2_changed.emit(self.model.canny_threshold2)
        self.model.on_canny_aperture_size_changed.emit(self.model.canny_aperture_size)

        # Overall
        self.model.on_changed.emit()
