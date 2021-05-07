from CommunicationInterface import CommunicationInterface
from KAuthServerReceiverThread import KAuthServerReceiverThread
from Messages.KAuthResponseMessage import KAuthResponseMessage
from Encryption import stringToKey, encrypt_symm, generate_session_key

import os


class KAuthServer(CommunicationInterface):
    """
    Kerberos Authentication Server (AS) + Database.
    """
    def __init__(self, addr, name):
        super().__init__(addr, name)
        # database (dictionary) with user access rights: {user_id : is_allowed}
        # admin_id = 0
        self.db = {0: True}

        # dictionary of secret keys for each client: {user_id : key}
        key = stringToKey("Password")
        self.client_secret_key = {0: key}

        # TGS secret key
        self.tgs_secret_key = stringToKey("TGS_key")
        
        # thread that manages all incoming messages
        self.thread = KAuthServerReceiverThread(self)
      
    def handle_auth_request(self, sender, request):
        """
        Authentication dialogue, slide 22 (--> AS)
        + slide 23 (AS -->)
        """
        try:
            client_id = request.client_id
            
            if self.db[client_id]: # check if this client has access rights
                
                nonce = request.nonce
                tgs_id = request.tgs_id
                tg_session_key = generate_session_key()

                # CHANGE
                tgt = encrypt_symm(self.tgs_secret_key, { # TO ENCRYPT WITH SECRET KEY BETWEEN TGS - AuthS
                        'flag': 0,
                        'session_key': tg_session_key,
                        'client_realm': '',
                        'client_id': client_id,
                        'client_address': sender,
                        'times': ''
                        })

                # CHANGE
                session_data = encrypt_symm(self.client_secret_key[client_id], { # TO ENCRYPT WITH SECRET KEY BETWEEN Client - AuthS
                        'session_key': tg_session_key,
                        'times': '',
                        'nonce': nonce,
                        'tgs_realm': '',
                        'tgs_id': tgs_id
                        })
                
                response = KAuthResponseMessage('', client_id, tgt, session_data)
                self.post_message(response, sender)
                
            else:
                # client does not have access rights, ignore message
                pass
            
        except KeyError:
            # client is not known in db, ignore message
            pass


    def start(self):
        try:
            os.system('clear')
        except:
            try:
                os.system('cls')#WINDOWS
            except:
                pass
            pass
        # Receiver thread
        self.thread.start()

        # CLI
        while True:
            print("")
            u_in = input('')

            # CLEAR THE CONSOLE
            if u_in == 'clear':
                try:
                    os.system('clear')
                    continue
                except:
                    try:
                        os.system('cls')#WINDOWS
                    except:
                        pass
                    pass
            # SHUT DOWN THE DEVICE
            if u_in == 'exit':
                exit()

            print("Unrecognized command")