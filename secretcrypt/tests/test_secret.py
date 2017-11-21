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
        self.assertEqual(b'mypass', secret.decrypt())

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
        self.assertEqual(b'plaintext', plaintext)
        mock_crypter_module.assert_not_called()

    @mock.patch('importlib.import_module')
    def test_decrypt_error(self, mock_import_module):
        mock_crypter_module = mock.MagicMock()
        mock_crypter_module.__name__ = 'secretcrypt.mock_crypter'

        def mock_import_side_effect(*args, **kwargs):
            self.assertEqual(kwargs['package'], secretcrypt.__name__)
            if args[0] == '.mock_crypter':
                return mock_crypter_module
            raise Exception('Importing wrong module')
        mock_import_module.side_effect = mock_import_side_effect

        class MyException(Exception):
            pass

        mock_crypter_module.decrypt.side_effect = MyException
        secret = StrictSecret('mock_crypter:key=value&key2=value2:myciphertext')
        # with self.assertRaises(ValueError):
        secret.decrypt()
