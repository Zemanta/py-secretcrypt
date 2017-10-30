import mock
import unittest
import __builtin__

from secretcrypt import password


class TestPassword(unittest.TestCase):

    @mock.patch.object(__builtin__, 'raw_input')
    def test_encrypt_decrypt(self, mock_raw_input):
        mock_raw_input.return_value = 'testpass'
        plaintext = b'myplaintext'
        ciphertext, decrypt_params = password.encrypt(plaintext)
        self.assertEqual(plaintext, password.decrypt(ciphertext, **decrypt_params))
