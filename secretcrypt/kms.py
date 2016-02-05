import base64

import boto3

_region = 'us-east-1'
_key_id = None
__kms_client = None


def set_region(region_name):
    global _region
    _region = region_name


def set_key_id(key_id):
    global _key_id
    _key_id = key_id


def _kms_client():
    global __kms_client
    if not __kms_client:
        __kms_client = boto3.client('kms', region_name=_region)
    return __kms_client


def encrypt(plaintext):
    ciphertext_blob = _kms_client().encrypt(
        KeyId=_key_id,
        Plaintext=plaintext
    )['CiphertextBlob']
    return base64.b64encode(ciphertext_blob)


def decrypt(ciphertext):
    return _kms_client().decrypt(
        CiphertextBlob=base64.b64decode(ciphertext)
    )['Plaintext']
