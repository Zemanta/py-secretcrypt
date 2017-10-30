import mock
import sys
import os
import unittest

from secretcrypt import encrypt_secret, mock_crypter, kms, plain, local, password


class TestEncryptHelper(unittest.TestCase):

    def test_encrypt(self):
        secret = encrypt_secret.encrypt_secret(
            mock_crypter,
            b'myplaintext',
            dict(my_decrypt_param='abc')
        )
        self.assertEqual('mock_crypter:my_decrypt_param=abc:ciphertext',
                         secret)


class TestEncryptCmd(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch.object(encrypt_secret, 'encrypt_secret')
        self.addCleanup(patcher.stop)
        self.mock_encrypt_secret = patcher.start()

        patcher = mock.patch.object(os, 'fdopen')
        self.addCleanup(patcher.stop)
        mock_fdopen = patcher.start()
        self.mock_stdin = mock.MagicMock()
        mock_fdopen.return_value = self.mock_stdin

    def test_encrypt_kms(self):
        with mock.patch.object(sys, 'argv', ['encrypt-secret', 'kms', 'alias/MyKey']):
            self.mock_stdin.readline.return_value = b'myplaintext\n'
            encrypt_secret.encrypt_secret_cmd()
            self.mock_encrypt_secret.assert_called_once_with(
                kms,
                b'myplaintext',
                dict(region='us-east-1', key_id='alias/MyKey')
            )

    def test_encrypt_plain(self):
        with mock.patch.object(sys, 'argv', ['encrypt-secret', 'plain']):
            self.mock_stdin.readline.return_value = b'myplaintext\n'
            encrypt_secret.encrypt_secret_cmd()
            self.mock_encrypt_secret.assert_called_once_with(
                plain,
                b'myplaintext',
                dict()
            )

    def test_encrypt_local(self):
        with mock.patch.object(sys, 'argv', ['encrypt-secret', 'local']):
            self.mock_stdin.readline.return_value = b'myplaintext\n'
            encrypt_secret.encrypt_secret_cmd()
            self.mock_encrypt_secret.assert_called_once_with(
                local,
                b'myplaintext',
                dict()
            )

    def test_encrypt_password(self):
        with mock.patch.object(sys, 'argv', ['encrypt-secret', 'password']):
            self.mock_stdin.readline.return_value = b'myplaintext\n'
            encrypt_secret.encrypt_secret_cmd()
            self.mock_encrypt_secret.assert_called_once_with(
                password,
                b'myplaintext',
                dict()
            )
