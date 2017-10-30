"""
Encrypts secrets. Reads secrets as user input or from standard input.

Usage:
  encrypt-secret [options] kms [--region=<region_name>] <key_id>
  encrypt-secret [options] local
  encrypt-secret [options] plain
  encrypt-secret [options] password

Options:
  --region=<region_name>    AWS Region Name [default: us-east-1]
  --multiline               Multiline input (read stdin bytes until EOF)
"""
from __future__ import print_function
from docopt import docopt
from six.moves import urllib
import os
import sys


def encrypt_secret(module, plaintext, encrypt_params):
    ciphertext, decrypt_params = module.encrypt(plaintext, **encrypt_params)
    module_name = module.__name__.split('.')[-1]
    return '{module_name}:{decrypt_params}:{ciphertext}'.format(
        module_name=module_name,
        ciphertext=ciphertext.decode('utf-8'),
        decrypt_params=urllib.parse.urlencode(decrypt_params),
    )


def encrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    encrypt_params = dict()
    if arguments['kms']:
        from secretcrypt import kms
        encrypt_params = dict(
            region=arguments['--region'],
            key_id=arguments['<key_id>'],
        )
        module = kms
    elif arguments['local']:
        from secretcrypt import local
        module = local
    elif arguments['plain']:
        from secretcrypt import plain
        module = plain
    elif arguments['password']:
        from secretcrypt import password
        module = password

    if arguments['--multiline']:
        plaintext = sys.stdin.read()
    else:
        # do not print prompt if input is being piped
        if sys.stdin.isatty():
            print('Enter plaintext: ', end="", file=sys.stderr),
            sys.stderr.flush()
        stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
        plaintext = stdin.readline().rstrip(b'\n')

    secret = encrypt_secret(module, plaintext, encrypt_params)
    print(secret)


if __name__ == '__main__':
    encrypt_secret_cmd()
