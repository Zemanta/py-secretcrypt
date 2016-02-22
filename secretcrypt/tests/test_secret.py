import unittest
import mock

import secretcrypt
from secretcrypt import Secret


class TestSecret(unittest.TestCase):

    @mock.patch('importlib.import_module')
    def test_decrypt(self, mock_import_module):
        mock_crypter_module = mock.MagicMock()
        mock_crypter_module.__name__ = 'secretcrypt.mock_crypter'

        def mock_import_side_effect(*args, **kwargs):
            self.assertEqual(kwargs['package'], secretcrypt.__name__)
            if args[0] == '.mock_crypter':
                return mock_crypter_module
            raise Exception('Importing wrong module')
        mock_import_module.side_effect = mock_import_side_effect

        secret = Secret('mock_crypter:key=value&key2=value2:myciphertext')
        self.assertEqual(secret._decrypt_params, dict(key='value', key2='value2'))
        self.assertEqual(secret._ciphertext, 'myciphertext')

        secret.decrypt()
        secret.decrypt()
        mock_crypter_module.decrypt.assert_called_once_with(
            'myciphertext',
            key='value',
            key2='value2',
        )

    def test_decrypt_plain(self):
        secret = Secret('plain::mypass')
        self.assertEqual('mypass', secret.decrypt())
