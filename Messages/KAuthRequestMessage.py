class KAuthRequestMessage(object):
    #SENT FROM CONTROL APPLICATION TO KERBEROS AUTHENTICATION SERVER
    #slide 22 (C --> AS)

    def __init__(self, options, client_id, client_realm, tgs_id, times, nonce):
        # string
        self.options = options
        # int
        self.client_id = client_id
        # string
        self.client_realm = client_realm
        # int
        self.tgs_id = tgs_id
        # string
        self.times = times
        # string
        self.nonce = nonce
    
    def __str__(self):
        return type(self).__name__ + '|' + 'OPTIONS=' + self.options + '|' + 'CLIENT_ID=' + str(self.client_id) + '|' + 'CLIENT_REALM=' + self.client_realm + '|' + 'TGS_ID=' + str(self.tgs_id) + '|' + 'TIMES=' + self.times + '|' + 'NONCE=' + self.nonce
    
    def __repr__(self):
        return self.__str__()