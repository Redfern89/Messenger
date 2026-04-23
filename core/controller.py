# core/controller.py

import asyncio
from qasync import asyncSlot
from PyQt5.QtCore import QObject, pyqtSignal

class AppController(QObject):
	login_success = pyqtSignal()
	login_failed = pyqtSignal(str)

	def __init__(self, session_manager):
		super().__init__()
		self.sm = session_manager

	@asyncSlot(str, str, str, str)
	async def handle_login(self, host, port, login, password):
		print("HANDLE LOGIN CALLED")
		try:
			self.sm.create_session(host, int(port))
			session = self.sm.get()

			await session.login(login, password)

			self.login_success.emit()

		except Exception as e:
			self.login_failed.emit(str(e))

'''class AppController(QObject):
	login_success = pyqtSignal()
	login_failed = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.state = AppState()

		self.http = None
		self.ws = None
		self.auth = None
		self.app = None

	async def _cleanup_session(self):
		if self.app:
			await self.app.shutdown()
			self.app = None
		
		if self.http:
			await self.http.close()
			self.http = None
		
		self.ws = None
		self.auth = None

	@asyncSlot(str, str, str, str)
	async def handle_login(self, host, port, login, password):
		await self._cleanup_session()
		try:
			port = int(port)

			# создаём инфраструктуру
			self.http = HttpClient(host, port)
			self.ws = WSClient(host, port, state=self.state)
			self.auth = AuthService(self.http, self.state)

			self.app = AppClient(self.state, self.auth, self.ws)

			await self.app.login(login, password)

			self.login_success.emit()

		except Exception as e:
			self.login_failed.emit(str(e))

	async def shutdown(self):
		if self.app:
			await self.app.shutdown()

		if self.http:
			await self.http.close()'''