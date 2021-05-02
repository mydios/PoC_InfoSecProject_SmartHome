from CommunicationInterface import CommunicationInterface
from KTicketGServerReceiverThread import KTicketGServerReceiverThread
from Messages.KTicketResponseMessage import KTicketResponseMessage

import os
import time


class KTicketGServer(CommunicationInterface):
    """
    
    """
    def __init__(self, addr, name):
        super().__init__(addr, name)
        
        # thread that manages all incoming messages
        self.thread = KTicketGServerReceiverThread(self)
      
    def handle_ticket_request(self, sender, request):
        tgt = self.decrypt_asymm(None, request.tgt) # TO DECRYPT WITH PRIVATE KEY OF TGS
        tgs_session_key = tgt['session_key']
        client_address = tgt['client_address']
        if client_address == sender: # check if sender address is correct
            auth_data = self.decrypt_symm(tgs_session_key, request.auth_data) # TO DECTYPT WITH SYMMETRIC TGS SESSION KEY
            client_id = tgt['client_id']
            
            if client_id == auth_data['client_id']: # check if client id is correct
                service_id = request.service_id
                nonce = request.nonce
                service_session_key = self.generate_session_key()
                
                sgt = self.encrypt_asymm(None, { # TO ENCRYPT WITH PUBLIC KEY OF SERVICE
                        'flag': '',
                        'session_key': service_session_key,
                        'realm': '',
                        'client_id': client_id,
                        'client_address': client_address,
                        'times': ''
                        })
    
                session_data = self.encrypt_symm(tgs_session_key, { # TO ENCRYPT WITH SYMMETRIC TGS SESSION KEY
                        'session_key': service_session_key,
                        'times': '',
                        'nonce': nonce,
                        'server_realm': '',
                        'service_id': service_id
                        })
                
                response = KTicketResponseMessage('', client_id, sgt, session_data)
                self.post_message(response, sender)
                
            else:
                # client id incorrect, ignore message
                pass
        else:
            # sender address incorrect, ignore message
            pass
    
    def generate_session_key(self):
        # TO DO
        time.sleep(0.5)
        return 'deadbeef'
    
    def encrypt_symm(self, key, data):
        # TO DO
        return str(data).encode('utf-8').hex()
    
    def encrypt_asymm(self, key, data):
        # TO DO
        return str(data).encode('utf-8').hex()
    
    def decrypt_symm(self, key, data):
        # TO DO
        # don't use eval in final version, not safe
        return eval(bytes.fromhex(data).decode('utf-8'))
    
    def decrypt_asymm(self, key, data):
        # TO DO
        # don't use eval in final version, not safe
        return eval(bytes.fromhex(data).decode('utf-8'))
    
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