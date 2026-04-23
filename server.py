#!/usr/bin/env python3

from aiohttp import web
from uuid import uuid4

routes = web.RouteTableDef()
uid = uuid4().hex


@routes.get("/ws")
async def websocket_handler(request):
	ws = web.WebSocketResponse()
	await ws.prepare(request)

	print("[WS] client connected")

	async for msg in ws:
		if msg.type == web.WSMsgType.TEXT:
			print(f"[WS] recv: {msg.data}")
			await ws.send_str(f"echo: {msg.data}")

	print("[WS] client disconnected")
	return ws


@routes.post("/login")
async def login(request):
	try:
		data = await request.json()
	except:
		return web.json_response(
			{"error": "Invalid JSON"},
			status=400
		)

	login = data.get("login")
	password = data.get("password")

	if login == "Redfern89" and password == "password000":
		return web.json_response({
			"token": uid
		})

	return web.json_response(
		{"error": "Invalid credentials"},
		status=401
	)


app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
	web.run_app(app, host="127.0.0.1", port=8000)