import socket
import socketserver
import threading
import traceback
from tkinter import Tk, Label, Entry, StringVar, Button, Frame, X, NSEW, TOP, CENTER, BOTTOM


class MyServer():
    def __init__(self):
        self.__ini_data()
        print('Data prepared...')
        # self.__ini_socket()
        self.__ini_widget()

        self.__exit()

    def __ini_widget(self):
        self.root_window = Tk()
        self.root_window.title('Server')

        # preconnection settings
        frame_address = Frame(self.root_window, bg="#000")
        frame_address.pack(side=TOP, fill=X, padx=5, pady=5)
        label_ip = Label(frame_address, text='IP')
        label_ip.grid(row=0)
        self.ip_text = StringVar()
        self.ip_text.set(self.HOST)
        self.ip_texter = Entry(frame_address, textvariable=self.ip_text)
        self.ip_texter.grid(row=0, column=1)
        label_port = Label(frame_address, text='Port')
        label_port.grid(row=1)
        self.port_text = StringVar()
        self.port_text.set(self.PORT)
        self.port_texter = Entry(frame_address, textvariable=self.port_text)
        self.port_texter.grid(row=1, column=1)
        self.btn_open = Button(frame_address, text='Open Port', command=self.__open_port)
        self.btn_open.grid(row=2, columnspan=2, sticky=NSEW)

        self.frame_talk = Frame(self.root_window, bg="#666")
        self.frame_talk.pack()

        self.c_info = Label(self.frame_talk, text='Client info - -')
        self.c_info.pack()

        self.c_text = Label(self.frame_talk, text="Please click 'Open Port'")
        self.c_text.pack()

        self.s_text = StringVar()
        self.s_texter = Entry(self.frame_talk, textvariable=self.s_text)
        self.s_texter.bind("<Key>", self.on_texter_key)
        self.s_texter.pack()

        btn_send = Button(self.frame_talk, text='Send', command=self.on_click_btn_send)
        btn_send.pack()

        # btn exit
        btn_exit = Button(self.root_window, text='Exit', command=self.on_btn_exit)
        btn_exit.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        # open window
        self.root_window.mainloop()

    def __ini_socket(self):
        pass

    def __exit(self):
        if self.INI_SERVER:
            self.server.close()
        if self.CONN:
            self.client.close()

    def __start_listen(self):
        self.client, self.c_add = self.server.accept()
        print('Connection established')
        self.c_info['text'] = 'Client info: host = ' + self.c_add[0] + ', port = %d' % self.c_add[1]
        # self.c_text['text'] = "Waiting for client's reply"
        self.CONN=True
        self.root_window.update()
        while True:
            try:
                c_data = self.client.recv(1024).decode('utf8')
                print('client:', c_data)
                if c_data == '#None':  # 放在后面会卡死
                    break
                self.c_text['text'] = c_data
                self.root_window.update()
            except Exception as e:
                traceback.print_exc()
        print('Listen stopped')

    def on_click_btn_send(self):
        try:

            s = self.s_text.get()
            self.client.send(s.encode('utf-8'))
            self.s_text.set('')

            # c_data = self.client.recv(1024).decode('utf8')
            # self.c_text['text'] = c_data

        except Exception as e:
            traceback.print_exc()

    def on_texter_key(self, event):
        if event.keysym == 'Return':
            # 按下了回车
            self.on_click_btn_send()

    def __open_port(self):
        self.btn_open.destroy()

        self.HOST = self.ip_text.get()
        self.PORT = int(self.port_text.get())
        self.server.bind((self.HOST, self.PORT))
        self.INI_SERVER = True

        print('Server socket bind successfully\nListening...')

        self.c_info['text'] = "Waiting for client's connection"
        self.server.listen(3)
        self.root_window.update()

        self.thread_listen = threading.Thread(target=self.__start_listen)
        self.thread_listen.start()

    def on_btn_exit(self):
        if self.CONN:
            self.client.send('#None'.encode('utf-8'))
            print('exit signal sent...')
            self.root_window.update()
            self.thread_listen.join()
        self.root_window.destroy()

    def __ini_data(self):
        self.INI_SERVER = False
        self.INI_CLIENT = False

        self.CONN = False

        self.HOST = '127.0.0.1'
        # self.HOST = '192.168.1.101'
        self.PORT = 54321

        self.server = socket.socket()


MyServer()
