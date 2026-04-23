class AuthService:
    def __init__(self, http, state):
        self.http = http
        self.state = state

    async def login(self, login, password):
        response = await self.http.login(login, password)
        token = response.get("token")

        if not token:
            raise Exception("Login failed: No token received")

        self.state.token = token

        return token