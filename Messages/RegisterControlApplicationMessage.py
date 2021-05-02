class RegisterControlApplicationMessage(object):
    #SENT FROM CONTROL APPLICATION TO CONTROL PLATFORM
    
    def __init__(self, application_name, credentials, authorisation_level, encryption_type="no_encryption", encryption_args=[]):
        # string
        self.application_name = application_name
        # string
        self.credentials = credentials
        # string
        self.authorisation_level = authorisation_level

        # THE ENCRYPTION SUPPORTED BY THIS CONTROL APPLICATION IS INCORPORATED IN THE MESSAGE
        # string
        self.encryption_type = encryption_type
        # list
        self.encryption_args = encryption_args

    def __str__(self):
        return type(self).__name__ + '|' + 'APPLICATION_NAME=' + self.application_name + 'CREDENTIALS=' + self.credentials + '|' + 'ENCRYPTION_DETAILS=' + self.encryption_type + ', ' + str(self.encryption_args)

    def __repr__(self):
        return self.__str__()