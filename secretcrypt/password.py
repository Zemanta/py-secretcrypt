from __future__ import print_function
import base64
import os

import pyscrypt
from six.moves import input

from secretcrypt import base_aes


def _get_key_salt(salt=None):
    password = input('Enter password: ').encode()
    if not salt:
        salt = base64.b64encode(os.urandom(16))
    key = pyscrypt.hash(
        password=password,
        salt=salt,
        N=32768,
        r=8,
        p=1,
        dkLen=32,
    )
    return key, salt


def encrypt(plaintext):
    key, salt = _get_key_salt()
    return base_aes.encrypt_plaintext(key, plaintext), {'salt': salt}


def decrypt(ciphertext, salt):
    key, _ = _get_key_salt(salt)
    return base_aes.decrypt_ciphertext(key, ciphertext)
