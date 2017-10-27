import datetime
import json
import socket
import socketserver
import threading
import traceback
from tkinter import Tk, Label, Entry, StringVar, Button, Frame, X, NSEW, TOP, CENTER, BOTTOM, Listbox, RIGHT, LEFT, NS, \
    EW, END, BOTH


class MyServer:
    def __init__(self):
        self.__ini_data()
        print('Data prepared...')
        # self.__ini_socket()
        self.__ini_widget()

        self.__exit()

    def __ini_widget(self):
        self.root_window = Tk()
        self.root_window.title('Server')

        # pre connection settings widgets group
        frame_address = Frame(self.root_window)
        frame_address.pack(side=TOP, fill=X, padx=5, pady=5)
        label_ip = Label(frame_address, text='IP')
        label_ip.grid(row=0, sticky=EW)
        self.ip_text = StringVar()
        self.ip_text.set(self.HOST)
        self.ip_texter = Entry(frame_address, textvariable=self.ip_text, width=30)
        self.ip_texter.grid(row=0, column=1, sticky=EW)
        label_port = Label(frame_address, text='Port')
        label_port.grid(row=1, sticky=EW)
        self.port_text = StringVar()
        self.port_text.set(self.PORT)
        self.port_texter = Entry(frame_address, textvariable=self.port_text)
        self.port_texter.grid(row=1, column=1, sticky=EW)
        self.btn_open = Button(frame_address, text='Open Port', command=self.__open_port)
        self.btn_open.grid(row=2, columnspan=2, sticky=NSEW)

        # talk widgets group
        self.frame_talk = Frame(self.root_window)

        self.c_info = Label(self.frame_talk, text='Client info - -\nWating for connection')
        self.c_info.pack(side=TOP, fill=X)

        self.list_box_data = Listbox(self.frame_talk)
        self.list_box_data.pack(expand=True, fill=BOTH)

        self.c_text = Label(self.frame_talk, text="Client's message")
        self.c_text.pack(side=TOP, fill=X)

        self.frame_server_input = Frame(self.frame_talk)
        self.frame_server_input.pack(fill=X)
        self.s_text = StringVar()
        self.s_texter = Entry(self.frame_server_input, textvariable=self.s_text)
        self.s_texter.bind("<Key>", self.on_texter_key)
        self.s_texter.pack(side=LEFT, fill=X, expand=True)
        btn_send = Button(self.frame_server_input, text='Send', command=self.on_click_btn_send, width=15)
        btn_send.pack(side=RIGHT)

        # btn exit
        btn_exit = Button(self.root_window, text='Exit', command=self.on_btn_exit)
        btn_exit.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        # open window
        self.root_window.mainloop()

    def __exit(self):
        if self.INI_SERVER:
            self.server.close()

        print('Byebye')
        # if self.CONN:
        #     self.client.close()

    def __start_listen(self):
        print('Start listen')
        try:
            self.client, self.c_add = self.server.accept()
            t_conn_establish = datetime.datetime.now()
            print('Connection established')
            self.c_info['text'] = 'Client info: host = %s , port = %d\nConnected at %s' % (
                self.c_add[0], self.c_add[1], t_conn_establish.strftime('%Y-%m-%d %H:%M:%S'))
            self.INI_CLIENT = True
            # self.CONN = True
            self.root_window.update()
            while True:
                try:
                    c_data = json.loads(self.client.recv(1024).decode('utf8'))
                    if c_data['release']:  # 放在后面会卡死
                        # self.CONN = False
                        break
                    print('%s\nClient:%s' % (c_data['s_time'], c_data['msg']))
                    self.c_text['text'] = c_data['msg']

                    self.list_box_data.insert(END, 'Client %s :' % (c_data['s_time']))
                    self.list_box_data.insert(END, ' %s' % (c_data['msg']))
                    self.list_box_data.see(END)

                    self.root_window.update()
                except Exception as e:
                    traceback.print_exc()
            if not self.EXIT:
                self.c_info['text'] = 'Connection released'
                self.frame_server_input.destroy()
                self.c_text['text'] = "Client is offline"

        except OSError as e:
            traceback.print_exc()
            pass

    def on_click_btn_send(self):
        try:
            self.s_data['msg'] = self.s_text.get()
            self.s_data['s_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.client.send(json.dumps(self.s_data).encode('utf-8'))
            self.s_text.set('')
            self.list_box_data.insert(END, 'Server %s :' % (self.s_data['s_time']))
            self.list_box_data.insert(END, ' %s' % (self.s_data['msg']))
            self.list_box_data.see(END)
        except Exception as e:
            traceback.print_exc()

    def on_texter_key(self, event):
        if event.keysym == 'Return':
            # 按下了回车
            self.on_click_btn_send()

    def __open_port(self):
        self.btn_open.destroy()
        self.frame_talk.pack(expand=True, fill=BOTH)

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
        self.EXIT=True
        self.frame_server_input.destroy()
        self.c_text['text'] = "Waiting for client's exit"
        if self.INI_SERVER and not self.INI_CLIENT:
            self.server.close()
        if self.INI_CLIENT:
            self.s_data['release'] = True
            self.client.send(json.dumps(self.s_data).encode('utf-8'))
            print('Exit signal sent...')
            # self.client.close()
            self.root_window.update()
            self.thread_listen.join()
        self.root_window.destroy()

    def __ini_data(self):
        self.INI_SERVER = False
        self.INI_CLIENT = False
        # self.CONN=False
        self.EXIT=False

        self.HOST = '127.0.0.1'
        # self.HOST = '192.168.1.101'
        self.PORT = 54321

        self.s_data = {'msg': '', 'release': False, 's_time': ''}

        self.server = socket.socket()


MyServer()
