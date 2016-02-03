import base64

import boto3

class KMS(object):
    _region = 'us-east-1'
    _key_id = None
    __kms_client = None

    @classmethod
    def set_region(cls, region_name):
        cls._region = region_name

    @classmethod
    def set_key_id(cls, key_id):
        cls._key_id = key_id

    @classmethod
    def _kms_client(cls):
        if not cls.__kms_client:
            cls.__kms_client = boto3.client('kms', region_name=cls._region)
        return cls.__kms_client

    @classmethod
    def encrypt(cls, plaintext):
        ciphertext_blob = cls._kms_client().encrypt(
            KeyId=cls._key_id,
            Plaintext=plaintext
        )['CiphertextBlob']
        return base64.b64encode(ciphertext_blob)

    @classmethod
    def decrypt(cls, ciphertext):
        return cls._kms_client().decrypt(
            CiphertextBlob=base64.b64decode(ciphertext)
        )['Plaintext']
