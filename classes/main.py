from pyrogram import Client
from pyrogram.raw import functions
import random
import time
from classes.proxies import Proxies
from classes.tokens import Tokens
from classes.auth import Auth
import os.path


class Main(Proxies, Tokens):

    #session field
    app = None
    #name of bot
    target_name = None 
    #how many account will be use
    count = None
    #referral id 
    refer = None
    #time in seconds from/ to do delay between actiion 
    delay_min = None
    delay_max = None
    join_channel = None
    channel_name = None


    def __init__(self, target_name, count, join_channel, channel_name, delay_min, delay_max, refer, tokens_filename, proxies_filename) -> None:
        self.target_name = target_name
        self.count = int(count)
        self.refer = refer
        self.delay_min = int(delay_min)
        self.delay_max = int(delay_max)
        self.join_channel = join_channel
        self.channel_name = channel_name
        Tokens.tokens_file_name = tokens_filename
        #if proxies file not defined then create default and use no proxy mode
        if (not proxies_filename):
            Proxies.check_proxies_file(self)
        else:
            Proxies.proxy_file_name = proxies_filename

    def check_sessions_folder(self):
        try:
            current_directory = os.getcwd()
            folder_name = "sessions"
            sessions_folder_path = os.path.join(current_directory, folder_name)
            if not os.path.exists(sessions_folder_path):
                os.makedirs(sessions_folder_path)
        except(NameError):
            pass

    def start(self):
        self.start_target_bot()
    
    def start_target_bot(self):
        try:
            counter = 0
            proxies = super().load_proxy_list()
            tokens = super().load_token_list()
            if (len(tokens) >= int(self.count)):
                for i in range(0, self.count):
                    token = tokens[i].split(":")
                    if len(proxies) > 0 and proxies[i] != None:
                        proxy = proxies[i].split(":")
                        if len(proxy) == 4 and len(token) == 3:
                            self.connect(token[0], token[1], token[2], proxy[0], proxy[1], proxy[2], proxy[3])
                        elif len(proxy) == 2 and len(token) == 3:
                            self.connect(token[0], token[1], token[2], proxy[0], proxy[1], None, None)
                        elif len(proxy) == 0 and len(token) == 3:
                            self.connect(token[0], token[1], token[2], None, None, None, None)
                        else:
                            continue
                    else:
                        if len(token) == 3:
                            self.connect(token[0], token[1], token[2], None, None, None, None)
                        else:
                            continue
                    self.app.connect()
                    #check if join to channel function enabled then process it
                    if (self.join_channel != None and self.channel_name != None):
                        if (self.join_to_channel()):
                            print("[Session: " + token[0] + "] has been joined to channel @" + str(self.channel_name))
                    if (self.start_bot()):
                        print("[Session: " + token[0] + "] has been sent start command")
                        counter = counter + 1
                    else:
                        print("[Session: " + token[0] + "] has NOT been sent start command")
                    self.app.disconnect()
                    #checking last element to avoid sleep time after proccessing last element
                    if i != self.count-1:
                        rnd = random.randrange(self.delay_min, self.delay_max)
                        print("Waiting " + str(rnd) + " seconds")
                        time.sleep(rnd)
            else:
                print("Not enough tokens in file")
            print("Sent " + str(counter) + "/" + str(self.count))
        except NameError:
            pass

    def connect(self, session_name, api_id, api_hash, ip, port, username, password):
        try:
            #proxy with authentication
            if ip != None and port != None and username != None and password != None:
                self.app = Client(name="./sessions/" + session_name, api_id=api_id, api_hash=api_hash, proxy=dict(hostname=ip, port=int(port), username=username, password=password))
            #public proxy
            elif ip != None and port != None:
                self.app = Client(name="./sessions/" + session_name, api_id=api_id, api_hash=api_hash, proxy=dict(hostname=ip, port=int(port)))
            #without authentication
            else:
                self.app = Client(name="./sessions/" + session_name, api_id=api_id, api_hash=api_hash)
            return 1
        except NameError:
            return 0

    def join_to_channel(self):
        try:
            target_channel = self.app.resolve_peer(self.channel_name)
            join_result = self.app.invoke(
                    functions.channels.JoinChannel(
                    channel=target_channel)
                )
            if (join_result.chats[0].username == self.channel_name):
                return 1
            else:
                return 0
        except(NameError):
            return 0

    def start_bot(self):
        try:
            #define target
            self.target = self.app.resolve_peer(self.target_name)
            self.app.invoke(
                    functions.messages.StartBot(
                    bot = self.target,
                    peer = self.target, 
                    random_id=random.randint(100000,999999),
                    start_param = self.refer)
                )
            return 1
        except NameError:
            return 0