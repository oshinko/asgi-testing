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
    if scope['path'] == '/hello':
        greet = 'Hello!'
    else:
        greet = 'Welcome!'

    await respond_json(send, dict(greet=greet))
