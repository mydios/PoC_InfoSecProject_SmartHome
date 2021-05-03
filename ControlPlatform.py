from CommunicationInterface import CommunicationInterface
from ControlPlatformReceiverThread import ControlPlatformReceiverThread
from Messages.StateUpdateMessage import StateUpdateMessage
from Messages.DeviceCommandMessage import DeviceCommandMessage
from collections import defaultdict

import os


class ControlPlatform(CommunicationInterface):
    """
        A ControlPlatform instance is a class that has the CommunicationInterface and thus communicates using 
        this interface via the network.py script which contains a Broker instance. Its initialization requires:

            - initialization parameters of CommunicationInterface:  addr=('localhost', int); name=str; pw=str; encryption_type=str; 
                                                                    encryption_args=list


        Because this class supports user input via the command console, this class uses to threads that mangage the 
        CommunicationInterface functionality. These threads is a ControlPlatformReceiverThread instance. 
    """

    def __init__(self, addr, name, pw='strong_password'):
        super().__init__(addr, name, pw, encryption_type="conrol_platform", encryption_args=[])
        # a dictionary to keep track of all registered devices and their relevant information
        # dict(str: list)
        # dict(device_name: [device_states, command_manual, encryption_type, encryption_args])
        self.registered_devices = {}

        # a dictionary to keep track of all registered control applications and their relevant information
        # dict(str: list)
        # dict(application_name: [encryption_type, encryption_args])
        self.registered_control_applications = {}

        # a dictionary to assign authorisation levels, device updates are allowed if auth[device] >= auth[application]
        # 0 = very restricted device OR unrestricted application(admin)
        self.authorisation_level = defaultdict(lambda:0)

        # thread that manages all incoming messages
        self.thread = ControlPlatformReceiverThread(self)

    def register_device(self, device_name, command_manual, encryption_type, encryption_args):
        """
        Function that handles an incoming RegisterDeviceMessage. Used by ControlPlatformReceiverThread

        """
        # First field in tuple is reserved for the state information (upon registration no state information has been received yet)
        self.registered_devices[device_name] = [
            None, command_manual, encryption_type, encryption_args]

    def register_control_application(self, application_name, credentials, authorisation_level, encryption_type, encryption_args):
        """
        Function that handles an incoming RegisterControlApplicationMessage. Used by ControlPlatformReceiverThread

        """
        # check if the application has the right credentials
        if credentials == "Password":
            self.registered_control_applications[application_name] = [
                encryption_type, encryption_args]
            self.authorisation_level[application_name] = authorisation_level
        else:
            print("Application '" + application_name + "' dropped: wrong credentials")

    def handle_state_update(self, message):
        """
        Function that handles an incoming StateUpdateMessage. Used by ControlPlatformReceiverThread

        """
        # update local information
        self.registered_devices[message.device_name][0] = message.device_states
        # pass on StateUpdateMessage to all registered ControlApplication instances
        for ca in self.registered_control_applications:
            self.post_message(message, ca)

    def handle_device_command(self, message):
        """
        Function that handles an incoming DeviceCommandMessage. Used by ControlPlatformReceiverThread

        """
        # Check if the command that the ControlApplication instance has issued, is valid
        manual_of_device = self.registered_devices[message.device_name][1]
        valid_state_values = [t[0]
                              for t in manual_of_device[message.device_state_name]]
        valid_command = (message.device_state_name in manual_of_device.keys()) and (
            message.device_state_value in valid_state_values)

        # Check if the user is authorised
        if self.authorisation_level[message.device_name] < self.authorisation_level[message.commander]:
            print("Application '" + message.commander + "' not authorised to use device '" + message.device_name + "'")
            valid_command = False

        if valid_command:
            self.post_message(message, message.device_name)

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

            # GET THE CURRENT REGISTERED DEVICES
            if u_in == 'print_registered_devices':
                for device in self.registered_devices:
                    print(device)
                continue

            # GET THE CURRENT REGISTERED CONTROL APPLICATIONS
            if u_in == 'print_registered_control_applications':
                for ca in self.registered_control_applications:
                    print(ca)
                continue

            print("Unrecognized command")
