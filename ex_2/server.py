import base64
import json
import os
import socket
import threading
from typing import List

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.bind(('0.0.0.0', 0))
srv_sock.listen()


def srv_log(*args, **kwargs):
    print('[Server %s:%s]' % srv_sock.getsockname(), *args, **kwargs)


srv_log('Listening...')
threads = []  # type: List[threading.Thread]


def ls(dir, **kwargs):
    files = os.listdir(dir or '.')
    return dict(files=files)


def get(path, **kwargs):
    filename = os.path.basename(path)
    path = os.path.expanduser(path)
    data = b''
    if os.path.exists(path):
        with open(path, 'rb') as io:
            data = io.read()
        data = base64.b64encode(data)
    return dict(filename=filename, data=data.decode('utf-8'))


commands = {
    'ls': ls,
    'get': get,
}


def handle_command(data, sock: socket.socket, logger=None):
    req = json.loads(data)  # type: dict
    command = commands.get(req['command'])
    if command:
        resp = command(*req.get('args'), **req.get('kwargs'))
        data = json.dumps(resp).encode('utf-8')
        if logger:
            logger('Send', data)
        sock.send(data)


def cli_loop(sock: socket.socket, info):
    def cli_log(*args, **kwargs):
        print('[Client %s:%s]' % info, *args, **kwargs)

    cli_log('Connected.')
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                cli_log('Disconnected.')
                break
            cli_log('Recv', data)
            if data:
                handle_command(data, sock, logger=cli_log)
    finally:
        sock.close()


while True:
    try:
        cli_sock, info = srv_sock.accept()
        cli_thread = threading.Thread(target=cli_loop, args=(cli_sock, info))
        threads.append(cli_thread)
        cli_thread.start()
    except KeyboardInterrupt:
        break

for t in threads:
    t.join()
srv_sock.close()
