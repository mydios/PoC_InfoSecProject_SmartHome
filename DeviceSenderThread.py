from Messages.StateUpdateMessage import StateUpdateMessage

from threading import Thread
import time

class DeviceSenderThread(Thread):
    """
    Initialization requires:
        - dvc =     SmartDevice instance
                    The SmartDevice instance for which this thread is performing the receive functionality
        
        - dest =    str
                    The communication name of the ControlPlatform instance that this SmartDevice is sending updates to
    """
    def __init__(self, dest, dvc):
        super().__init__(daemon=True)
        self.device = dvc
        self.destination = dest
    
    def run(self):
        while True:
            #SEND A STATE UPDATE OF THE DEVICE TO THE CONTROL PLATFORM EVERY 5 SECONDS
            message = StateUpdateMessage(self.device.name, self.device.device_states)
            self.device.post_message(message, self.destination)
            time.sleep(5)