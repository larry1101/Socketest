import socket
import socketserver
import traceback
from tkinter import Tk, Label, Entry, StringVar, Button


class MyServer():
    def __init__(self):
        self.__ini_socket()
        print('Socket established')
        self.__ini_widget()

        self.__exit()

    def __ini_widget(self):
        self.root_window = Tk()
        self.root_window.title('Server')

        self.btn_open=Button(self.root_window,text='Open Port', command=self.__start_listen)
        self.btn_open.pack()

        self.c_info = Label(self.root_window, text='Client info - -')
        self.c_info.pack()

        self.c_text = Label(self.root_window, text="Please click 'Open Port'")
        self.c_text.pack()

        self.s_text = StringVar()
        self.s_texter = Entry(self.root_window, textvariable=self.s_text)
        self.s_texter.pack()

        btn_send = Button(self.root_window, text='Send', command=self.on_click_btn_send)
        btn_send.pack()

        btn_exit = Button(self.root_window, text='Exit', command=self.root_window.destroy)
        btn_exit.pack()

        # open window
        self.root_window.mainloop()

    def __ini_socket(self):
        self.HOST = '127.0.0.1'
        self.PORT = 54321

        self.server = socket.socket()
        self.server.bind((self.HOST, self.PORT))

    def __exit(self):
        self.client.close()
        self.server.close()

    def __start_listen(self):
        self.btn_open.destroy()
        print('Listening...')
        self.c_info['text'] = "Waiting for client's connection"
        self.server.listen(5)
        self.root_window.update()

        self.client, self.c_add = self.server.accept()
        print('Connection established')
        self.c_info['text'] = 'Client info: host = ' + self.c_add[0] + ', port = %d' % self.c_add[1]
        self.root_window.update()

        try:
            c_data = self.client.recv(1024).decode('utf8')
            self.c_text['text'] = c_data
            self.root_window.update()

            self.client.send('hello client'.encode('utf-8'))

            c_data = self.client.recv(1024).decode('utf8')
            self.c_text['text'] = c_data

        except Exception as e:
            traceback.print_exc()

    def on_click_btn_send(self):
        try:

            s = self.s_text.get()
            self.client.send(s.encode('utf-8'))

            c_data = self.client.recv(1024).decode('utf8')
            self.c_text['text'] = c_data

        except Exception as e:
            traceback.print_exc()


MyServer()
