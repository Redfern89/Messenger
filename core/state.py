from PyQt5.QtCore import QObject, pyqtSignal

class AppState(QObject):
	changed = pyqtSignal()

	def __init__(self):
		super().__init__()
		self._token = None

	def set_token(self, value):
		self._token = value
		self.changed.emit()