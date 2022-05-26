from core.ui.abstract_ui import AbstractUi
from PyQt5 import uic


class Tools(AbstractUi):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        uic.loadUi('./ui/tools.ui', self)

        self.extract_text = False
        self.detect_edges = False

        self.align_image = {
            'execute': False,
            'opened_image': None
        }

        self.buttonExtractText.clicked.connect(self._extract_text)
        self.buttonDetectEdges.clicked.connect(self._detect_edges)
        self.buttonAlignImage.clicked.connect(self._align_image)

    def get_widget_state(self):
        return {
            'extract_text': self.extract_text,
            'detect_edges': self.detect_edges,
            'align_image': self.align_image,
        }

    def set_widget_state(self, state=None):
        if state is None:
            state = {}

        self.buttonExtractText.blockSignals(True)
        self.buttonDetectEdges.blockSignals(True)
        self.buttonAlignImage.blockSignals(True)

        self.extract_text = state.get('extract_text', False)
        self.detect_edges = state.get('detect_edges', False)
        self.align_image = state.get('align_image', {
            'execute': False,
            'opened_image': None
        })

        self.buttonExtractText.blockSignals(False)
        self.buttonDetectEdges.blockSignals(False)
        self.buttonAlignImage.blockSignals(False)

    @AbstractUi.image_processed
    def _extract_text(self):
        self.extract_text = True

    @AbstractUi.image_processed
    def _detect_edges(self):
        self.detect_edges = True

    @AbstractUi.image_processed
    def _align_image(self):
        self.align_image["execute"] = True
        self.align_image["opened"] = None
