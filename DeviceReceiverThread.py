from threading import Thread
from Messages.DeviceCommandMessage import DeviceCommandMessage

class DeviceReceiverThread(Thread):
    """
    Initialization requires:
        - dvc =     SmartDevice instance
                    The SmartDevice instance for which this thread is performing the receive functionality
    """
    def __init__(self, dvc):
        super().__init__(daemon=True)
        self.device = dvc
    
    def run(self):
        while True:
            #Receive DeviceCommandMessage messages to change on of the internal states of the device
            #All other messages are dropped and in this case something is printed to the terminal
            tpl = self.device.receive_message()
            message = tpl[1]
            if type(message).__name__ != "DeviceCommandMessage":
                print("Received a message that should nog arrive at "+self.device.name)
                continue
            if message.device_name != self.device.name:
                print("Received a message that should nog arrive at "+self.device.name)
                continue
            self.device._change_state(message.device_state_name, message.device_state.state_value)

