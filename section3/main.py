async def app(scope, receive, send):
    await print_websocket_item(scope, receive, send)
    if scope['type'] == 'http':
        await http_applciation(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_applciation(scope, receive, send)


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


async def websocket_applciation(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            await send({
                'type': 'websocket.send',
                'text': event['text']
            })


async def print_websocket_item(scope, receive, send):
    print('-------------header--------------')
    header = HeaderParse(scope)
    print('header.keys: {}'.format(header.keys))
    print('header.keys_demo: {}'.format(header.keys_demo))
    print('header.as_dict: {}'.format(header.as_dict))
    print('header.as_dict_demo: {}'.format(header.as_dict_demo))


class HeaderParse:
    def __init__(self, scope):
        self._scope = scope

    @property
    def keys(self):
        return [header[0].decode() for header in self._scope["headers"]]

    @property
    def keys_demo(self):
        header_keys = []
        for header in self._scope["headers"]:
            header_keys.append(header[0].decode())
        return header_keys

    @property
    def as_dict(self):
        return {header[0].decode(): header[1].decode() for header in self._scope["headers"]}

    @property
    def as_dict_demo(self):
        header_as_dict = {}
        for header in self._scope["headers"]:
            header_as_dict[header[0].decode()] = header[1].decode()
        return header_as_dict
