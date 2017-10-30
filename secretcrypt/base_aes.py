import base64
import os

import pyaes


def encrypt_plaintext(key, plaintext):
    iv = os.urandom(16)
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    encrypter = pyaes.Encrypter(aes)
    ciphertext_blob = encrypter.feed(plaintext)
    ciphertext_blob += encrypter.feed()  # flush
    return base64.b64encode(iv + ciphertext_blob)


def decrypt_ciphertext(key, ciphertext):
    blob = base64.b64decode(ciphertext)
    iv = blob[:16]
    ciphertext_blob = blob[16:]
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    decrypter = pyaes.Decrypter(aes)
    plaintext = decrypter.feed(ciphertext_blob)
    plaintext += decrypter.feed()  # flush
    return plaintext
