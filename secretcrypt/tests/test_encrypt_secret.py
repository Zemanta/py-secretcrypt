import unittest

from secretcrypt import encrypt_secret, mock_crypter


class TestEncryptCmd(unittest.TestCase):

    def test_encrypt(self):
        secret = encrypt_secret.encrypt_secret(mock_crypter, 'myplaintext').secret
        self.assertIn(':', secret)
        class_name, ciphertext = secret.split(':')
        self.assertEqual(class_name, mock_crypter.__name__)
        self.assertEqual(ciphertext, 'ciphertext')
