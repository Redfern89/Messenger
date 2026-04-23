import asyncio

class AppClient:
	def __init__(self, state, auth_service, wscli):
		self.state = state
		self.auth = auth_service
		self.ws = wscli
		self.ws_ready = asyncio.Event()
		self._ws_task = None

	async def login(self, login, password):
		token = await self.auth.login(login, password)
		await self.connect_ws()

		print(f"[AppCli] Login: {login}:{password}")

		return token

	async def connect_ws(self):
		await self.ws.connect()
		self._ws_task = asyncio.create_task(self.ws.recv_loop())
		self.ws_ready.set()

	async def send(self, message):
		if not self.ws_ready.is_set():
			raise Exception("[AppCLI] WS not ready")
		
		await self.ws.send(message=message)
	
	async def shutdown(self):
		if self._ws_task:
			self._ws_task.cancel()

		await self.ws.close()
