import getpass
import mock
import unittest

from secretcrypt import password


class TestPassword(unittest.TestCase):

    @mock.patch.object(getpass, 'getpass')
    def test_encrypt_decrypt(self, mock_getpass):
        mock_getpass.return_value = 'testpass'
        plaintext = b'myplaintext'
        ciphertext, decrypt_params = password.encrypt(plaintext)
        self.assertEqual(plaintext, password.decrypt(ciphertext, **decrypt_params))
