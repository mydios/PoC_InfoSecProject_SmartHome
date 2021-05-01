from CommunicationInterface import CommunicationInterface
from Messages.RegisterControlApplicationMessage import RegisterControlApplicationMessage
from Messages.DeviceCommandMessage import DeviceCommandMessage
from ControlApplicationReceiverThread import ControlApplicationReceiverThread

from threading import Semaphore
import os
import time
import uuid


class ControlApplication(CommunicationInterface):
    """
        A ControlApplication instance is a class that has the CommunicationInterface and thus communicates using 
        this interface via the network.py script which contains a Broker instance. Its initialization requires:

            - initialization parameters of CommunicationInterface:  addr=('localhost', int); name=str; pw=str; encryption_type=str; 
                                                                    encryption_args=list

            - control_platform_name :                               str
                                                                    name of the ControlPlatform instance that this 
                                                                    ControlApplication instance will register with. 
    """

    def __init__(self, addr, name, control_platform_name="control_platform", pw='strong_password', encryption_type="no_encryption", encryption_args=[]):
        super().__init__(addr, name, pw, encryption_type, encryption_args)
        self.control_name = control_platform_name

        self.devices_information = {}

        self.semaphore = Semaphore()
        
        # Kerberos
        self.client_id = 0
        self.tgs_id = 1

        self.thread = ControlApplicationReceiverThread(self)

    def _register(self):
        """
        This function sends the enregistrement message to the ControlPlatform instance that this ControlApplication instance
        is registered with. The message contains all necessary information for the ControlPlatform and the ControlApplication
        to communicate in the future.
        """
        # THE ENCRYPTION SUPPORTED BY THIS DEVICE IS INCORPORATED IN THE REGISTER MESSAGE
        content = RegisterControlApplicationMessage(
            self.name, self.encryption_type, self.encryption_args)
        self.post_message(message=content, destination=self.control_name)

    def update_device_state(self, device_name, new_states):
        """
        Function that updates the state values of a single device. Used by ControlApplicationReceiverThread 

        """
        self.semaphore.acquire()
        self.devices_information[device_name] = new_states
        self.semaphore.release()

    def command_device(self, device_name, state_name, new_state_value):
        """
        Function that posts a command to a certain device. Used in the CLI of this process.

        """
        message = DeviceCommandMessage(
            device_name, state_name, new_state_value, self.name)
        self.post_message(message, self.control_name)

    def handle_auth_response(self, message):
        session_data = self.decode(None, message.session_data) # TO DECTYPT WITH PRIVATE KEY OF CLIENT
        
        if session_data['tgs_id'] == self.tgs_id and session_data['nonce'] == self.nonce: # check nonce to avoid replay attacks
            self.tgt = message.tgt
            self.tgs_session_key = session_data['session_key']
            
        else:
            # invalid or old nonce, ignore message
            pass
    
    def generate_nonce(self):
        # https://stackoverflow.com/questions/5590170/what-is-the-standard-method-for-generating-a-nonce-in-python
        return uuid.uuid4().hex
    
    def decode(self, key, data):
        # TO DO
        time.sleep(0.5)
        # don't use eval in final version
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
        # register with control platform
        self._register()
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

            # GET THE CURRENT INFORMATION OF THE DEVICES
            if u_in == 'print_devices':
                for device in self.devices_information:
                    print(device + ' : ' +
                          str(self.devices_information[device]))
                print("")
                continue

            # SET A STATE
            # set_state device_name state_name state_value
            l = u_in.split(' ')
            correct_command = True
            correct_command *= len(l) == 4
            if not correct_command:
                print("Unrecognized command")
                continue
            correct_command *= l[0] == 'set_state'
            correct_command *= l[3].isnumeric()
            if not correct_command:
                print(
                    "Please use the following command structure: set_state device_name state_name state_value")
                continue
            l[3] = int(l[3])
            self.command_device(l[1], l[2], l[3])
