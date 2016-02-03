"""
Encrypted secrets.

Usage:
  encrypt-secret kms [--region=<region_name>] <key_id> <plaintext>
  encrypt-secret local <plaintext>

Options:
  --region=<region_name>    AWS Region Name [default: us-east-1]
"""
from __future__ import print_function
from docopt import docopt

from secretcrypt import Secret


def encrypt_secret(cls, plaintext):
    ciphertext = cls.encrypt(plaintext)
    return Secret('%s:%s' % (cls.__name__, ciphertext))


def encrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    if arguments['kms']:
        from kms import KMS
        KMS.set_region(arguments['--region'])
        KMS.set_key_id(arguments['<key_id>'])
        cls = KMS
    elif arguments['local']:
        from local import Local
        cls = Local
    secret = encrypt_secret(cls, arguments['<plaintext>'])
    return secret.secret

if __name__ == '__main__':
    print(encrypt_secret_cmd())
