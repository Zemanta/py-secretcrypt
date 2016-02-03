import unittest

from secretcrypt import encrypt_secret


class MockCrypter(object):

    @classmethod
    def encrypt(cls, plaintext):
        return 'ciphertext'


class TestEncryptCmd(unittest.TestCase):

    def test_encrypt(self):
        secret = encrypt_secret.encrypt_secret(MockCrypter, 'myplaintext').secret
        self.assertIn(':', secret)
        class_name, ciphertext = secret.split(':')
        self.assertEqual(class_name, MockCrypter.__name__)
        self.assertEqual(ciphertext, 'ciphertext')
