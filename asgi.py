import json


def batch_encode(*strings):
    for s in strings:
        yield s.encode('utf8') if isinstance(s, str) else s


async def respond_json(send, data, status=200, headers=None):
    headers_ = []

    for k, v in headers or []:
        k, v = batch_encode(k, v)

        if k.lower() == b'content-type':
            continue

        headers_.append((k, v))

    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers_ + [(b'content-type', b'application/json')]
    })

    await send({
        'type': 'http.response.body',
        'body': json.dumps(data).encode('utf8'),
    })


async def app(scope, receive, send):
    print(scope)

    if scope['type'] == 'lifespan':
        while True:
            message = await receive()

            if message['type'] == 'lifespan.startup':
                ...  # Do some startup here!
                await send({'type': 'lifespan.startup.complete'})

            elif message['type'] == 'lifespan.shutdown':
                ...  # Do some shutdown here!
                await send({'type': 'lifespan.shutdown.complete'})
                return

    if scope['method'] == 'POST':
        message = await receive()
        data = json.loads(message['body'].decode('utf8'))  # ignore 'more_body'

        print('received', data)

        await send(dict(type='http.response.start', status=201))
        await send(dict(type='http.response.body', body=b''))
        return

    if scope['path'] == '/hello':
        greet = 'Hello!'
    else:
        greet = 'Welcome!'

    await respond_json(send, dict(greet=greet))
