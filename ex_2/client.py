import base64
import json
import os.path
import socket
import sys

srv_ip = input('Input Server IP: ') or '127.0.0.1'
srv_port = int(input('Input Server Port: '))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((srv_ip, srv_port))
except:
    sys.exit(1)


def send_command(cmd, *args, **kwargs):
    sock.send(json.dumps(dict(
        command=cmd, args=args, kwargs=kwargs,
    )).encode('utf-8'))


def recv_response():
    data = b''
    while True:
        buffer = sock.recv(4096)
        data += buffer
        if len(buffer) != 4096:
            break

    resp = json.loads(data.decode('utf-8'))  # type: dict
    return resp


def quit_(*_):
    sock.close()
    sys.exit(0)


def get(*args):
    send_command('get', path=' '.join(args))
    resp = recv_response()
    dest_dir = os.path.expanduser(input('Save Dir: '))

    filename = resp.get('filename')
    data = resp.get('data').encode()  # type: bytes
    data = base64.b64decode(data)

    with open(os.path.join(dest_dir, filename), 'bw') as io:
        io.write(data)
    print('Save "%s" Completed.' % filename)


def ls(*args):
    send_command('ls', dir=' '.join(args))
    resp = recv_response()
    print(resp['files'])


commands = {
    'quit': quit_,
    'get': get,
    'ls': ls,
}
while sock:
    try:
        _args = input('> ').split(' ')
        cmd, args = _args[0], _args[1:]
        command = commands.get(cmd)
        if command:
            command(*args)
    except KeyboardInterrupt:
        break

sock.close()
