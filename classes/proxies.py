import os

class Proxies:

    proxy_file_name = None
    _hostname = None
    _port= None
    __proxy_list = []

    def load_proxy_list(self):
        try:
            with open(self.proxy_file_name) as f:
                self.__proxy_list = f.readlines()
            self.trim_values()
            return self.__proxy_list
        except NameError:
            print(NameError)
    
    def trim_values(self):
        try:
            for i in range(0, len(self.__proxy_list)):
                self.__proxy_list[i] = self.__proxy_list[i].strip()
        except NameError:
            print(NameError)

    def check_proxies_file(self):
        try:
            current_directory = os.getcwd()
            file_name = "proxies.txt"
            file_path = os.path.join(current_directory, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w'):
                    pass
            self.proxy_file_name = file_name
        except NameError:
            pass

