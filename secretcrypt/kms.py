import base64

import boto3

_kms_clients = {}


def _kms_client(region):
    global _kms_clients
    if region not in _kms_clients:
        kms_client = boto3.client('kms', region_name=region)
        _kms_clients[region] = kms_client
    return _kms_clients[region]


def encrypt(plaintext, region, key_id):
    ciphertext_blob = _kms_client(region).encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )['CiphertextBlob']
    return base64.b64encode(ciphertext_blob), dict(region=region)


def decrypt(ciphertext, region):
    return _kms_client(region).decrypt(
        CiphertextBlob=base64.b64decode(ciphertext)
    )['Plaintext']
