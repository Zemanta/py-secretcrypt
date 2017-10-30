import base64
import os
import sys

from secretcrypt import base_aes


__key = None


def _key():
    global __key
    if __key:
        return __key

    data_dir = _key_dir()
    key_file = os.path.join(data_dir, 'key')

    if os.path.isfile(key_file):
        with open(key_file, 'rb') as f:
            __key = base64.b64decode(f.read())
            return __key

    __key = base64.b64encode(os.urandom(16))
    try:
        os.makedirs(data_dir)
    except OSError as e:
        # errno17 == dir exists
        if e.errno != 17:
            raise
    with open(key_file, 'wb') as f:
        f.write(__key)
    return __key


def _key_dir():
    data_dir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    if sys.platform.startswith('darwin'):
        data_dir = os.path.expanduser('~/Library/Application Support')
    elif sys.platform in ['win32', 'cygwin']:
        data_dir = os.path.expanduser('~\\AppData\\Local\\')
    return os.path.join(data_dir, "secretcrypt")


def encrypt(plaintext):
    return base_aes.encrypt_plaintext(_key(), plaintext), {}


def decrypt(ciphertext):
    return base_aes.decrypt_ciphertext(_key(), ciphertext)
