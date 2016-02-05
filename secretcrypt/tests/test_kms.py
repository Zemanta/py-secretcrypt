import base64
import mock
from six.moves import reload_module
import unittest

from secretcrypt import kms


class TestLocal(unittest.TestCase):

    def setUp(self):
        reload_module(kms)
        self.patcher = mock.patch('boto3.client')
        self.boto3_client = self.patcher.start()
        self.mock_kms_client = mock.MagicMock()
        self.boto3_client.return_value = self.mock_kms_client

        self.key = 'mykey'
        self.region = 'myregion'
        self.plaintext = 'myplaintext'
        self.ciphertext_blob = b'abc'
        self.ciphertext = base64.b64encode(self.ciphertext_blob)

    def test_lazy_kms_client(self):
        self.mock_kms_client.encrypt.return_value = dict(CiphertextBlob=self.ciphertext_blob)
        ciphertext, decrypt_params = kms.encrypt('a', 'region1', 'key1')
        self.boto3_client.assert_called_with(
            'kms',
            region_name='region1'
        )
        ciphertext, decrypt_params = kms.encrypt('a', 'region2', 'key2')
        self.boto3_client.assert_called_with(
            'kms',
            region_name='region2'
        )

        self.boto3_client.reset_mock()
        ciphertext, decrypt_params = kms.encrypt('a', 'region1', 'key1')
        self.boto3_client.assert_not_called()

    def test_encrypt(self):
        self.mock_kms_client.encrypt.return_value = dict(CiphertextBlob=self.ciphertext_blob)
        ciphertext, decrypt_params = kms.encrypt(self.plaintext, self.region, self.key)
        self.boto3_client.assert_called_with(
            'kms',
            region_name=self.region
        )
        self.mock_kms_client.encrypt.assert_called_with(
            KeyId=self.key,
            Plaintext=self.plaintext
        )
        self.assertEqual(ciphertext, self.ciphertext)
        self.assertEqual(decrypt_params, dict(region=self.region))

    def test_decrypt(self):
        self.mock_kms_client.decrypt.return_value = dict(Plaintext=self.plaintext)
        plaintext = kms.decrypt(self.ciphertext, self.region)
        self.boto3_client.assert_called_with(
            'kms',
            region_name=self.region
        )
        self.mock_kms_client.decrypt.assert_called_with(
            CiphertextBlob=self.ciphertext_blob
        )
        self.assertEqual(plaintext, self.plaintext)
