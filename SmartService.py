from CommunicationInterface import CommunicationInterface
from ServiceReceiverThread import ServiceReceiverThread
from Messages.KServiceResponseMessage import KServiceResponseMessage
from Encryption import stringToKey, encrypt_symm, decrypt_symm
import os


class SmartService(CommunicationInterface):
    """
    SmartService contains data that can be retrieved or updated by a client (= ControlApplication).
    Kerberos is used to authenticate the client.
    """
    def __init__(self, addr, name, service_id, data):
        super().__init__(addr, name)
        
        self.data = data
        
        # Kerberos
        ###########
        
        self.service_id = service_id # id of the service
        
        # dictionary with connection data per client
        # {client_id : {subkey, sequence_nr}}
        self.clients = {}

        self.secret_key = stringToKey("Service Password")
        
        ###########
        
        # thread that manages all incoming messages
        self.thread = ServiceReceiverThread(self)
    
    # Kerberos
    ##################################################
    
    def handle_service_request(self, sender, request):
        """
        Client/server dialogue, slide 26 (--> V)
        + slide 27 (V -->)
        """
        # CHANGE
        sgt = decrypt_symm(self.secret_key, request.sgt) # TO DECRYPT WITH SECRET KEY BETWEEN Service - TGS
        client_address = sgt['client_address']
        
        if client_address == sender: # check if sender address is correct
            sg_session_key = sgt['session_key']
            session_data = decrypt_symm(sg_session_key, request.auth_data) # TO DECRYPT WITH SYMMETRIC SERVICE-GRANTING SESSION KEY
            client_id = sgt['client_id']
            
            if client_id == session_data['client_id']: # check if client id is correct              
                self.clients[client_id] = {
                        'subkey': session_data['subkey'],
                        'sequence_nr': session_data['sequence_nr']
                        }
    
                auth_data = encrypt_symm(sg_session_key, { # TO ENCRYPT WITH SYMMETRIC SERVICE-GRANTING SESSION KEY
                        'timestamp': session_data['timestamp'],
                        'subkey': session_data['subkey'],
                        'sequence_nr': session_data['sequence_nr'],
                        'data': self.data
                        })
                
                response = KServiceResponseMessage(auth_data)
                self.post_message(response, sender)
                
            else:
                # client id incorrect, ignore message
                pass
        else:
            # sender address incorrect, ignore message
            pass
    
    ##################################################

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