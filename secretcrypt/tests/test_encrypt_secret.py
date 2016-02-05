import unittest
from six.moves import urllib

from secretcrypt import encrypt_secret, mock_crypter


class TestEncryptCmd(unittest.TestCase):

    def test_encrypt(self):
        secret = encrypt_secret.encrypt_secret(
            mock_crypter,
            'myplaintext',
            dict(my_decrypt_param='abc')
        )
        self.assertEqual('mock_crypter:my_decrypt_param=abc:ciphertext',
                         secret)
