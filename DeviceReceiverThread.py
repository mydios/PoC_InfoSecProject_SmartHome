from threading import Thread
from Messages.DeviceCommandMessage import DeviceCommandMessage

class DeviceReceiverThread(Thread):
    def __init__(self, dvc):
        super().__init__(daemon=True)
        self.device = dvc
    
    def run(self):
        while True:
            #SEND A STATE UPDATE OF THE DEVICE TO THE CONTROL PLATFORM EVERY 60 seconds
            tpl = self.device.receive_message()
            message = tpl[1]
            if type(message).__name__ != "DeviceCommandMessage":
                print("Received a message that should nog arrive at "+self.device.name)
                continue
            if message.device_name != self.device.name:
                print("Received a message that should nog arrive at "+self.device.name)
                continue
            self.device._change_state(message.device_state_name, message.device_state.state_value)

