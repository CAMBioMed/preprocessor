from functools import partial

from PySide6.QtWidgets import QWidget

from preprocessor.gui.hsv_threshold_model import HSVThresholdModel
from preprocessor.gui.ui_hsv_threshold import Ui_HSVThreshold


class HSVThresholdWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        QWidget.__init__(self, parent)

        self.ui = Ui_HSVThreshold()
        self.ui.setupUi(self)

        self.model = HSVThresholdModel()
        self._connect_signals()
        self.model.trigger_signals(None)  # Trigger all signals to initialize UI
        # self.model.params = self.model.params

    def _connect_signals(self) -> None:
        # Connect model to UI
        self.model.on_hue_min_changed.connect(self.ui.sliderHueMin.setValue)
        self.model.on_hue_min_changed.connect(self.ui.spinboxHueMin.setValue)
        self.model.on_hue_max_changed.connect(self.ui.sliderHueMax.setValue)
        self.model.on_hue_max_changed.connect(self.ui.spinboxHueMax.setValue)
        self.model.on_saturation_min_changed.connect(self.ui.sliderSaturationMin.setValue)
        self.model.on_saturation_min_changed.connect(self.ui.spinboxSaturationMin.setValue)
        self.model.on_saturation_max_changed.connect(self.ui.sliderSaturationMax.setValue)
        self.model.on_saturation_max_changed.connect(self.ui.spinboxSaturationMax.setValue)
        self.model.on_value_min_changed.connect(self.ui.sliderValueMin.setValue)
        self.model.on_value_min_changed.connect(self.ui.spinboxValueMin.setValue)
        self.model.on_value_max_changed.connect(self.ui.sliderValueMax.setValue)
        self.model.on_value_max_changed.connect(self.ui.spinboxValueMax.setValue)

        # Connect UI to model
        self.ui.sliderHueMin.valueChanged.connect(partial(setattr, self.model, "hue_min"))
        self.ui.spinboxHueMin.valueChanged.connect(partial(setattr, self.model, "hue_min"))
        self.ui.sliderHueMax.valueChanged.connect(partial(setattr, self.model, "hue_max"))
        self.ui.spinboxHueMax.valueChanged.connect(partial(setattr, self.model, "hue_max"))
        self.ui.sliderSaturationMin.valueChanged.connect(partial(setattr, self.model, "saturation_min"))
        self.ui.spinboxSaturationMin.valueChanged.connect(partial(setattr, self.model, "saturation_min"))
        self.ui.sliderSaturationMax.valueChanged.connect(partial(setattr, self.model, "saturation_max"))
        self.ui.spinboxSaturationMax.valueChanged.connect(partial(setattr, self.model, "saturation_max"))
        self.ui.sliderValueMin.valueChanged.connect(partial(setattr, self.model, "value_min"))
        self.ui.spinboxValueMin.valueChanged.connect(partial(setattr, self.model, "value_min"))
        self.ui.sliderValueMax.valueChanged.connect(partial(setattr, self.model, "value_max"))
        self.ui.spinboxValueMax.valueChanged.connect(partial(setattr, self.model, "value_max"))
