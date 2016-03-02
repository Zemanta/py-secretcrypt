import unittest
import mock

import secretcrypt
from secretcrypt import StrictSecret, Secret


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

        secret = StrictSecret('mock_crypter:key=value&key2=value2:myciphertext')
        self.assertEqual(secret._decrypt_params, dict(key='value', key2='value2'))
        self.assertEqual(secret._ciphertext, b'myciphertext')

        secret.decrypt()
        secret.decrypt()
        mock_crypter_module.decrypt.assert_called_with(
            b'myciphertext',
            key='value',
            key2='value2',
        )

    def test_decrypt_plain(self):
        secret = StrictSecret('plain::mypass')
        self.assertEqual('mypass', secret.decrypt())

    @mock.patch('importlib.import_module')
    def test_eager_decrypt(self, mock_import_module):
        mock_crypter_module = mock.MagicMock()
        mock_crypter_module.decrypt.side_effect = lambda *args, **kwargs: b'plaintext'
        mock_crypter_module.__name__ = 'secretcrypt.mock_crypter'

        def mock_import_side_effect(*args, **kwargs):
            self.assertEqual(kwargs['package'], secretcrypt.__name__)
            if args[0] == '.mock_crypter':
                return mock_crypter_module
            raise Exception('Importing wrong module')
        mock_import_module.side_effect = mock_import_side_effect

        secret = Secret('mock_crypter:key=value&key2=value2:myciphertext')
        mock_crypter_module.decrypt.assert_called_with(
            b'myciphertext',
            key='value',
            key2='value2',
        )
        mock_crypter_module.reset_mock()
        plaintext = secret.get()
        self.assertEqual('plaintext', plaintext)
        mock_crypter_module.assert_not_called()

    # def test_encoding(self):
    #     plaintext = '?\x9a\xc4\xea\xb4\xf5\xc3\xb7\xc4\x9d\xec)C\x94i\x07\x1a&\xf3\x1e2\xdd\x95c[=\xb9\xc7c\xef1\x12'
    #     s = Secret('plain::' + plaintext)
    #     self.assertEqual(s.get(encoding=None), plaintext)
