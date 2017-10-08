import socket
import threading
import traceback

host = '127.0.0.1'
port = 54321

c = socket.socket()
c.connect((host, port))

print('Conntcted...')

c.send('Hello, I am client'.encode('utf-8'))


def listen():
    while True:
        try:
            s_data = c.recv(1024).decode('utf8')
            print('Server:', s_data)
            if s_data == 'exit':
                break

        except Exception:
            traceback.print_exc()


t = threading.Thread(target=listen)
t.start()

c_data = ''
while c_data != 'exit':
    try:
        c_data = input('>>')
        c.send(c_data.encode('utf-8'))
    except Exception as e:
        traceback.print_exc()

t.join()

c.close()

print('Closed')
