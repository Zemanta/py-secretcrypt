from __future__ import print_function
import base64
import os
import getpass

import pyscrypt

from secretcrypt import base_aes


def _get_key_salt(salt=None):
    password = getpass.getpass('Enter password: ').encode()
    if not salt:
        salt = base64.b64encode(os.urandom(16))
    key = pyscrypt.hash(
        password=password,
        salt=salt,
        N=1024,
        r=1,
        p=1,
        dkLen=24,
    )
    return key, salt


def encrypt(plaintext):
    key, salt = _get_key_salt()
    return base_aes.encrypt_plaintext(key, plaintext), {'salt': salt}


def decrypt(ciphertext, salt):
    key, _ = _get_key_salt(salt)
    return base_aes.decrypt_ciphertext(key, ciphertext)
