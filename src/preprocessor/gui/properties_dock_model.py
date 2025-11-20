from PySide6.QtCore import QObject, Signal

from preprocessor.processing.params import (
    ThresholdingMethod,
    QuadratDetectionParams,
    DownscaleParams,
    BlurParams,
    ThresholdingParams,
    CannyParams,
    ContourApproximationMethod,
    FindContourParams, HoughParams,
)


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

    _thresholding_inverse: bool = False
    on_thresholding_inverse_changed: Signal = Signal(bool)

    @property
    def thresholding_inverse(self) -> bool:
        return self._thresholding_inverse

    @thresholding_inverse.setter
    def thresholding_inverse(self, value: bool) -> None:
        if self._thresholding_inverse != value:
            self.on_thresholding_inverse_changed.emit(value)
            self.on_changed.emit()
            self._thresholding_inverse = value

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

    #########
    # Hough #
    #########

    _hough_enabled: bool = False
    on_hough_enabled_changed: Signal = Signal(bool)

    @property
    def hough_enabled(self) -> bool:
        return self._hough_enabled

    @hough_enabled.setter
    def hough_enabled(self, value: bool) -> None:
        if self._hough_enabled != value:
            self.on_hough_enabled_changed.emit(value)
            self.on_changed.emit()
            self._hough_enabled = value

    _hough_probabilistic: bool = False
    on_hough_probabilistic_changed: Signal = Signal(bool)

    @property
    def hough_probabilistic(self) -> bool:
        return self._hough_probabilistic

    @hough_probabilistic.setter
    def hough_probabilistic(self, value: bool) -> None:
        if self._hough_probabilistic != value:
            self.on_hough_probabilistic_changed.emit(value)
            self.on_changed.emit()
            self._hough_probabilistic = value

    _hough_rho: int = 1
    on_hough_rho_changed: Signal = Signal(int)

    @property
    def hough_rho(self) -> int:
        return self._hough_rho

    @hough_rho.setter
    def hough_rho(self, value: int) -> None:
        if self._hough_rho != value:
            self.on_hough_rho_changed.emit(value)
            self.on_changed.emit()
            self._hough_rho = value

    _hough_theta: float = 1.0
    on_hough_theta_changed: Signal = Signal(float)

    @property
    def hough_theta(self) -> float:
        return self._hough_theta

    @hough_theta.setter
    def hough_theta(self, value: float) -> None:
        if self._hough_theta != value:
            self.on_hough_theta_changed.emit(value)
            self.on_changed.emit()
            self._hough_theta = value

    _hough_threshold: int = 100
    on_hough_threshold_changed: Signal = Signal(int)

    @property
    def hough_threshold(self) -> int:
        return self._hough_threshold

    @hough_threshold.setter
    def hough_threshold(self, value: int) -> None:
        if self._hough_threshold != value:
            self.on_hough_threshold_changed.emit(value)
            self.on_changed.emit()
            self._hough_threshold = value

    _hough_srn: float = 0.0
    on_hough_srn_changed: Signal = Signal(float)

    @property
    def hough_srn(self) -> float:
        return self._hough_srn

    @hough_srn.setter
    def hough_srn(self, value: float) -> None:
        if self._hough_srn != value:
            self.on_hough_srn_changed.emit(value)
            self.on_changed.emit()
            self._hough_srn = value

    _hough_stn: float = 0.0
    on_hough_stn_changed: Signal = Signal(float)

    @property
    def hough_stn(self) -> float:
        return self._hough_stn

    @hough_stn.setter
    def hough_stn(self, value: float) -> None:
        if self._hough_stn != value:
            self.on_hough_stn_changed.emit(value)
            self.on_changed.emit()
            self._hough_stn = value

    _hough_min_theta: float = 0.0
    on_hough_min_theta_changed: Signal = Signal(float)

    @property
    def hough_min_theta(self) -> float:
        return self._hough_min_theta

    @hough_min_theta.setter
    def hough_min_theta(self, value: float) -> None:
        if self._hough_min_theta != value:
            self.on_hough_min_theta_changed.emit(value)
            self.on_changed.emit()
            self._hough_min_theta = value

    _hough_max_theta: float = 180.0
    on_hough_max_theta_changed: Signal = Signal(float)

    @property
    def hough_max_theta(self) -> float:
        return self._hough_max_theta

    @hough_max_theta.setter
    def hough_max_theta(self, value: float) -> None:
        if self._hough_max_theta != value:
            self.on_hough_max_theta_changed.emit(value)
            self.on_changed.emit()
            self._hough_max_theta = value

    _hough_min_line_length: int = 0
    on_hough_min_line_length_changed: Signal = Signal(int)

    @property
    def hough_min_line_length(self) -> int:
        return self._hough_min_line_length

    @hough_min_line_length.setter
    def hough_min_line_length(self, value: int) -> None:
        if self._hough_min_line_length != value:
            self.on_hough_min_line_length_changed.emit(value)
            self.on_changed.emit()
            self._hough_min_line_length = value

    _hough_max_line_gap: int = 0
    on_hough_max_line_gap_changed: Signal = Signal(int)

    @property
    def hough_max_line_gap(self) -> int:
        return self._hough_max_line_gap

    @hough_max_line_gap.setter
    def hough_max_line_gap(self, value: int) -> None:
        if self._hough_max_line_gap != value:
            self.on_hough_max_line_gap_changed.emit(value)
            self.on_changed.emit()
            self._hough_max_line_gap = value


    #################
    # Find Contours #
    #################
    _find_contour_enabled: bool = False
    on_find_contour_enabled_changed: Signal = Signal(bool)

    @property
    def find_contour_enabled(self) -> bool:
        return self._find_contour_enabled

    @find_contour_enabled.setter
    def find_contour_enabled(self, value: bool) -> None:
        if self._find_contour_enabled != value:
            self.on_find_contour_enabled_changed.emit(value)
            self.on_changed.emit()
            self._find_contour_enabled = value

    _find_contour_method: ContourApproximationMethod = ContourApproximationMethod.SIMPLE
    on_find_contour_method_changed: Signal = Signal(ContourApproximationMethod)

    @property
    def find_contour_method(self) -> ContourApproximationMethod:
        return self._find_contour_method

    @find_contour_method.setter
    def find_contour_method(self, value: ContourApproximationMethod) -> None:
        if self._find_contour_method != value:
            self.on_find_contour_method_changed.emit(value)
            self.on_changed.emit()
            self._find_contour_method = value

    @property
    def params(self) -> QuadratDetectionParams:
        return QuadratDetectionParams(
            downscale=DownscaleParams(
                enabled=self.downscale_enabled,
                max_size=self.downscale_max_size,
            ),
            blur=BlurParams(
                enabled=self.blur_enabled,
                kernel_size=self.blur_kernel_size,
            ),
            thresholding=ThresholdingParams(
                method=self.thresholding_method,
                inverse=self.thresholding_inverse,
                threshold=self.thresholding_threshold,
                maximum=self.thresholding_maximum,
                block_size=self.thresholding_block_size,
                C=self.thresholding_C,
                otsu_enabled=self.thresholding_otsu_enabled,
            ),
            canny=CannyParams(
                enabled=self.canny_enabled,
                threshold1=self.canny_threshold1,
                threshold2=self.canny_threshold2,
                aperture_size=self.canny_aperture_size,
            ),
            hough=HoughParams(
                enabled=self.hough_enabled,
                probabilistic=self.hough_probabilistic,
                rho=self.hough_rho,
                theta=self.hough_theta,
                threshold=self.hough_threshold,
                srn=self.hough_srn,
                stn=self.hough_stn,
                min_theta=self.hough_min_theta,
                max_theta=self.hough_max_theta,
                min_line_length=self.hough_min_line_length,
                max_line_gap=self.hough_max_line_gap,
            ),
            findContour=FindContourParams(
                enabled=self.find_contour_enabled,
                method=self.find_contour_method,
            ),
        )

    @params.setter
    def params(self, value: QuadratDetectionParams) -> None:
        self.downscale_enabled = value.downscale.enabled
        self.downscale_max_size = value.downscale.max_size

        self.blur_enabled = value.blur.enabled
        self.blur_kernel_size = value.blur.kernel_size

        self.thresholding_method = value.thresholding.method
        self.thresholding_inverse = value.thresholding.inverse
        self.thresholding_threshold = value.thresholding.threshold
        self.thresholding_maximum = value.thresholding.maximum
        self.thresholding_block_size = value.thresholding.block_size
        self.thresholding_C = value.thresholding.C
        self.thresholding_otsu_enabled = value.thresholding.otsu_enabled

        self.canny_enabled = value.canny.enabled
        self.canny_threshold1 = value.canny.threshold1
        self.canny_threshold2 = value.canny.threshold2
        self.canny_aperture_size = value.canny.aperture_size

        self.hough_enabled = value.hough.enabled
        self.hough_probabilistic = value.hough.probabilistic
        self.hough_rho = value.hough.rho
        self.hough_theta = value.hough.theta
        self.hough_threshold = value.hough.threshold
        self.hough_srn = value.hough.srn
        self.hough_stn = value.hough.stn
        self.hough_min_theta = value.hough.min_theta
        self.hough_max_theta = value.hough.max_theta
        self.hough_min_line_length = value.hough.min_line_length
        self.hough_max_line_gap = value.hough.max_line_gap

        self.find_contour_enabled = value.findContour.enabled
        self.find_contour_method = value.findContour.method
