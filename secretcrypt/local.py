import os

import appdirs
import cryptography.fernet


class Local(object):
    __crypter = None

    @classmethod
    def _crypter(cls):
        if not cls.__crypter:
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
            cls.__crypter = cryptography.fernet.Fernet(key)
        return cls.__crypter

    @classmethod
    def encrypt(cls, plaintext):
        return cls._crypter().encrypt(plaintext)

    @classmethod
    def decrypt(cls, ciphertext):
        return cls._crypter().decrypt(ciphertext)
