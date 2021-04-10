from multiprocessing.connection import Client


class CommunicationInterface(object):
    def __init__(self, addr, name, pw='strong_password', encryption_type = "no_encryption", encryption_args =[]):
        # CREATE CLIENT CONNECTION TO ONE OF THE LISTENERS IN THE BROKER
        self.client = Client(address=addr, authkey=pw.encode())
        # SET NAME FOR COMMUNICATION
        self.name = name
        # SET ENCRYPTION TYPE
        self.encryption_type = encryption_type
        # SET ENCRYPTION ARGS
        self.encryption_args = encryption_args
        # FIRST REGISTER MESSAGE TO BROKER, CONTENT IS NAME
        self.post_message(self.name, None)
        

    def post_message(self, message, destination):
        # SEND A MESSAGE
        # Messages are pickled tuples of the form (string, object, string)=(sender_name, message, destination_name)
        # Encryption is performed using encryption factory function _encrypt
        message = self._encrypt(
            message)
        self.client.send((self.name, message, destination))

    def receive_message(self):
        # RECIEVE A MESSAGE
        message = self.client.recv()
        # Decryption is performed using decryption factory function _decrypt
        message = self._decrypt(
            message)
        return message

    def _encrypt(self, message):
        #ENCRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message

    def _decrypt(self, message):
        #DECRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message
