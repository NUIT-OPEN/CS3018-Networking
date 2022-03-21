import multiprocessing
import queue
import socket
import threading

ip = input('Input Server IP: ') or '127.0.0.1'
port_range = [int(i) for i in (input('Input Server Ports Range: ') or '1-1025').split('-')]

print_lock = threading.Lock()

q = queue.Queue()
for port in range(*port_range):
    q.put(port)


def log(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def scan():
    while True:
        try:
            port = q.get(False)
        except queue.Empty:
            break

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            log('[%s:%s]' % (ip, port), 'Open', 'Protocol: %s' % socket.getservbyport(port, 'tcp'))
        except:
            log('[%s:%s]' % (ip, port), 'Close', end='\r')
        finally:
            sock.close()


threads = []
for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=scan)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
