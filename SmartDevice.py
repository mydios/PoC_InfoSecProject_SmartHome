from CommunicationInterface import CommunicationInterface
from Messages.RegisterDeviceMessage import RegisterDeviceMessage
from DeviceReceiverThread import DeviceReceiverThread
from DeviceSenderThread import DeviceSenderThread

import threading
import os


class SmartDevice(CommunicationInterface):
    def __init__(self, addr, name, command_manual, start_states, control_platform_name, pw='strong_password'):
        super().__init__(addr, name, pw)
        # command_manual = dictionary(str:list((int, str))) = dictionary(state_name:list((state_value, value_name)))
        # dictionary of states with a corresponding list of accepted values which are integers and can have a valuename (e.g. ON, OFF...)
        self.command_manual = command_manual

        # start_states = dict string state_name : 2-tuple (int, str)=(state_value, value_name)
        self.device_states = start_states
        self.state_semaphore = threading.Semaphore()

        # string
        self.control_name = control_platform_name

        # threads for sending updates about state and receiving messages to/from control platform
        self.t_s = DeviceSenderThread(self.control_name, self)
        self.t_r = DeviceReceiverThread(self)

    def _change_state(self, state_name, state_value):

        for ps in self.command_manual[state_name]:
            if ps[0] == state_value:
                self.state_semaphore.acquire()
                self.device_states[state_name] = ps
                self.state_semaphore.release()
                return True
        return False

    def _register(self):
        # THE ENCRYPTION SUPPORTED BY THIS DEVICE IS INCORPORATED IN THE REGISTER MESSAGE
        content = RegisterDeviceMessage(
            self.name, self.command_manual, self.encryption_type, self.encryption_args)
        self.post_message(message=content, destination=self.control_name)

    def start(self):
        try:
            os.system('clear')
        except:
            pass
        # register with control platform
        self._register()
        # start send/receive threads (will only work when control platform and control application have been implemented)
        # self.t_r.start()
        # self.t_s.start()
        while True:
            u_in = input('')
            if u_in == 'clear':
                try:
                    os.system('clear')
                    continue
                except:
                    pass
            if u_in == 'exit':
                exit()

            if u_in == 'print_states':
                print("Current states: ")
                for state in self.device_states.keys():
                    print('\t'+state+': '+str(self.device_states[state]))
                print("")
                continue
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


d = SmartDevice(('localhost', 10001), 'lamp', {'state': [(1, "ON"), (False, "OFF")], 'color': [
                (0, "WHITE"), (1, "RED"), (2, "GREEN")]}, {'state': (0, "OFF"), 'color': (1, "RED")}, "control_platform_name")
d.start()
