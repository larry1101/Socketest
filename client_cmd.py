import socket
import traceback

host='127.0.0.1'
port=54321

c = socket.socket()
c.connect((host,port))

print('Conntcted...')

c.send('Hello, I am client'.encode('utf-8'))
c_data=''
while c_data != 'exit':
    try:
        s_data=c.recv(1024)
        print('Server:',s_data.decode('utf8'))
        c_data=input('>')
        c.send(c_data.encode('utf-8'))
    except Exception as e:
        traceback.print_exc()

c.close()

print('Closed')