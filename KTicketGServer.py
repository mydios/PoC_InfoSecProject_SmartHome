from CommunicationInterface import CommunicationInterface
from KTicketGServerReceiverThread import KTicketGServerReceiverThread
from Messages.KTicketResponseMessage import KTicketResponseMessage
from Encryption import encrypt_symm, decrypt_symm, generate_session_key, stringToKey

import os


class KTicketGServer(CommunicationInterface):
    """
    Kerberos Ticket-Granting Server (TGS).
    """
    def __init__(self, addr, name):
        super().__init__(addr, name)
        
        # thread that manages all incoming messages
        self.thread = KTicketGServerReceiverThread(self)

        # dictionary of secret keys for each service: {service_id : key}
        key = stringToKey("Service Password")
        self.client_secret_key = {15 : key}

        # TGS secret key
        self.tgs_secret_key = stringToKey("TGS_key")
      
    def handle_ticket_request(self, sender, request):
        """
        TGS dialogue, slide 24 (--> TGS)
        + slide 25 (TGS -->)
        """
        # CHANGE
        tgt = decrypt_symm(self.tgs_secret_key, request.tgt) # TO DECRYPT WITH SECRET KEY BETWEEN AuthS - TGS

        client_address = tgt['client_address']
        
        if client_address == sender: # check if sender address is correct
            tg_session_key = tgt['session_key']
            auth_data = decrypt_symm(tg_session_key, request.auth_data) # TO DECRYPT WITH SYMMETRIC TICKET-GRANTING SESSION KEY
            client_id = tgt['client_id']
            
            if client_id == auth_data['client_id']: # check if client id is correct
                service_id = request.service_id
                nonce = request.nonce
                sg_session_key = generate_session_key()

                # CHANGE
                sgt = encrypt_symm(None, { # TO ENCRYPT WITH SECRET KEY BETWEEN Service - TGS
                        'flag': '',
                        'session_key': sg_session_key,
                        'realm': '',
                        'client_id': client_id,
                        'client_address': client_address,
                        'times': ''
                        })
    
                session_data = encrypt_symm(tg_session_key, { # TO ENCRYPT WITH SYMMETRIC TICKET-GRANTING SESSION KEY
                        'session_key': sg_session_key,
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