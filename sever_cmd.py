"""
socketserver ?
"""

import socket
import threading
import traceback

host = '127.0.0.1'
port = 54321

sk = socket.socket()

sk.bind((host, port))

sk.listen(5)

conn, address = sk.accept()
print('conn =', conn, 'add =', address)


# sk.sendall(bytes("Hello world", encoding="utf-8"))
def listen():
    while True:
        try:
            c_data = conn.recv(1024).decode('utf8')
            print('Client:', c_data)
            if c_data == 'exit':
                break

        except Exception:
            traceback.print_exc()


t = threading.Thread(target=listen)
t.start()

s_data = ''
while s_data != 'exit':
    s_data = input('>>')
    conn.send(s_data.encode('utf-8'))

t.join()

conn.close()
sk.close()

print('Closed')
