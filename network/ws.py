import asyncio
import websockets
from core.state import AppState


class WSClient:
    def __init__(self, host, port, state: AppState):
        self.state = state
        self.ws = None
        self.running = False
        self.host = host
        self.port = port
        self.reconnect_timeout = 2 # Пока тут, потом вынесу в settings

    async def connect(self):
        if self.ws and not self.ws.closed:
            return

        url = f"ws://{self.host}:{self.port}/ws"

        try:
            self.ws = await websockets.connect(url)
            self.state.connected = True
            print("[WS] Connected")

        except Exception as e:
            self.state.connected = False
            raise Exception(f"[WS] Connect failed: {e}")
    
    async def recv_loop(self):
        self.running = True

        while self.running:
            try:
                message = await self.ws.recv()
                print(f"[WS] Received {message}")
            
            except websockets.ConnectionClosed:
                self.state.connected = False
                print("[WS] Connection closed, reconnecting ...")
                await self._reconnect()
                continue

            except Exception as e:
                raise Exception(f"[WS] Error {e}") from e
    
    async def send(self, message):
        if self.ws is None or self.ws.closed:
            raise Exception("[WS] Cannot send: not connected")

        await self.ws.send(message)

    async def _reconnect(self):
        while self.running:
            await asyncio.sleep(self.reconnect_timeout)

            try:
                if self.ws:
                    await self.ws.close()
                    self.ws = None

                await self.connect()
                return

            except Exception as e:
                print(f"[WS] Reconnect failed: {e}")
        
    async def close(self):
        self.running = False

        if self.ws:
            await self.ws.close()