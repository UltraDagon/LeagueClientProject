import tkinter as tk
import tkinter.font
import random
import certifi
import urllib3
import requests
import threading
import json
from psutil import process_iter

class App():

    def __init__(self):
        self.session = requests.Session()
        self.session.headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.url = None
        self.clicked = None
        self.popups = []

        self.fonts = {}

        self.root = tk.Tk()
        self.focus = None

        self.fonts['default'] = tk.font.Font(family="SpiegelSans Trial",
                                             size=12)
        self.fonts['small'] = tk.font.Font(family="SpiegelSans Trial",
                                             size=10)

        self.root.geometry("1280x720")
        self.root.title("Ultra_Dagon's League Client Project")
        self.root.bind("<Button-1>", self.on_click)

        self.social = tk.Frame(self.root, bg="#9999cc")

        self.icon_uname_status = tk.Frame(self.social, height=80, width=224, bg="#9999cc")

        self.icon_display = tk.Canvas(self.icon_uname_status, bg="red", height=66, width=61)
        self.icon_display.bind("<Button-1>", self.open_customize_identity)
        self.icon_display.place(x=9, y=6)

        self.username = tk.Label(self.icon_uname_status, text="%username", font=('SpiegalSans, 12'), bg="#9999cc")
        self.username.place(relx=0.4,rely=0.35)

        self.status = tk.Entry(self.icon_uname_status, width=12, font=self.fonts['small'], bg="#9999cc")
        self.status.place(relx=0.4,rely=0.625)

        self.icon_uname_status.pack(fill=tk.X)

        self.friends = tk.Label(self.social, text="Friend 1\nFriend 2\nFriend 3\nFriend 4\nFriend 5", font=('Arial, 18'), bg="#9999cc")
        self.friends.pack()

        self.social.pack(side=tk.RIGHT, fill=tk.Y)

        self.navigation_bar = tk.Frame(self.root, bg="#ccccff") #11 tabs

        self.play_party = tk.Button(self.navigation_bar, text="Play", font=('Arial, 18'))
        self.play_party.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.home = tk.Button(self.navigation_bar, text="Home", font=('Arial, 18'))
        self.home.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.navigation_bar.pack(side=tk.TOP, fill=tk.X)

        self.connect()
        self.load_fields()
        self.root.mainloop()

    def open_customize_identity(self, event):
        self.customize_identity = tk.Frame(self.root, bg="#003366")
        self.customize_identity.place(x=160, y=80, width=960, height=560)

        self.customize_identity.bind("<Button-1>", self.click_popup)
        self.click_popup((self.customize_identity))

        self.popups.append(self.customize_identity)

    def connect(self):
        process = None
        process_args = {}

        for p in process_iter():
            if p.name() == 'LeagueClientUx.exe':
                process = p
        if process is None:
            print("Client was not found to be open.")
            self.root.destroy()
            return

        for arg in process.cmdline():
            if len(arg) > 0 and '=' in arg:
                key, value = arg[2:].split('=', 1)
                process_args[key] = value

        self.session.auth = ('riot', process_args['remoting-auth-token'])
        self.url = f"https://127.0.0.1:{int(process_args['app-port'])}"

        print(self.request('get', '/lol-summoner/v2/summoner-names').json())

    def load_fields(self):
        self.username.config(text=self.request('get', '/lol-chat/v1/me').json()['gameName'])
        self.status.insert(tk.END,self.request('get', '/lol-chat/v1/me').json()['statusMessage'])

    def request(self, method: str, endpoint: str, **kwargs):
        url = self.url
        if 'path' in kwargs:
            url = url.format(**kwargs['path'])
            kwargs.pop('path')
        if kwargs.get('data'):
            kwargs['data'] = json.dumps(kwargs['data'])

        return self.session.request(method, f'{url}{endpoint}', verify=False, **kwargs)

    def change_status(self):
        print(f'Setting status to: {self.status.get()}')
        print(self.request('put', '/lol-chat/v1/me', data={'statusMessage': self.status.get()}))

    def on_click(self, event):
        if self.focus == self.root.focus_get():
            self.root.focus_set()
        if self.focus != self.root.focus_get() and str(self.focus) != '.':
            self.change_status()
        self.focus = self.root.focus_get()

        print(event)
        print(self.clicked)
        print()
        if (self.clicked is None):
            self.close_popups()
        self.clicked = None

    def click_popup(self, event):
        self.clicked = event

    def close_popups(self):
        for p in self.popups:
            p.place_forget()


urllib3.disable_warnings() # Not sure if I should get certification or not
App()