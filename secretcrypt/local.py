import os

import appdirs
import cryptography.fernet


__crypter = None


def _crypter():
    global __crypter
    if not __crypter:
        data_dir = appdirs.user_data_dir(__name__, '')
        key_file = os.path.join(data_dir, 'key')
        if os.path.isfile(key_file):
            with open(key_file) as f:
                key = f.read()
        else:
            key = cryptography.fernet.Fernet.generate_key()
            try:
                os.makedirs(data_dir)
            except OSError as e:
                # errno17 == dir exists
                if e.errno != 17:
                    raise
            with open(key_file, 'wb') as f:
                f.write(key)
        __crypter = cryptography.fernet.Fernet(key)
    return __crypter


def encrypt(plaintext):
    return _crypter().encrypt(plaintext)


def decrypt(ciphertext):
    return _crypter().decrypt(ciphertext)
