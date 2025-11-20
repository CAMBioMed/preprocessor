from PySide6.QtCore import QObject, Signal

from preprocessor.processing.params import ThresholdingMethod, QuadratDetectionParams


# NOTE: There must be a way in Python to avoid most of this boilerplate...

class PropertiesDockModel(QObject):

    on_changed: Signal = Signal()

    #############
    # Downscale #
    #############

    _downscale_enabled: bool = True
    on_downscale_enabled_changed: Signal = Signal(bool)

    @property
    def downscale_enabled(self) -> bool:
        return self._downscale_enabled

    @downscale_enabled.setter
    def downscale_enabled(self, value: bool) -> None:
        if self._downscale_enabled != value:
            self.on_downscale_enabled_changed.emit(value)
            self.on_changed.emit()
            self._downscale_enabled = value

    _downscale_max_size: int = 800
    on_downscale_max_size_changed: Signal = Signal(int)

    @property
    def downscale_max_size(self) -> int:
        return self._downscale_max_size

    @downscale_max_size.setter
    def downscale_max_size(self, value: int) -> None:
        if self._downscale_max_size != value:
            self.on_downscale_max_size_changed.emit(value)
            self.on_changed.emit()
            self._downscale_max_size = value

    ########
    # Blur #
    ########

    _blur_enabled: bool = False
    on_blur_enabled_changed: Signal = Signal(bool)

    @property
    def blur_enabled(self) -> bool:
        return self._blur_enabled

    @blur_enabled.setter
    def blur_enabled(self, value: bool) -> None:
        if self._blur_enabled != value:
            self.on_blur_enabled_changed.emit(value)
            self.on_changed.emit()
            self._blur_enabled = value

    _blur_kernel_size: int = 5
    on_blur_kernel_size_changed: Signal = Signal(int)

    @property
    def blur_kernel_size(self) -> int:
        return self._blur_kernel_size

    @blur_kernel_size.setter
    def blur_kernel_size(self, value: int) -> None:
        if self._blur_kernel_size != value:
            self.on_blur_kernel_size_changed.emit(value)
            self.on_changed.emit()
            self._blur_kernel_size = value

    ################
    # Thresholding #
    ################
    _thresholding_method: ThresholdingMethod = ThresholdingMethod.NONE
    on_thresholding_method_changed: Signal = Signal(ThresholdingMethod)

    @property
    def thresholding_method(self) -> ThresholdingMethod:
        return self._thresholding_method

    @thresholding_method.setter
    def thresholding_method(self, value: ThresholdingMethod) -> None:
        if self._thresholding_method != value:
            self.on_thresholding_method_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_method = value

    _thresholding_threshold: int = 127
    on_thresholding_threshold_changed: Signal = Signal(int)

    @property
    def thresholding_threshold(self) -> int:
        return self._thresholding_threshold

    @thresholding_threshold.setter
    def thresholding_threshold(self, value: int) -> None:
        if self._thresholding_threshold != value:
            self.on_thresholding_threshold_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_threshold = value

    _thresholding_maximum: int = 255
    on_thresholding_maximum_changed: Signal = Signal(int)

    @property
    def thresholding_maximum(self) -> int:
        return self._thresholding_maximum

    @thresholding_maximum.setter
    def thresholding_maximum(self, value: int) -> None:
        if self._thresholding_maximum != value:
            self.on_thresholding_maximum_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_maximum = value

    _thresholding_block_size: int = 3
    on_thresholding_block_size_changed: Signal = Signal(int)

    @property
    def thresholding_block_size(self) -> int:
        return self._thresholding_block_size

    @thresholding_block_size.setter
    def thresholding_block_size(self, value: int) -> None:
        if self._thresholding_block_size != value:
            self.on_thresholding_block_size_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_block_size = value

    _thresholding_C: float = 5.0
    on_thresholding_C_changed: Signal = Signal(float)

    @property
    def thresholding_C(self) -> float:
        return self._thresholding_C

    @thresholding_C.setter
    def thresholding_C(self, value: float) -> None:
        if self._thresholding_C != value:
            self.on_thresholding_C_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_C = value

    _thresholding_otsu_enabled: bool = False
    on_thresholding_otsu_enabled_changed: Signal = Signal(bool)

    @property
    def thresholding_otsu_enabled(self) -> bool:
        return self._thresholding_otsu_enabled

    @thresholding_otsu_enabled.setter
    def thresholding_otsu_enabled(self, value: bool) -> None:
        if self._thresholding_otsu_enabled != value:
            self.on_thresholding_otsu_enabled_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_otsu_enabled = value

    #########
    # Canny #
    #########
    _canny_enabled: bool = True
    on_canny_enabled_changed: Signal = Signal(bool)

    @property
    def canny_enabled(self) -> bool:
        return self._canny_enabled

    @canny_enabled.setter
    def canny_enabled(self, value: bool) -> None:
        if self._canny_enabled != value:
            self.on_canny_enabled_changed.emit(value)
            self.on_changed.emit()
            self._canny_enabled = value

    _canny_threshold1: int = 50
    on_canny_threshold1_changed: Signal = Signal(int)

    @property
    def canny_threshold1(self) -> int:
        return self._canny_threshold1

    @canny_threshold1.setter
    def canny_threshold1(self, value: int) -> None:
        if self._canny_threshold1 != value:
            self.on_canny_threshold1_changed.emit(value)
            self.on_changed.emit()
            self._canny_threshold1 = value

    _canny_threshold2: int = 150
    on_canny_threshold2_changed: Signal = Signal(int)

    @property
    def canny_threshold2(self) -> int:
        return self._canny_threshold2

    @canny_threshold2.setter
    def canny_threshold2(self, value: int) -> None:
        if self._canny_threshold2 != value:
            self.on_canny_threshold2_changed.emit(value)
            self.on_changed.emit()
            self._canny_threshold2 = value

    _canny_aperture_size: int = 3
    on_canny_aperture_size_changed: Signal = Signal(int)

    @property
    def canny_aperture_size(self) -> int:
        return self._canny_aperture_size

    @canny_aperture_size.setter
    def canny_aperture_size(self, value: int) -> None:
        if self._canny_aperture_size != value:
            self.on_canny_aperture_size_changed.emit(value)
            self.on_changed.emit()
            self._canny_aperture_size = value

    @property
    def params(self) -> QuadratDetectionParams:
        return QuadratDetectionParams(
            # Downscale
            downscale_enabled = self._downscale_enabled,
            downscale_max_size = self._downscale_max_size,
            # Blur
            blur_enabled = self._blur_enabled,
            blur_kernel_size = self._blur_kernel_size,
            # Thresholding
            thresholding_method = self._thresholding_method,
            thresholding_threshold = self._thresholding_threshold,
            thresholding_maximum = self._thresholding_maximum,
            thresholding_block_size = self._thresholding_block_size,
            thresholding_C = self._thresholding_C,
            thresholding_otsu_enabled = self._thresholding_otsu_enabled,
            # Canny
            canny_enabled = self._canny_enabled,
            canny_threshold1 = self._canny_threshold1,
            canny_threshold2 = self._canny_threshold2,
            canny_aperture_size = self._canny_aperture_size,
        )

    @params.setter
    def params(self, value: QuadratDetectionParams) -> None:
        self.downscale_enabled = value.downscale_enabled
        self.downscale_max_size = value.downscale_max_size
        self.blur_enabled = value.blur_enabled
        self.blur_kernel_size = value.blur_kernel_size
        self.thresholding_method = value.thresholding_method
        self.thresholding_threshold = value.thresholding_threshold
        self.thresholding_maximum = value.thresholding_maximum
        self.thresholding_block_size = value.thresholding_block_size
        self.thresholding_C = value.thresholding_C
        self.thresholding_otsu_enabled = value.thresholding_otsu_enabled
        self.canny_enabled = value.canny_enabled
        self.canny_threshold1 = value.canny_threshold1
        self.canny_threshold2 = value.canny_threshold2
        self.canny_aperture_size = value.canny_aperture_size
