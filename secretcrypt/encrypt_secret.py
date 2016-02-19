"""
Encrypts secrets. Reads secrets as user input or from standard input.

Usage:
  encrypt-secret kms [--region=<region_name>] <key_id>
  encrypt-secret local
  encrypt-secret plain

Options:
  --region=<region_name>    AWS Region Name [default: us-east-1]
"""
from __future__ import print_function
from docopt import docopt
from six.moves import urllib
import sys


def encrypt_secret(module, plaintext, encrypt_params):
    ciphertext, decrypt_params = module.encrypt(plaintext, **encrypt_params)
    module_name = module.__name__.split('.')[-1]
    return '{module_name}:{decrypt_params}:{ciphertext}'.format(
        module_name=module_name,
        ciphertext=ciphertext,
        decrypt_params=urllib.parse.urlencode(decrypt_params),
    )


def encrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    encrypt_params = dict()
    if arguments['kms']:
        import kms
        encrypt_params = dict(
            region=arguments['--region'],
            key_id=arguments['<key_id>'],
        )
        module = kms
    elif arguments['local']:
        import local
        module = local
    elif arguments['plain']:
        import plain
        module = plain

    # do not print prompt if input is being piped
    prompt = 'Enter plaintext: ' if sys.stdin.isatty() else ''
    plaintext = raw_input(prompt)
    secret = encrypt_secret(module, plaintext, encrypt_params)
    return secret


if __name__ == '__main__':
    print(encrypt_secret_cmd())
