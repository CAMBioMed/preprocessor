from PySide6.QtCore import QObject, Signal

from preprocessor.gui.hsv_threshold_params import HSVThresholdParams
from dataclasses import replace


class HSVThresholdModel(QObject):
    # Signals have to be class attributes to satisfy MyPy
    on_changed: Signal = Signal()
    on_hue_min_changed: Signal = Signal(int)
    on_hue_max_changed: Signal = Signal(int)
    on_saturation_min_changed: Signal = Signal(int)
    on_saturation_max_changed: Signal = Signal(int)
    on_value_min_changed: Signal = Signal(int)
    on_value_max_changed: Signal = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        # Defaults
        self._params = HSVThresholdParams(
            hue_min=0,
            hue_max=179,
            saturation_min=0,
            saturation_max=255,
            value_min=0,
            value_max=255,
        )

    # We set the values on an instance of the dataclass
    # such that we trigger validation and adjustment logic

    @property
    def hue_min(self) -> int:
        return self.params.hue_min

    @hue_min.setter
    def hue_min(self, value: int) -> None:
        # if self._params.hue_min == value:
        #     return
        self.params = replace(self.params, hue_min=value)
        # self.on_hue_min_changed.emit(self._params.hue_min)
        # self.on_changed.emit()

    @property
    def hue_max(self) -> int:
        return self.params.hue_max

    @hue_max.setter
    def hue_max(self, value: int) -> None:
        # if self._params.hue_max == value:
        #     return
        self.params = replace(self.params, hue_max=value)
        # self.on_hue_max_changed.emit(self._params.hue_max)
        # self.on_changed.emit()

    @property
    def saturation_min(self) -> int:
        return self.params.saturation_min

    @saturation_min.setter
    def saturation_min(self, value: int) -> None:
        # if self._params.saturation_min == value:
        #     return
        self.params = replace(self.params, saturation_min=value)
        # self.on_saturation_min_changed.emit(self._params.saturation_min)
        # self.on_changed.emit()

    @property
    def saturation_max(self) -> int:
        return self.params.saturation_max

    @saturation_max.setter
    def saturation_max(self, value: int) -> None:
        # if self._params.saturation_max == value:
        #     return
        self.params = replace(self.params, saturation_max=value)
        # self.on_saturation_max_changed.emit(self._params.saturation_max)
        # self.on_changed.emit()

    @property
    def value_min(self) -> int:
        return self.params.value_min

    @value_min.setter
    def value_min(self, value: int) -> None:
        # if self._params.value_min == value:
        #     return
        self.params = replace(self.params, value_min=value)
        # self.on_value_min_changed.emit(self._params.value_min)
        # self.on_changed.emit()
        # self.trigger_signals(previousParams)

    @property
    def value_max(self) -> int:
        return self.params.value_max

    @value_max.setter
    def value_max(self, value: int) -> None:
        # if self._params.value_max == value:
        #     return
        # previousParams = self._params
        self.params = replace(self.params, value_max=value)
        # self.on_value_max_changed.emit(self._params.value_max)
        # self.on_changed.emit()
        # self.trigger_signals(previousParams)

    @property
    def params(self) -> HSVThresholdParams:
        return self._params

    @params.setter
    def params(self, value: HSVThresholdParams) -> None:
        # Apply the changes
        oldValue = self._params
        self._params = value
        self.trigger_signals(oldValue)

        # # Trigger the signals unconditionally
        # # (This allows us to refresh the UI by triggering all signals.)
        # self.on_hue_min_changed.emit(self._params.hue_min)
        # self.on_hue_max_changed.emit(self._params.hue_max)
        # self.on_saturation_min_changed.emit(self._params.saturation_min)
        # self.on_saturation_max_changed.emit(self._params.saturation_max)
        # self.on_value_min_changed.emit(self._params.value_min)
        # self.on_value_max_changed.emit(self._params.value_max)
        # self.on_changed.emit()

    def trigger_signals(self, previous: HSVThresholdParams | None) -> None:
        if not previous or self._params.hue_min != previous.hue_min:
            self.on_hue_min_changed.emit(self._params.hue_min)
        if not previous or self._params.hue_max != previous.hue_max:
            self.on_hue_max_changed.emit(self._params.hue_max)
        if not previous or self._params.saturation_min != previous.saturation_min:
            self.on_saturation_min_changed.emit(self._params.saturation_min)
        if not previous or self._params.saturation_max != previous.saturation_max:
            self.on_saturation_max_changed.emit(self._params.saturation_max)
        if not previous or self._params.value_min != previous.value_min:
            self.on_value_min_changed.emit(self._params.value_min)
        if not previous or self._params.value_max != previous.value_max:
            self.on_value_max_changed.emit(self._params.value_max)
        if not previous or self._params != previous:
            self.on_changed.emit()