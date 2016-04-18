def encrypt(plaintext, my_decrypt_param):
    return b'ciphertext', dict(my_decrypt_param=my_decrypt_param)


def decrypt(ciphertext):
    return b'plaintext'
