from CommunicationInterface import CommunicationInterface
from KAuthServerReceiverThread import KAuthServerReceiverThread
from Messages.KAuthResponseMessage import KAuthResponseMessage

import os
import time


class KAuthServer(CommunicationInterface):
    """
    
    """
    def __init__(self, addr, name):
        super().__init__(addr, name)
        # database (dictionary) with user access rights: {user_id : is_allowed}
        # admin_id = 0
        self.db = {0: True}
        
        # thread that manages all incoming messages
        self.thread = KAuthServerReceiverThread(self)
      
    def handle_auth_request(self, sender, request):
        try:
            client_id = request.client_id
            
            if self.db[client_id]: # check if this client has access rights
                
                nonce = request.nonce
                tgs_id = request.tgs_id
                tgs_session_key = self.generate_session_key()
                
                tgt = self.encrypt_asymm(None, { # TO ENCRYPT WITH PUBLIC KEY OF TGS
                        'flag': 0,
                        'session_key': tgs_session_key,
                        'client_realm': '',
                        'client_id': client_id,
                        'client_address': sender,
                        'times': ''
                        })
    
                session_data = self.encrypt_asymm(None, { # TO ENCTYPT WITH PUBLIC KEY OF CLIENT
                        'session_key': tgs_session_key,
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
    
    def generate_session_key(self):
        # TO DO
        time.sleep(0.5)
        return 'deadbeef'
    
    def encrypt_asymm(self, key, data):
        # TO DO
        return str(data).encode('utf-8').hex()
    
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