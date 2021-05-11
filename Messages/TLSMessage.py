CLIENT_HELLO = 0
SERVER_HELLO = 1
ENCRYPTED_EXTENSIONS = 2
CERTIFICATE_REQUEST = 3
CERTIFICATE = 4
CERTIFICATE_VERIFY = 5
FINISH_S = 6
FINISH_C = 7
ENCRYPTED_DATA= 8
types = {0: "CLIENT_HELLO", 1:"SERVER_HELLO", 2:"ENCRYPTED_EXTENSIONS",
         3: "CERTIFICATE_REQUEST", 4: "CERTIFICATE",
         5: "CERTIFICATE_VERIFY", 6: "FINISH",
         7: "FINISH_C", 8: "ENCRYPTED_DATA"}


class TLSMessage():
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop("type")
        self.source = kwargs.pop("source")
        if self.type == CLIENT_HELLO:
            self.client_random_data = kwargs.pop("client_random_data")
            self.cipher_suites = kwargs.pop("cipher_suites")
            self.public_key = kwargs.pop("public_key")
            self.supported_versions = kwargs.pop("supported_versions")
        elif self.type == SERVER_HELLO:
            self.server_random_data = kwargs.pop("server_random_data")
            self.selected_cipher = kwargs.pop("selected_cipher")
            self.public_key = kwargs.pop("public_key")
            self.chosen_version = kwargs.pop("chosen_version")
        else:
            self.encrypted_data = kwargs.pop("encrypted_data")
        
    def __str__(self):
        to_return =  f'{type(self).__name__}|TYPE={types[self.type]}' 
        if self.type == CLIENT_HELLO:
            to_return += f'|CLIENT_RANDOM_DATA={self.client_random_data}|CIPHER_SUITES={self.cipher_suites}|PUBLIC_KEY={self.public_key}|SUPPORTED_VERSIONS={self.supported_versions}'
        elif self.type == SERVER_HELLO:
            to_return += f'|SERVER_RANDOM_DATA={self.server_random_data}|SELECTED_CIPHER={self.selected_cipher}|PUBLIC_KEY={self.public_key}|CHOSEN_VERSION={self.chosen_version}'
        else:
            to_return += f'|DATA={self.encrypted_data}'

        return to_return
    def __repr__(self):
        return self.__str__()