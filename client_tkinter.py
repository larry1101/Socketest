import datetime
import json
import socket
import threading
import traceback
from tkinter import Tk, Label, StringVar, Entry, Button, Frame, TOP, X, EW, NSEW, Listbox, BOTH, RIGHT, LEFT, END, \
    BOTTOM


class MyClient:
    def __init__(self):
        self.__ini_data()
        print('Data prepared...')
        self.__ini_widget()

        self.__exit()

    def __ini_data(self):
        self.c_data = {'msg': '', 'release': False, 's_time': ''}

        self.INI_SERVER = False
        self.INI_CLIENT = False
        self.EXIT=False

        self.HOST = '127.0.0.1'
        # self.HOST = '192.168.1.101'
        self.PORT = 54321

        self.client = socket.socket()

    def __ini_widget(self):
        self.root_window = Tk()
        self.root_window.title('Client')

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
        self.btn_open = Button(frame_address, text='Connect', command=self.__connect)
        self.btn_open.grid(row=2, columnspan=2, sticky=NSEW)

        self.conn_stat = Label(self.root_window, text="Please click 'Connect'")
        self.conn_stat.pack(side=TOP, fill=X)

        # talk widgets group
        self.frame_talk = Frame(self.root_window)

        self.list_box_data = Listbox(self.frame_talk)
        self.list_box_data.pack(expand=True, fill=BOTH)
        self.s_text = Label(self.frame_talk, text="Server's message'")
        self.s_text.pack(side=TOP, fill=X)

        self.frame_client_input = Frame(self.frame_talk)
        self.frame_client_input.pack(fill=X)
        self.c_text = StringVar()
        self.c_texter = Entry(self.frame_client_input, textvariable=self.c_text)
        self.c_texter.bind("<Key>", self.on_texter_key)
        self.c_texter.pack(side=LEFT, fill=X, expand=True)
        btn_send = Button(self.frame_client_input, text='Send', command=self.on_click_btn_send)
        btn_send.pack(side=RIGHT)

        btn_exit = Button(self.root_window, text='Exit', command=self.on_btn_exit)
        btn_exit.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        # open window
        self.root_window.mainloop()

    def on_click_btn_send(self):
        try:
            self.c_data['s_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c_data['msg'] = self.c_text.get()
            self.client.send(json.dumps(self.c_data).encode('utf-8'))
            self.c_text.set('')
            self.list_box_data.insert(END, 'Server %s :' % (self.c_data['s_time']))
            self.list_box_data.insert(END, ' %s' % (self.c_data['msg']))
            self.list_box_data.see(END)
        except Exception as e:
            traceback.print_exc()

    def __exit(self):
        self.client.close()

    def __start_listen(self):
        while True:
            try:
                s_data = json.loads(self.client.recv(1024).decode('utf8'))
                if s_data['release']:
                    # self.CONN=False
                    break
                print('server:', s_data['msg'])
                self.s_text['text'] = s_data['msg']
                self.list_box_data.insert(END, 'Server %s :' % (s_data['s_time']))
                self.list_box_data.insert(END, ' %s' % (s_data['msg']))
                self.list_box_data.see(END)
                self.root_window.update()
            except Exception as e:
                traceback.print_exc()
        if not self.EXIT:
            self.conn_stat['text'] = 'Connection released'
            self.frame_client_input.destroy()
            self.s_text['text'] = "Server is offline"

    def __connect(self):
        try:
            self.client.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:
            traceback.print_exc()
            print('目标ip:port可能没在监听')
            return
        self.frame_talk.pack(expand=True, fill=BOTH)
        self.conn_stat['text'] = "Connected"
        self.INI_SERVER=True
        self.INI_CLIENT=True
        self.btn_open.destroy()
        self.root_window.update()

        self.thread_listen = threading.Thread(target=self.__start_listen)
        self.thread_listen.start()

    def on_btn_exit(self):
        self.EXIT=True
        self.frame_client_input.destroy()
        self.conn_stat['text'] = "Waiting for server's exit"
        self.c_data['release'] = True
        self.client.send(json.dumps(self.c_data).encode('utf-8'))
        print('exit signal sent...')
        self.root_window.update()
        self.thread_listen.join()
        self.root_window.destroy()

    def on_texter_key(self, event):
        if event.keysym == 'Return':
            # 按下了回车
            self.on_click_btn_send()


MyClient()
