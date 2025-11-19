from PySide6.QtWidgets import QDockWidget

from preprocessor.gui.properties_dock import Ui_PropertiesDock
from preprocessor.gui.properties_dock_model import PropertiesDockModel
from preprocessor.gui.quadrat_detection import ThresholdingMethod


class Ui_PropertiesDockWithModel(QDockWidget, Ui_PropertiesDock):

    model: PropertiesDockModel

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        Ui_PropertiesDock.__init__(self)
        self.setupUi(self)

    def setupUi(self, PropertiesDock):
        super().setupUi(PropertiesDock)

        self.model = PropertiesDockModel()
        self._connect_signals()
        self._trigger_initial_updates()

    def _connect_signals(self):
        # NOTE: Surely there is a way to avoid all this boilerplate...

        # Downscale
        self.checkboxDownscaleEnabled.stateChanged.connect(
            lambda value: setattr(self.model, 'downscale_enabled', value)
        )
        self.model.on_downscale_enabled_changed.connect(
            self.checkboxDownscaleEnabled.setChecked
        )

        self.spinboxDownscaleMaxSize.valueChanged.connect(
            lambda value: setattr(self.model, 'downscale_max_size', value)
        )
        self.model.on_downscale_max_size_changed.connect(
            self.spinboxDownscaleMaxSize.setValue
        )

        # Blur
        self.checkboxBlurEnabled.stateChanged.connect(
            lambda value: setattr(self.model, 'blur_enabled', value)
        )
        self.model.on_blur_enabled_changed.connect(
            self.checkboxBlurEnabled.setChecked
        )

        self.spinboxBlurKernelSize.valueChanged.connect(
            lambda value: setattr(self.model, 'blur_kernel_size', value)
        )
        self.model.on_blur_kernel_size_changed.connect(
            self.spinboxBlurKernelSize.setValue
        )

        # Thresholding
        def on_comboboxThresholdingMethod_changed(i: int):
            method_str = self.comboboxThresholdingMethod.itemText(i)
            method = ThresholdingMethod.from_string(method_str)
            setattr(self.model, 'thresholding_method', method)

        self.comboboxThresholdingMethod.currentIndexChanged.connect(on_comboboxThresholdingMethod_changed)

        def on_thresholding_method_changed(method: ThresholdingMethod):
            self.comboboxThresholdingMethod.setCurrentText(method.value)
            self.sliderThresholdingThreshold.setEnabled(
                method != ThresholdingMethod.NONE
            )
            self.spinboxThresholdingThreshold.setEnabled(
                method != ThresholdingMethod.NONE
            )
            self.sliderThresholdingMaximum.setEnabled(
                method != ThresholdingMethod.NONE
            )
            self.spinboxThresholdingMaximum.setEnabled(
                method != ThresholdingMethod.NONE
            )
            self.sliderThresholdingBlockSize.setEnabled(
                method == ThresholdingMethod.MEAN or
                method == ThresholdingMethod.GAUSSIAN
            )
            self.spinboxThresholdingC.setEnabled(
                method == ThresholdingMethod.MEAN or
                method == ThresholdingMethod.GAUSSIAN
            )
            self.checkboxThresholdingOtsu.setEnabled(
                method != ThresholdingMethod.NONE and
                method != ThresholdingMethod.MEAN and
                method != ThresholdingMethod.GAUSSIAN
            )

        self.model.on_thresholding_method_changed.connect(on_thresholding_method_changed)


        self.sliderThresholdingThreshold.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_threshold', value)
        )
        self.model.on_thresholding_threshold_changed.connect(
            self.sliderThresholdingThreshold.setValue
        )
        self.spinboxThresholdingThreshold.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_threshold', value)
        )
        self.model.on_thresholding_threshold_changed.connect(
            self.spinboxThresholdingThreshold.setValue
        )

        self.sliderThresholdingMaximum.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_maximum', value)
        )
        self.model.on_thresholding_maximum_changed.connect(
            self.sliderThresholdingMaximum.setValue
        )
        self.spinboxThresholdingMaximum.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_maximum', value)
        )
        self.model.on_thresholding_maximum_changed.connect(
            self.spinboxThresholdingMaximum.setValue
        )

        self.sliderThresholdingBlockSize.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_block_size', value)
        )
        self.model.on_thresholding_block_size_changed.connect(
            self.sliderThresholdingBlockSize.setValue
        )

        self.spinboxThresholdingC.valueChanged.connect(
            lambda value: setattr(self.model, 'thresholding_C', value)
        )
        self.model.on_thresholding_C_changed.connect(
            self.spinboxThresholdingC.setValue
        )

        self.checkboxThresholdingOtsu.stateChanged.connect(
            lambda value: setattr(self.model, 'thresholding_otsu_enabled', value)
        )
        self.model.on_thresholding_otsu_enabled_changed.connect(
            self.checkboxThresholdingOtsu.setChecked
        )

        # Canny

        self.checkboxCannyEnabled.stateChanged.connect(
            lambda value: setattr(self.model, 'canny_enabled', value)
        )
        self.model.on_canny_enabled_changed.connect(
            self.checkboxCannyEnabled.setChecked
        )

        self.sliderCannyThreshold1.valueChanged.connect(
            lambda value: setattr(self.model, 'canny_threshold1', value)
        )
        self.model.on_canny_threshold1_changed.connect(
            self.sliderCannyThreshold1.setValue
        )
        self.spinboxCannyThreshold1.valueChanged.connect(
            lambda value: setattr(self.model, 'canny_threshold1', value)
        )
        self.model.on_canny_threshold1_changed.connect(
            self.spinboxCannyThreshold1.setValue
        )

        self.sliderCannyThreshold2.valueChanged.connect(
            lambda value: setattr(self.model, 'canny_threshold2', value)
        )
        self.model.on_canny_threshold2_changed.connect(
            self.sliderCannyThreshold2.setValue
        )
        self.spinboxCannyThreshold2.valueChanged.connect(
            lambda value: setattr(self.model, 'canny_threshold2', value)
        )
        self.model.on_canny_threshold2_changed.connect(
            self.spinboxCannyThreshold2.setValue
        )

        self.spinboxCannyApertureSize.valueChanged.connect(
            lambda value: setattr(self.model, 'canny_aperture_size', value)
        )
        self.model.on_canny_aperture_size_changed.connect(
            self.spinboxCannyApertureSize.setValue
        )

    def _trigger_initial_updates(self):
        # Downscale
        self.model.on_downscale_enabled_changed.emit(
            self.model.downscale_enabled
        )
        self.model.on_downscale_max_size_changed.emit(
            self.model.downscale_max_size
        )

        # Blur
        self.model.on_blur_enabled_changed.emit(
            self.model.blur_enabled
        )
        self.model.on_blur_kernel_size_changed.emit(
            self.model.blur_kernel_size
        )

        # Thresholding
        self.model.on_thresholding_method_changed.emit(
            self.model.thresholding_method
        )
        self.model.on_thresholding_threshold_changed.emit(
            self.model.thresholding_threshold
        )
        self.model.on_thresholding_maximum_changed.emit(
            self.model.thresholding_maximum
        )
        self.model.on_thresholding_block_size_changed.emit(
            self.model.thresholding_block_size
        )
        self.model.on_thresholding_C_changed.emit(
            self.model.thresholding_C
        )
        self.model.on_thresholding_otsu_enabled_changed.emit(
            self.model.thresholding_otsu_enabled
        )

        # Canny
        self.model.on_canny_enabled_changed.emit(
            self.model.canny_enabled
        )
        self.model.on_canny_threshold1_changed.emit(
            self.model.canny_threshold1
        )
        self.model.on_canny_threshold2_changed.emit(
            self.model.canny_threshold2
        )
        self.model.on_canny_aperture_size_changed.emit(
            self.model.canny_aperture_size
        )

        # Overall
        self.model.on_changed.emit()