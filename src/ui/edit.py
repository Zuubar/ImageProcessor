import re
from PyQt5 import uic

from src.helpers.generic import GenericHelper
from src.ui.abstract_ui import AbstractUi


class Edit(AbstractUi):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        uic.loadUi(GenericHelper.get(__file__, '../../ui/edit.ui'), self)

        self.brightnessSlider.valueChanged.connect(self.brightness_changed)
        self.blurSlider.valueChanged.connect(self.blur_changed)
        self.rotationDial.valueChanged.connect(self.rotation_changed)
        self.contrastSlider.valueChanged.connect(self.contrast_changed)

        self.buttonFlipHorizontally.clicked.connect(self.flip_horizontally)
        self.buttonFlipVertically.clicked.connect(self.flip_vertically)
        self.buttonFlipBoth.clicked.connect(self.flip_both)

        self.flip_mode = None

    def get_widget_state(self):
        return {
            'brightness_slider': self.brightnessSlider.value(),
            'blur_slider': self.blurSlider.value(),
            'rotation_dial': self.rotationDial.value(),
            'contrast_slider': self.contrastSlider.value(),
            'flip_mode': self.flip_mode
        }

    def set_widget_state(self, state=None):
        if state is None:
            state = {}

        self.brightnessSlider.setValue(state.get('brightness_slider', 0))
        self.blurSlider.setValue(state.get('blur_slider', 0))
        self.rotationDial.setValue(state.get('rotation_dial', 180))
        self.contrastSlider.setValue(state.get('contrast_slider', 10))
        self.flip_mode = state.get('flip_mode', None)

    @AbstractUi.image_processed
    def brightness_changed(self):
        self.brightnessLabel.setText(
            re.sub(r"\d+", str(self.brightnessSlider.value()), str(self.brightnessLabel.text())))

    @AbstractUi.image_processed
    def blur_changed(self):
        self.blurLabel.setText(
            re.sub(r"\d+", str(self.blurSlider.value()), str(self.blurLabel.text())))

    @AbstractUi.image_processed
    def rotation_changed(self):
        self.rotationLabel.setText(
            re.sub(r"[+-]?\d+(?:\.\d+)?", str(-(self.rotationDial.value() - 180)), str(self.rotationLabel.text())))

    @AbstractUi.image_processed
    def contrast_changed(self):
        self.contrastLabel.setText(
            re.sub(r"\b\d+([.,]\d+)?", str(self.contrastSlider.value() / 10), str(self.contrastLabel.text())))

    @AbstractUi.image_processed
    def flip_horizontally(self):
        self.flip_mode = 1

    @AbstractUi.image_processed
    def flip_vertically(self):
        self.flip_mode = 0

    @AbstractUi.image_processed
    def flip_both(self):
        self.flip_mode = -1
