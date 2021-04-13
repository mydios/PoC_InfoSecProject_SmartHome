from CommunicationInterface import CommunicationInterface
from Messages.RegisterDeviceMessage import RegisterDeviceMessage
from DeviceReceiverThread import DeviceReceiverThread
from DeviceSenderThread import DeviceSenderThread

import threading
import os


class SmartDevice(CommunicationInterface):
    """
        A SmartDevice instance is a class that has the CommunicationInterface and thus communicates using 
        this interface via the network.py script which contains a Broker iinstance. Its initialization requires:

            - initialization parameters of CommunicationInterface:  addr=('localhost', int); name=str; pw=str; encryption_type=str; 
                                                                    encryption_args=list

            - command_manual =          dict(str:list((int, str)))
                                        dictionary of names of the internal states of this device with a corresponding list 
                                        of accepted values which are integers and can have a valuename (e.g. ON, OFF...).
                                        'dictionary(state_name:list((state_value, value_name)))'

            - start_states =            dict(str:(int, str)) where key:value represents state_name : (state_value, value_name)
                                        dictionary of intial states of SmartDevice upon creation. The initial states mus be conform
                                        the command_manual

            - control_platform_name =   str
                                        name of the ControlPlatform instance that this SmartDevice will register with. It sends its
                                        command_manual to this ControlPlatform instance to inform it of its offered services

        Because this class supports user input via the command console, this class uses to threads that mangage the 
        CommunicationInterface functionality. These threads are respectively instances of the DeviceSenderThread and the 
        DeviceReceiverThread classes. 
    """

    def __init__(self, addr, name, command_manual, start_states, control_platform_name, pw='strong_password', encryption_type="no_encryption", encryption_args=[]):
        super().__init__(addr, name, pw, encryption_type, encryption_args)
        # command_manual
        self.command_manual = command_manual
        self.device_states = start_states

        # a semaphore used to perform thread-safe state transitions
        self.state_semaphore = threading.Semaphore()

        # control_name is the name of the ControlPlatform this device registers with
        self.control_name = control_platform_name

        # threads for CommunicationInterface functionality
        self.t_s = DeviceSenderThread(self.control_name, self)
        self.t_r = DeviceReceiverThread(self)

    def _change_state(self, state_name, state_value):
        """
        This function changes the internal state of this device in a thread-safe manner. It requires
        the following arguments:
            - state_name =      str
                                the name of the state that needs to be changed
            - state_value =     int
                                the new state value
        These arguments must conform to the command_manual for any change to take effect.
        """
        for ps in self.command_manual[state_name]:
            if ps[0] == state_value:
                self.state_semaphore.acquire()
                self.device_states[state_name] = ps
                self.state_semaphore.release()
                return True
        return False

    def _register(self):
        """
        This function sends the enregistrement message to the ControlPlatform instance that this device
        is registered with. The message contains all necessary information for the ControlPlatform and the SmartDevice
        to communicate in the future.
        """
        # THE ENCRYPTION SUPPORTED BY THIS DEVICE IS INCORPORATED IN THE REGISTER MESSAGE
        content = RegisterDeviceMessage(
            self.name, self.command_manual, self.encryption_type, self.encryption_args)
        self.post_message(message=content, destination=self.control_name)

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
        # start send/receive threads
        self.t_r.start()
        self.t_s.start()

        # CLI
        while True:
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
            # GET THE CURRENT INTERNAL STATE OF THE DEVICE
            if u_in == 'print_states':
                print("Current states: ")
                for state in self.device_states.keys():
                    print('\t'+state+': '+str(self.device_states[state]))
                print("")
                continue
            # GET A LISTING OF THE STATES AND SUPPORTED STATE VALUES
            if u_in == 'get_command_manual':
                print('\tstate names | possible values')
                for key in self.command_manual.keys():
                    s = '\t' + key + ', ' + str(self.command_manual[key])
                    print(s)
                print("")
                continue
            # SET A STATE
            l = u_in.split(' ')
            if len(l) == 3 and l[0] == 'set_state':
                if l[1] in self.command_manual.keys():
                    if l[2].isnumeric():
                        ret = self._change_state(l[1], int(l[2]))
                        if ret:
                            s = 'set state ' + l[1] + ' to ' + l[2]
                            print(s)
                            print("")
                            continue
            print("Unrecognized command")
            print("")


"""
d = SmartDevice(('localhost', 10001), 'lamp', {'state': [(1, "ON"), (False, "OFF")], 'color': [
                (0, "WHITE"), (1, "RED"), (2, "GREEN")]}, {'state': (0, "OFF"), 'color': (1, "RED")}, "control_platform_name")
d.start()
"""
