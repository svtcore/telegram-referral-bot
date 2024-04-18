class Tokens:

    tokens_file_name = None
    __token_list = []

    def load_token_list(self):
        try:
            with open(self.tokens_file_name) as f:
                self.__token_list = f.readlines()
            self.__trim_values()
            return self.__token_list
        except NameError:
            print(NameError)
    
    def __trim_values(self):
        try:
            for i in range(0, len(self.__token_list)):
                self.__token_list[i] = self.__token_list[i].strip()
        except NameError:
            print(NameError)

