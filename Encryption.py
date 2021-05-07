import time
import uuid

def generate_session_key():
    # TO DO
    time.sleep(0.5)
    return 'deadbeef'

def encrypt_symm(key, data):
    # TO DO
    return str(data).encode('utf-8').hex()

def decrypt_symm(key, data):
    # TO DO
    # don't use eval in final version, not safe
    return eval(bytes.fromhex(data).decode('utf-8'))

def stringToKey(word):
    return str(word).encode('utf-8').hex()

def generate_nonce():
    # https://stackoverflow.com/questions/5590170/what-is-the-standard-method-for-generating-a-nonce-in-python
    return uuid.uuid4().hex

def generate_subkey(key):
    # TO DO
    return key[int(len(key)/2):]