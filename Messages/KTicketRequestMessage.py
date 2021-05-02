class KTicketRequestMessage(object):
    #SENT FROM CONTROL APPLICATION TO KERBEROS TICKET-GRANTING SERVER

    def __init__(self, options, service_id, times, nonce, tgt, auth_data):
        # string
        self.options = options
        # int
        self.service_id = service_id
        # string
        self.times = times
        # string
        self.nonce = nonce
        # encrypted data
        self.tgt = tgt
        # encrypted data
        self.auth_data = auth_data
    
    def __str__(self):
        return type(self).__name__ + '|' + 'OPTIONS=' + self.options + '|' + 'SERVICE_ID=' + str(self.service_id) + '|' + 'TIMES=' + self.times + '|' + 'NONCE=' + self.nonce + '|' + 'TGT=' + self.tgt + '|' + 'AUTH_DATA=' + self.auth_data
    
    def __repr__(self):
        return self.__str__()