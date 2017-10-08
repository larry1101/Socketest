import socket
import traceback

host = '127.0.0.1'
port = 54321

sk = socket.socket()

sk.bind((host, port))

sk.listen(5)

conn, address = sk.accept()
print('conn =', conn, 'add =', address)
# sk.sendall(bytes("Hello world", encoding="utf-8"))
while True:
    try:
        c_data = conn.recv(1024).decode('utf8')
        print('Client:',c_data)
        if c_data == 'exit':
            break
        s_data = input('>')
        conn.send(s_data.encode('utf-8'))

    except Exception as e:
        traceback.print_exc()

conn.close()
sk.close()

print('Closed')
