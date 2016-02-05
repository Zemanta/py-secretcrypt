"""
Encrypts secrets. Reads secrets as user input or from standard input.

Usage:
  encrypt-secret kms [--region=<region_name>] <key_id>
  encrypt-secret local

Options:
  --region=<region_name>    AWS Region Name [default: us-east-1]
"""
from __future__ import print_function
from docopt import docopt
import sys

from secretcrypt import Secret


def encrypt_secret(module, plaintext):
    ciphertext = module.encrypt(plaintext)
    module_name = module.__name__.split('.')[-1]
    return Secret('%s:%s' % (module_name, ciphertext))


def encrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    if arguments['kms']:
        import kms
        kms.set_region(arguments['--region'])
        kms.set_key_id(arguments['<key_id>'])
        module = kms
    elif arguments['local']:
        import local
        module = local

    # do not print prompt if input is being piped
    prompt = 'Enter plaintext: ' if sys.stdin.isatty() else ''
    plaintext = raw_input(prompt)
    secret = encrypt_secret(module, plaintext)
    return secret.secret

if __name__ == '__main__':
    print(encrypt_secret_cmd())
