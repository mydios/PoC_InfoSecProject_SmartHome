class RegisterDeviceMessage(object):
    #SENT FROM DEVICE TO CONTROL PLATFORM
    
    def __init__(self, device_name, command_manual, encryption_type="no_encryption", encryption_args=[]):
        # string
        self.device_name = device_name
        # command_manual = dictionary(str:list((int, str))) = dictionary(state_name:list((state_value, value_name)))
        self.command_manual = command_manual

        # THE ENCRYPTION SUPPORTED BY THIS DEVICE IS INCORPORATED IN THE MESSAGE
        # string
        self.encryption_type = encryption_type
        # list
        self.encryption_args = encryption_args

    def __str__(self):
        return type(self).__name__ + '|' + 'DEVICE_NAME=' + self.device_name + '|' + 'COMMAND_MANUAL=' + str(self.command_manual) + '|' + 'ENCRYPTION_DETAILS=' + self.encryption_type + ', ' + str(self.encryption_args)

    def __repr__(self):
        return self.__str__()