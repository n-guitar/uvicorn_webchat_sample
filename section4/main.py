async def app(scope, receive, send):
    if scope['type'] == 'http':
        await http_applciation(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_applciation(WebSocket(scope, receive, send))
        return


async def http_applciation(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })


async def websocket_applciation(ws):
    await ws.accept()
    try:
        while True:
            data = await ws.receive()
            await ws.send_text(data['text'])
    except:
        await ws.close()


class HeaderParse:
    def __init__(self, scope):
        self._scope = scope

    @property
    def keys(self):
        return [header[0].decode() for header in self._scope["headers"]]

    @property
    def as_dict(self):
        return {header[0].decode(): header[1].decode() for header in self._scope["headers"]}


class WebSocket:
    def __init__(self, scope, receive, send):
        self._scope = scope
        self._receive = receive
        self._send = send

    @property
    def headers(self):
        return HeaderParse(self._scope)

    @property
    def path(self):
        return self._scope["path"]

    async def accept(self):
        await self.receive()
        await self.send({
            "type": "websocket.accept"
        })

    async def close(self,):
        await self.send({
            "type": "websocket.close"
        })

    async def send(self, message):
        await self._send(message)

    async def receive(self):
        message = await self._receive()
        return message

    async def send_text(self, text):
        await self.send({
            "type": "websocket.send",
            "text": text
        })
