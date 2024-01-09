import tkinter as tk
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

        self.root = tk.Tk()

        self.root.geometry("1280x720")
        self.root.title("Ultra_Dagon's League Client Project")

        self.social = tk.Frame(self.root, bg="#9999cc")

        self.username = tk.Label(self.social, text="%username", font=('Arial, 18'))
        self.username.pack()

        self.status = tk.Entry(self.social, font=('Arial, 18'))
        self.status.pack()

        self.set_status = tk.Button(self.social, text="Set Status", font=('Arial, 18'), command=self.change_status)
        self.set_status.pack()

        self.social.pack(side=tk.RIGHT, fill=tk.Y)

        self.navigation_bar = tk.Frame(self.root, bg="#ccccff") #11 tabs

        self.play_party = tk.Button(self.navigation_bar, text="Play", font=('Arial, 18'))
        self.play_party.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.home = tk.Button(self.navigation_bar, text="Home", font=('Arial, 18'))
        self.home.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.navigation_bar.pack(side=tk.TOP, fill=tk.X)

        #self.connect_button = tk.Button(self.root, text="Connect", font=('Arial, 60'), command=lambda: [self.connect, self.connect_button.place_forget])
        #self.connect_button.place(relx=0.3, rely=0.3, relheight=.4, relwidth=.4)
        self.connect()
        self.load_fields()
        self.root.mainloop()

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

        print(self.request('get', '/lol-summoner/v1/current-summoner/summoner-profile'))

    def load_fields(self):
        self.status.insert(0,self.request('get', '/lol-chat/v1/me').json()['statusMessage'])

    def request(self, method: str, endpoint: str, **kwargs):
        url = self.url
        if 'path' in kwargs:
            url = url.format(**kwargs['path'])
            kwargs.pop('path')
        if kwargs.get('data'):
            kwargs['data'] = json.dumps(kwargs['data'])

        return self.session.request(method, f'{url}{endpoint}', verify=False, **kwargs)

    def change_status(self):
        print(self.status.get())
        print(self.request('put', '/lol-chat/v1/me', data={'statusMessage': self.status.get()}))

urllib3.disable_warnings() # Not sure if I should get certification or not
App()