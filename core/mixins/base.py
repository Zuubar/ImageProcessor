import functools

import cv2 as cv
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap


class BaseMixin(object):
    def render_image(func):
        @functools.wraps(func)
        def wrapper(self, **kwargs):
            result = func(self, **kwargs)
            self._render_image()
            return result

        return wrapper

    def _render_image(self):
        if self.image is None:
            return

        frame = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image).scaled(self.UI_image_view.width(),
                                                 self.UI_image_view.height(),
                                                 QtCore.Qt.KeepAspectRatio,
                                                 QtCore.Qt.SmoothTransformation)
        self.UI_image_view.setPixmap(pixmap)

    @render_image
    def _process_image(self, **kwargs):
        if self.image is None:
            return

        def apply_effects(fx_functions, current_image):
            return current_image if len(fx_functions) == 0 \
                else apply_effects(fx_functions[1:], fx_functions[0](current_image))

        fx_functions = [getattr(self, attr) for attr in dir(self) if attr.startswith('fx')]
        self.image = apply_effects(fx_functions, self.original_image)