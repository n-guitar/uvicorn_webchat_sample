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
    print('-------------scope--------------')
    print('scope: {}'.format(scope))
    print('scope_type: {}'.format(type(scope)))
    print('-------------receive--------------')
    print('receive_type: {}'.format(type(receive)))
    print('-------------send--------------')
    print('send_type: {}'.format(type(send)))
