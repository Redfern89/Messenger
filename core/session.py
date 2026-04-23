import asyncio

from core.state import AppState
from network.http import HttpClient
from network.ws import WSClient
from services.auth_service import AuthService
from core.app_client import AppClient
from PyQt5.QtCore import QObject, pyqtSignal

class Session():
    def __init__(self, host, port, state):
        self.host = host
        self.port = port
        self.state = state

        self.http = HttpClient(host, port)
        self.ws = WSClient(host, port, state)
        self.auth = AuthService(self.http, state)
        self.app = AppClient(state, self.auth, self.ws)

    async def login(self, login, password):
        return await self.app.login(login, password)
    
    async def close(self):
        await self.app.shutdown()
        await self.http.close()

class SessionManager(QObject):
    session_changed = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.session = None

    def create_session(self, host, port):
        if self.session:
            asyncio.create_task(self.session.close())

        self.session = Session(host, port, AppState())
        self.session_changed.emit(self.session)

    def get(self):
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()

    def destroy(self):
        self.session = None