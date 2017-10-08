import socket
import threading
import traceback
from tkinter import Tk, Label, StringVar, Entry, Button


class MyClient():
    def __init__(self):
        self.__ini_socket()
        self.__ini_widget()

        self.__exit()

    def __ini_widget(self):
        self.root_window = Tk()
        self.root_window.title('Client')

        self.btn_open = Button(self.root_window, text='Connect', command=self.__connect)
        self.btn_open.pack()

        self.s_text = Label(self.root_window, text="Please click 'Connect'")
        self.s_text.pack()

        self.c_text = StringVar()
        self.c_texter = Entry(self.root_window, textvariable=self.c_text)
        self.c_texter.bind("<Key>", self.on_texter_key)
        self.c_texter.pack()

        btn_send = Button(self.root_window, text='Send', command=self.on_click_btn_send)
        btn_send.pack()

        btn_exit = Button(self.root_window, text='Exit', command=self.on_btn_exit)
        btn_exit.pack()

        # open window
        self.root_window.mainloop()

    def on_click_btn_send(self):
        try:
            c_data = self.c_text.get().encode('utf-8')
            self.client.send(c_data)

            # s_data = self.client.recv(1024).decode('utf8')
            # self.s_text['text'] = s_data
        except Exception as e:
            traceback.print_exc()

    def __ini_socket(self):
        self.HOST = '127.0.0.1'
        self.PORT = 54321

        self.client = socket.socket()

    def __exit(self):
        self.client.close()

    def __start_listen(self):
        while True:
            try:
                s_data = self.client.recv(1024).decode('utf8')
                print('server:', s_data)
                if s_data == '#None':  # 放在后面会卡死
                    break
                self.s_text['text'] = s_data
                self.root_window.update()
            except Exception as e:
                traceback.print_exc()
        print('Listen stopped')

    def __connect(self):
        self.btn_open.destroy()
        self.client.connect((self.HOST, self.PORT))
        # self.client.send('Hello, I am client'.encode('utf-8'))
        self.s_text['text'] = "Wating for server's reply"
        self.root_window.update()

        self.thread_listen = threading.Thread(target=self.__start_listen)
        self.thread_listen.start()

    def on_btn_exit(self):
        self.client.send('#None'.encode('utf-8'))
        print('exit signal sent...')
        self.root_window.update()
        self.thread_listen.join()
        self.root_window.destroy()

    def on_texter_key(self, event):
        if event.keysym == 'Return':
            # 按下了回车
            self.on_click_btn_send()


MyClient()
