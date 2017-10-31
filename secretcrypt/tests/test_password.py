import mock
import unittest

from secretcrypt import password


class TestPassword(unittest.TestCase):

    @mock.patch.object(password, 'input')
    def test_encrypt_decrypt(self, mock_raw_input):
        mock_raw_input.return_value = 'testpass'
        plaintext = b'myplaintext'
        ciphertext, decrypt_params = password.encrypt(plaintext)
        self.assertEqual(plaintext, password.decrypt(ciphertext, **decrypt_params))
