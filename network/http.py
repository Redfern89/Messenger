import asyncio
import aiohttp

class HttpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = None
        self.base_url = f"http://{self.host}:{self.port}"
    
    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def login(self, login, password):
        url = f"{self.base_url}/login"
        await self._ensure_session()
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with self.session.post(url=url, json={
                "login": login,
                "password": password
            }, timeout=timeout) as response:
                try:
                    if response.status != 200:
                        text = await response.text()
                        raise Exception(f"Login failed: {text}")
                    
                    data = await response.json()
                    return data
                except aiohttp.ContentTypeError as e:
                    text = await response.text()
                    raise Exception(f"Invalid response format: {text}") from e

        except aiohttp.ClientConnectorError as e:
            raise Exception("Server is unreachable") from e

        except aiohttp.ClientError as e:
            raise Exception(f"HTTP error: {e}") from e

        except asyncio.TimeoutError as e:
            raise Exception("Request timeout") from e
        
    async def close(self):
        if self.session is not None:
            await self.session.close()