class DeviceCommandMessage(object):
    #SENT FROM CONTROL APPLICATION TO CONTROL CONTROL PLATFORM
    #SENT FROM CONTROL PLATFORM TO DEVICE

    def __init__(self, device_name, device_state_name, device_state_value):
        # string
        self.device_name = device_name
        # string
        self.device_state_name = device_state_name
        # int
        self.device_state_value = device_state_value

    def __str__(self):
        return type(self).__name__ + '|' + 'DEVICE_NAME=' + self.device_name + '|' + 'DEVICE_STATE_NAME=' + str(self.device_state) + '|' + 'DEVICE_STATE_VALUE=' + str(self.device_state_value)