# httpとwebsocketの条件分岐
async def app(scope, receive, send):
    if scope['type'] == 'http':
        await http_applciation(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_applciation(scope, receive, send)

# httpの処理
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

# websocketの処理
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
