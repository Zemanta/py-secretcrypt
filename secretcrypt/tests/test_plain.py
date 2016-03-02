import unittest

from secretcrypt import plain


class TestLocal(unittest.TestCase):

    def test_encrypt_decrypt(self):
        plaintext = b'myplaintext'
        ciphertext, decrypt_params = plain.encrypt(plaintext)
        self.assertEqual(plaintext, plain.decrypt(ciphertext, **decrypt_params))
