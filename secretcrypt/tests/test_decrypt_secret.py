import mock
import sys
import unittest

from secretcrypt import decrypt_secret


class TestDecryptCmd(unittest.TestCase):

    @mock.patch.object(sys, 'stdout')
    def test_encrypt_kms(self, mock_stdout):
        with mock.patch.object(sys, 'argv', ['decrypt-secret', 'mock_crypter::test']):
            decrypt_secret.decrypt_secret_cmd()
            mock_stdout.write.assert_has_calls([
                mock.call('plaintext'),
                mock.call('\n'),
            ])
