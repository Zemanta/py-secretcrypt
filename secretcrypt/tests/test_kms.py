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

    def test_encrypt(self):
        self.mock_kms_client.encrypt.return_value = dict(CiphertextBlob=self.ciphertext_blob)
        kms.set_key_id(self.key)
        kms.set_region(self.region)
        ciphertext = kms.encrypt(self.plaintext)
        self.boto3_client.assert_called_with(
            'kms',
            region_name=self.region
        )
        self.mock_kms_client.encrypt.assert_called_with(
            KeyId=self.key,
            Plaintext=self.plaintext
        )
        self.assertEqual(ciphertext, self.ciphertext)

    def test_decrypt(self):
        self.mock_kms_client.decrypt.return_value = dict(Plaintext=self.plaintext)
        kms.set_region(self.region)
        plaintext = kms.decrypt(self.ciphertext)
        self.boto3_client.assert_called_with(
            'kms',
            region_name=self.region
        )
        self.mock_kms_client.decrypt.assert_called_with(
            CiphertextBlob=self.ciphertext_blob
        )
        self.assertEqual(plaintext, self.plaintext)
